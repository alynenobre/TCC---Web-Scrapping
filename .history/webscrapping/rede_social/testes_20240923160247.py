from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.service import Service
import json
from transformers import pipeline

# Dicionário simples de substituição de emojis
emoji_dict = {
    "😍": "love",
    "🔥": "fire",
    "❤️": "love",
    "🙌": "praise",
    # Adicione mais emojis conforme necessário
}

def replace_emojis(text):
    for emoji, replacement in emoji_dict.items():
        text = text.replace(emoji, replacement)
    return text

# Inicializando a pipeline de análise de sentimento
sentiment_analysis = pipeline("sentiment-analysis")

# Configurando o caminho do ChromeDriver
service = Service(r'C:\Users\alyne.custodio\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe')

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
driver.get('https://www.instagram.com/p/Cwva6UixMpH/')
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
comments = driver.find_elements(By.XPATH, '//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")]')
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
# Carregar os dados JSON para realizar a análise de sentimento
data = json.loads(json_data)

# Adicionando a análise de sentimento a cada post usando transformers
for post in data:
    if 'comentário' in post:  # Verifica se a chave 'comentário' existe
        # Substituir emojis antes de análise
        processed_text = replace_emojis(post['comentário'])
        result = sentiment_analysis(processed_text)[0]
        post['sentiment'] = {"label": result['label'], "score": result['score']}
    else:
        post['sentiment'] = None  # Define como None se a chave 'comentário' não existir

# Convertendo os dados novamente para JSON
json_result = json.dumps(data, indent=4, ensure_ascii=False)
print("JSON com Sentimentos:\n", json_result)
# Fechando o navegador
driver.quit()
