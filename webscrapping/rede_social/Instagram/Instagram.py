#PIP
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import datetime

#Pacotes
from rede_social.browser import Browser
import rede_social.contantes as CONST

class Instagram():
    def __init__(self):
        self.browser = None

    def login(self, username:str, password:str):
        self.browser = Browser(api_name="INSTAGRAM").open_browser()
        self.browser.get('https://www.instagram.com/')
        
        #Login da rede social
        username_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        username_input.send_keys(username)
        time.sleep(2)
        password_input.send_keys(password)
        time.sleep(2)
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        time.sleep(2)


    def get_post_hashtag(self, hashtag:str):  # Renomeando para 'get_post_hashtag'
        if self.browser is None:
            print("Você precisa fazer login primeiro.")
            return []

        self.browser.get(f'https://www.instagram.com/tags/{hashtag}')
        post_data = []
        
        for _ in range(5):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            elements_xpath1 = self.browser.find_elements(By.CSS_SELECTOR, 'article > div > div')
            
            for post in elements_xpath1:
                image_url = post.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                try:
                    # Clique no post para abrir mais detalhes
                    post.click()
                    time.sleep(2)  # Aguarde a página carregar após clicar no post
                    
                    # Extrair o número de curtidas do post aberto
                    likes_element = self.browser.find_element(By.CSS_SELECTOR, 'button > span')
                    likes = likes_element.text
                except NoSuchElementException:
                    # Se não puder encontrar o número de curtidas, defina-o como "N/A" ou outro valor padrão
                    likes = "N/A"
                
                # Voltar para a página anterior
                self.browser.execute_script("window.history.go(-1)")
                time.sleep(2)  # Aguarde a página voltar antes de continuar

                post_data.append({
                    "hashtag": hashtag,
                    "image_url": image_url,
                    "likes": likes,
                    "data_execution": datetime.datetime.now()
                })

        return post_data




