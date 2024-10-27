from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import json
import datetime
import re
from transformers import pipeline

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
        # Configurando o caminho do ChromeDriver
        service = Service(r'C:\Users\alyne.custodio\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get('https://www.instagram.com')
        sleep(2)

        # Inserindo nome de usuário e senha
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(5)

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
        comments = self.driver.find_elements(By.XPATH, '//span[contains(@class, "_ap3a _aaco _aacu _aacx _aad7 _aade")]')

        # Inicializando a lista para armazenar os dados dos comentários
        post_data = []

        # Iterando sobre os comentários capturados
        for comment in comments:
            try:
                comment_text = comment.text
                processed_text = replace_emojis(comment_text)
                result = sentiment_analysis(processed_text)[0]
                
                post_data.append({
                    "comentário": comment_text,
                    "sentimento": {
                        "label": result['label'],
                        "score": result['score']
                    },
                    "data_recolhimento": datetime.datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Erro ao processar o comentário: {e}")
                continue

        # Convertendo a lista de dicionários para JSON
        json_data = json.dumps(post_data, indent=4, ensure_ascii=False)
        print(json_data)

        # Salvando os dados em um arquivo JSON
        with open('instagram_comments.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

    def close(self):
        # Fechando o navegador
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    # Substitua pelos seus dados de login
    username = 'tcc4261@gmail.com'
    password = '24450479@Ju'
    post_url = 'https://www.instagram.com/p/Cwva6UixMpH/'  # URL do post a ser analisado

    instagram_bot = Instagram(username, password)
    instagram_bot.login()
    instagram_bot.collect_comments(post_url)
    instagram_bot.close()
