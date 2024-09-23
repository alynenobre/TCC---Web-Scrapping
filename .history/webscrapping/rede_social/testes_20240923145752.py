from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.service import Service
import json

# Configurando o caminho do ChromeDriver atualizado
service = Service(r'C:\Users\alyne.custodio\Downloads\chromedriver_win64\chromedriver.exe')

# Iniciando o WebDriver com o Service
driver = webdriver.Chrome(service=service)

# Abrindo o Instagram e logando
driver.get('https://www.instagram.com')
sleep(2)

# Inserindo nome de usuário e senha
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')

username_input.send_keys('tcc4261@gmail.com')
password_input.send_keys('24450479@Ju')
password_input.send_keys(Keys.RETURN)
sleep(5)

# Acessando uma publicação específica
driver.get('https://www.instagram.com/p/C8VCGyQSSGS/')
sleep(3)

# Carregando mais comentários (se houver)
while True:
    try:
        load_more_comments = driver.find_element(By.XPATH, '//span[contains(text(), "Ver todos os comentários")]')
        load_more_comments.click()
        sleep(2)
    except:
        break

# Coletando os comentários
comments = driver.find_elements(By.XPATH, '//span[contains(@class, "x1lliihq x1plvlek xryxfnj")]')
# Inicializando a lista para armazenar os dados dos posts
post_data = []

# Iterando sobre os comentários capturados
for comment in comments:
    try:
        comment_text = comment.text
        post_data.append({
            "comentário": comment_text
        })
    except:
        continue

# Convertendo a lista de dicionários para JSON
json_data = json.dumps(post_data, indent=4, ensure_ascii=False)
print(json_data)
# Fechando o navegador
driver.quit()
