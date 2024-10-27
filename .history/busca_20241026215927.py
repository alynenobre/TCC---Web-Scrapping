from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from random import random
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

    @staticmethod
    def randwait(min_time=5, max_time=10):
        """ for determining delays in capturing data, so as not to block the request

        Args:
            min_time (int, optional): _description_. Defaults to 5.
            max_time (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """        
        delay = round(min_time + (random() * (max_time - min_time)), 2)
        print(f'\t\t...aguardando {delay}s')
        sleep(delay)
        return delay
    
    def login(self):
        # Configurando o WebDriver
        service = Service(r'C:\Users\alyne.custodio\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.randwait()
        self.driver.get('https://www.instagram.com')
        self.randwait()

        # Inserindo nome de usuário e senha
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        self.randwait()
        
    # Função para identificar links HREF
    def identificar_links_href(self, html: str):
        print(f'[Identificando hrefs]')
        links = re.findall(r'href=["\'](.*?)["\']', html)
        return links
    

    def coleta_post_tags(self, tag: str):
        # Acessando uma publicação específica
        self.driver.get(f'https://www.instagram.com/tag/{tag}')
        html_busca = self.driver.page_source
        self.randwait()
        lista_post = self.identificar_links_href(html_busca)
        
        while True:
            try:
                # Encontrando o elemento <div> pelo XPath
                div_element = self.driver.find_element(By.XPATH, '//span[contains(@class, "_ac7v xras4av xgc1b0m xat24cr xzboxd6")]')
                
                # Se o elemento for clicável, clique nele
                if div_element.is_displayed():
                    div_element.click()  # Abre ou ativa o <div>
                    print("Elemento clicado.")

            except Exception as e:
                print(f"Erro ao encontrar o elemento: {e}")
                self.randwait() # Espera aleatoriamente antes de tentar novamente

            html_busca = self.driver.page_source
            self.randwait()
            lista_hrefs = self.identificar_links_href(html_busca)
            # Define a expressão regular
            pattern = r'^/tag/p/[A-Za-z0-9_-]+/$'
            lista_post = [post for post in lista_hrefs if re.match(pattern, post)]
            
            self.randwait()
            # Carregar dados existentes do JSON, se o arquivo já existir
            try:
                with open('instagram_post.txt', 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []  # Se o arquivo não existir ou estiver vazio, inicia com uma lista vazia

            # Adicionar novos dados aos dados existentes
            existing_data.extend(lista_post)

            # Salvando os dados atualizados em um arquivo JSON
            with open('instagram_post.txt', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)


    def close(self):
        # Fechando o navegador
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    # Substitua pelos seus dados de login
    username = 'tcc4261@gmail.com'
    password = '24450479@Ju'
    post_url = 'https://www.instagram.com/p/DBZHjWyRUb8'  # URL do post a ser analisado

    instagram_bot = Instagram(username, password)
    instagram_bot.login()
    instagram_bot.coleta_post_tags("casadedeus")
    instagram_bot.close()
