#PIP
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time 


#Pacotes
from rede_social.browser import Browser

class Instagram():

    def login(self, username:str, password:str ):

        browser= Browser(api_name="INSTAGRAM")
        browser = browser.open_browser()
        browser.get('https://www.instagram.com/')
        
        #Login da redes social
        username_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']" )))
        password_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']" )))

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(120)


