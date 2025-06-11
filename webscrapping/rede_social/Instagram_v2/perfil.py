from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import re


class Perfil:
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

    def extrair_curtidas(self, texto):
        resultado = re.search(r'([\d\.,]+)\s+curtidas', texto)
        if resultado:
            return int(resultado.group(1).replace('.', '').replace(',', ''))
        return 0
    
    def publicações_usuarios(self, usuario: str, scrolls: int = 5):
        self.driver.get(f'https://www.instagram.com/{usuario}')
        url_publi = []

        
        # Realiza rolagens para carregar mais posts
        for _ in range(scrolls):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(2)  # Ajuste conforme sua internet

        # Captura todos os links que são posts (contêm /p/)
        links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')

        url_publi = []
        for link in links:
            href = link.get_attribute('href')
            if href and href not in url_publi:
                url_publi.append(href)
                print(href)

            
        self.driver.quit()
        return url_publi


    def reels_usuarios(self, usuario: str, scrolls: int = 5):
        # Acessa o perfil
        self.driver.get(f'https://www.instagram.com/{usuario}/')

        sleep(5)  # Tempo para login manual se necessário

        # Realiza rolagens para carregar mais posts
        for _ in range(scrolls):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(2)  # Ajuste conforme sua internet

        # Captura todos os links que são REELS (contêm /reel/)
        links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')

        url_reels = []
        for link in links:
            href = link.get_attribute('href')
            if href and href not in url_reels:
                url_reels.append(href)
                print(href)

        self.driver.quit()
        return url_reels
    
    def close(self):
        if self.driver:
            self.driver.quit()
