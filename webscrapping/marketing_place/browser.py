# STDLib
import time
import json
import os.path
from random import random
from contextlib import contextmanager

# PIP
#Sfrom webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions as ex

#packges
from marketing_place.constants import STORE_SAMPLES


class BrowserSoucer:
    global cache_xpath
    cache_xpath = {}
    global SAMPLES
    
    # Check whether or not you need to store Xpath
    if STORE_SAMPLES:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xpath_samples.json'), 'r') as fin:
           
            SAMPLES = json.load(fin)
    else:
        SAMPLES = {}    
    
    # Função para armazenar amostras em um arquivo JSON
    def store_samples(updates:dict=None):
        if updates is not None:
            for key, value in updates.items():
                if key in SAMPLES: SAMPLES[key].append(value)
                else: SAMPLES[key] = [value]
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xpath_samples.json'), 'w') as fout:
            json.dump(SAMPLES, fout, indent=2)

    # Delay
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
        time.sleep(delay)
        return delay

    
    @contextmanager
    def get_driver(*args, **kwargs):

        # Configura as opções do navegador
        LOCAL = False

        # LOCAL
        if LOCAL: 
            # Especifique o caminho para o executável do Chromedriver baixado
            chromedriver_path = r'C:\Users\alyne.custodio\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

            # Configura as opções do navegador
            service = Service(chromedriver_path)
            options = webdriver.Chrome(service=service)
            # Inicia o navegador e retorna a instância
            driver = webdriver.Chrome(service=service)

        else:
            # Configure the browser
            options = webdriver.ChromeOptions()
            options.headless = True
            options.add_argument("window-size=1920x1080")
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36"
            options.add_argument(f'user-agent={userAgent}')
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

            # Start the browser and return it
            driver = webdriver.Chrome(options=options)


        try:
            yield driver
        finally:
            # Fecha o navegador
            driver.close()

            # Salva as amostras se estiver ativado
            if STORE_SAMPLES:
                BrowserSoucer.store_samples()
