from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import json
import datetime
import pandas as pd
from transformers import pipeline
from webscrapping.banco import banco
# Dicionário simples de substituição de emojis
emoji_dict = {
    "😍": "love",
    "🔥": "fire",
    "❤️": "love",
    "🙌": "praise",
    # Adicione mais emojis conforme necessário
}

def replace_emojis(text):
    for emoji, replacement in emoji_dict.items():
        text = text.replace(emoji, replacement)
    return text

# Inicializando a pipeline de análise de sentimento com um modelo multilingue que suporta português
sentiment_analysis = pipeline("sentiment-analysis", model="turing-usp/FinBertPTBR")

class Instagram:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None

    def login(self):
        # Configurando o WebDriver
        service = Service(r'C:\Users\alyne.custodio\Documents\GitHub\TCC---Web-Scrapping\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get('https://www.instagram.com')
        sleep(2)

        # Inserindo nome de usuário e senha
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(15)

    def collect_comments(self, post_url: str):
        # Acessando uma publicação específica
        self.driver.get(post_url)
        sleep(3)

        # Carregando mais comentários (se houver)
        while True:
            try:
                load_more_comments = self.driver.find_element(By.XPATH, '//span[contains(text(), "Ver todos os comentários")]')
                load_more_comments.click()
                sleep(2)
            except:
                break

        # Coletando os comentários
        comments = self.driver.find_elements(By.XPATH, '//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")]')

        # Inicializando a lista para armazenar os dados dos comentários
        post_data = []

        # Iterando sobre os comentários capturados
        for comment in comments:
            try:
                comment_text = comment.text
                comment_html = comment.get_attribute("outerHTML")  # Captura o HTML do elemento
                processed_text = replace_emojis(comment_text)
                result = sentiment_analysis(processed_text)[0]
                
                post_data.append({
                    "comentário": comment_text,
                    "html": comment_html,  # Adiciona o HTML do comentário
                    "sentimento": {
                        "label": result['label'],
                        "score": result['score']
                    },
                    "data_recolhimento": datetime.datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Erro ao processar o comentário: {e}")
                continue

        # Carregar dados existentes do JSON, se o arquivo já existir
        try:
            with open('instagram_comments.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []  # Se o arquivo não existir ou estiver vazio, inicia com uma lista vazia

        # Adicionar novos dados aos dados existentes
        existing_data.extend(post_data)

        # Salvando os dados atualizados em um arquivo JSON
        with open('instagram_comments.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
            
        return existing_data

    def close(self):
        # Fechando o navegador
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    # Substitua pelos seus dados de login
    username = 'tcc4261@gmail.com'
    password = '24450479@Ju'
    post_url = 'https://www.instagram.com/p/DI1-rOrx7Tl/'  # URL do post a ser analisado

    instagram_bot = Instagram(username, password)
    instagram_bot.login()
    resultado = instagram_bot.collect_comments(post_url)
    
    df = pd.DataFrame(resultado)
    for col in df.columns:
        df[col] = df[col].apply(str)

    # Conectando ao banco de dados
    conexao_banco = banco.Banco()
    conexao_banco.conecta_banco(database="rede_social")
    # SQL para criar a tabela 'instagram' no esquema 'public'
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS public.instagram_analise_nl (
        html SERIAL PRIMARY KEY,
        sentimento TEXT NOT NULL, -- Transformado em uma string simples
        comentario TEXT NOT NULL,
        data_recolhimento TIMESTAMP NOT NULL
    );
    """

    # Criar a tabela 'instagram' no esquema 'public'
    conexao_banco.criar_drop_db(sql_create_table)
    
    # Inserindo os dados no banco de dados
    for i in df.index:
        # Acessa diretamente os valores do dicionário
        sentimento_dict = df['sentimento'][i]
        sentimento_str = f"sentimento: {sentimento_dict}".replace("'","")  # Converte o sentimento para string legível
        sql = """
        INSERT INTO public.instagram_analise_nl (html, sentimento, comentario, data_recolhimento) 
        VALUES ('%s', '%s', '%s', '%s')
        ON CONFLICT (html) DO NOTHING; -- Evita erro de duplicação;
        """ % (df['html'][i], sentimento_str, df['comentário'][i], df['data_recolhimento'][i])
        conexao_banco.inserir_db(sql)

    
    instagram_bot.close()
