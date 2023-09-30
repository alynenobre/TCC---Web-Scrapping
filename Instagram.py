from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

# PIP

import multiprocessing
import wget
import json
import time 
import datetime


# Configuracoes do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3') # Execute o Chrome no modo headless, se necessário


#Iniciando o navegador
browser = webdriver.Chrome(options=chrome_options)

# Abrindo site da rede social
browser.get('https://www.instagram.com/')

#Login da redes social
username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "input['username']" ))
password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "input['password']" ))

username.send_keys()
password.send_keys()


time.sleep(120)


