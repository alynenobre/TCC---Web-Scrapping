#PIP
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import datetime
import re

#Pacotes
from rede_social.browser import Browser
import rede_social.contantes as CONST

class Instagram():
    def __init__(self):
        self.browser = None

    # Função para formatar URL
    def formatar_url(prefixo, produto, sufixo):
        return f"{prefixo}{produto.replace(' ', '+')}{sufixo}"

    # Função para computar JPEG
    def computar_jpeg(self, url: str):
        self.browser.get(url)
        self.browser.execute_script(f"document.body.style.zoom='50%'")
        time.sleep(2)
        jpeg_base64 = self.browser.get_screenshot_as_base64()
        self.browser.close()
        return jpeg_base64

    # Função para identificar links HREF
    def identificar_links_href(self, html: str):
        links = re.findall(r'href=["\'](.*?)["\']', html)
        return links    

    def login(self, username:str, password:str):
        self.username= username
        self.password = password
        self.browser = Browser(api_name="INSTAGRAM").open_browser()
        self.browser.get('https://www.instagram.com/')
        
        #Login da rede social
        self.username_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        self.password_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        self.username_input.send_keys(username)
        time.sleep(2)
        self.password_input.send_keys(password)
        time.sleep(2)
        self.password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        time.sleep(2)


    def get_post_hashtag(self, hashtag:str):  # Renomeando para 'get_post_hashtag'
        self.login(self.username, self.password)
        if self.browser is None:
            print("Você precisa fazer login primeiro.")
            return []

        self.browser.get(f'https://www.instagram.com/tags/{hashtag}')
        post_data = []
        time.sleep(10)
        html_tags = self.browser.page_source
        elements_hrefs = self.identificar_links_href(html_tags)
        regex_post = re.compile(r".*=/p/.*")
        hrefs_post = list(set([url for url in elements_hrefs if regex_post.search(url)]))
        for post in hrefs_post:

            img_element = post.find_element(By.CLASS_NAME, '_aagv')
            image_url =  img_element.get_attribute('src')

            # Encontrando o elemento pai do link
            #parent_element = post.find_element(By.XPATH, '//*[@id="mount_0_0_UN"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div[2]/div/div[1]/div[1]/a')
            
            # Encontrando o link dentro do elemento pai
            link_element = post.find_element(By.CLASS_NAME, '_a6hd')
            url = link_element.get_attribute('href')

            
            # Clique no post para abrir mais detalhes
            self.browser.get(f'{url}')
            time.sleep(2)  # Aguarde a página carregar após clicar no post
            
            # Verifique diretamente um seletor mais simples
            likes_element = self.browser.find_element(By.XPATH, "//*[contains(text(),'curtidas')]")
            likes = likes_element.text

            # Extraindo apenas os dígitos
            likes = re.findall(r'\d+', likes)
            likes = likes[0]

            # Voltar para a página anterior 
            self.browser.execute_script("window.history.go(-1)")
            time.sleep(2)  # Aguarde a página voltar antes de continuar

            post_data.append({
                "hashtag": hashtag,
                "image_url": image_url,
                "likes": likes,
                "url": url, 
                "data_execution": datetime.datetime.now()
            })

        return post_data




