from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class Browser():

    def __init__(self, api_name:str):
        self.api_name = api_name

    def open_browser(self):

        print(self.api_name)
        # Configuracoes do navegador
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--log-level=3') # Execute o Chrome no modo headless, se necessário


        #Iniciando o navegador
        browser = webdriver.Chrome(options=chrome_options)

        # Abrindo site da rede social
        return browser

