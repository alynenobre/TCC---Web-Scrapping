from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import json, re
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
        service = Service(r'C:\Users\alyne.custodio\Documents\GitHub\TCC---Web-Scrapping\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get('https://www.instagram.com')
        sleep(2)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(30)

    def collect_comments(self, post_url: str):
        self.driver.get(post_url)
        sleep(5)

        while True:
            try:
                load_more = self.driver.find_element(By.XPATH, '//span[contains(text(), "Ver todos os comentários")]')
                load_more.click()
                sleep(2)
            except:
                break

        post_data = []

        comentarios_divs = self.driver.find_elements(By.XPATH, '//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")]')
        # Inicializando a lista para armazenar os dados dos comentários
        post_data = []

        # Iterando sobre os comentários capturados
        for comment in comentarios_divs:
            try:
                comment_text = comment.text
                comment_html = comment.get_attribute("outerHTML")  # Captura o HTML do elemento
                processed_text = replace_emojis(comment_text)
                result = sentiment_analysis(processed_text)[0]
                try:
                    nome = comment.find_element(By.XPATH, ".//a[starts-with(@href, '/') and not(contains(@href, '/p/'))]").text
                except:
                    pass
                if nome and comment_text and nome != comment_text:
                    try:
                        curtida_span = comment.find_element(By.XPATH, ".//preceding::span[contains(text(),'curtida')][1]")
                        numero_de_curtida = int(re.findall(r'\d+', curtida_span.text)[0]) if re.findall(r'\d+', curtida_span.text) else 0
                    except:
                        numero_de_curtida = 0

                    comment_html = comment.get_attribute("outerHTML")
                    processed_text = replace_emojis(comment_text)
                    result = sentiment_analysis(processed_text)[0]

                    post_data.append({
                        "comentário": comment_text,
                        "html": comment_html,
                        "perfil": nome,
                        "likes": numero_de_curtida,
                        "sentimento": {
                            "label": result['label'],
                            "score": result['score']
                        },
                        "data_recolhimento": datetime.datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Erro ao processar o comentário: {e}")
                continue
        

        try:
            with open('instagram_comments.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.extend(post_data)

        with open('instagram_comments_2.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        return existing_data

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    username = 'tcc4261@gmail.com'
    password = '24450479@Ju'
    post_url = 'https://www.instagram.com/p/DI1-rOrx7Tl/'

    instagram_bot = Instagram(username, password)
    instagram_bot.login()
    resultado = instagram_bot.collect_comments(post_url)

    df = pd.DataFrame(resultado)
    for col in df.columns:
        df[col] = df[col].apply(str)

    df = pd.DataFrame(resultado)
    df['likes'] = df['likes'].astype(int)

    conexao_banco = banco.Banco()
    conexao_banco.conecta_banco(database="rede_social")

    sql_create_table = """
    CREATE TABLE IF NOT EXISTS public.instagram_analise_nl (
        html TEXT PRIMARY KEY,
        sentimento TEXT NOT NULL,
        comentario TEXT NOT NULL,
        perfil TEXT NOT NULL,
        likes INT NOT NULL,
        data_recolhimento TIMESTAMP NOT NULL
    );
    """
    conexao_banco.criar_drop_db(sql_create_table)

    sql = """
    INSERT INTO public.instagram_analise_nl (html, sentimento, comentario, perfil, likes, data_recolhimento)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (html) DO NOTHING;
    """

    for i in df.index:
        sentimento_dict = df['sentimento'][i]
        sentimento_str = f"sentimento: {sentimento_dict}".replace("'", "")
        valores = (
            df['html'][i],
            sentimento_str,
            df['comentário'][i],
            df['perfil'][i],
            int(df['likes'][i]),
            df['data_recolhimento'][i]
        )
        try:
            conexao_banco.inserir_db(sql, valores)
        except Exception as e:
            print(f"Erro ao inserir dados no banco de dados: {e}")

    instagram_bot.close()