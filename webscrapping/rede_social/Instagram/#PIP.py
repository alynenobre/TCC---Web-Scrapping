#PIP
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
        
        for _ in range(5):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            elements_xpath1 = self.browser.find_elements(By.CSS_SELECTOR, 'article > div > div:nth-child(2)')
            
            for post in elements_xpath1:
                image_url = post.find_element(By.CSS_SELECTOR, 'img').get_attribute("src")
                try:
                    # Clique no post para abrir mais detalhes
                    post.click()
                    time.sleep(2)  # Aguarde a página carregar após clicar no post
                    
                    # Extrair o número de curtidas do post aberto
                    likes_element = self.browser.find_element(By.CSS_SELECTOR, 'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6 > div > article > div > div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x5wqa0o.xln7xf2.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x65f84u.x1vq45kp.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x11njtxf > div > div > div.x78zum5.xdt5ytf.x1q2y9iw.x1n2onr6.xh8yej3.x9f619.x1iyjqo2.x18l3tf1.x26u7qi.xy80clv.xexx8yu.x4uap5.x18d9i69.xkhd6sd > section.x12nagc.x182iqb8.x1pi30zi.x1swvt13 > div > div > span > a > span > span')
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




