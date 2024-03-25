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

        # Especifique o caminho para o executável do Chromedriver baixado
        chromedriver_path = r'C:\Users\alyne.custodio\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

        # Configura as opções do navegador
        service = Service(chromedriver_path)


        # Configuracoes do navegador
        #chrome_options = webdriver.ChromeOptions()
        chrome_options = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        chrome_options.add_argument('--log-level=3') # Execute o Chrome no modo headless, se necessário


        #Iniciando o navegador
        browser = webdriver.Chrome(options=chrome_options)

        # Abrindo site da rede social
        return browser

