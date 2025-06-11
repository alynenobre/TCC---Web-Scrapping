from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import random, emoji
import json, re
import datetime
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

# Inicializando a pipeline de análise de sentimento com um modelo multilingue que suporta português
sentiment_analysis = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )

class Instagram:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None

    def login(self):
        service = Service(r'C:\Users\alyne.custodio\Documents\GitHub\TCC---Web-Scrapping\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get('https://www.instagram.com')
        sleep(2)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(30)
        
    def publicações_usuarios(self, usuario: str, scrolls: int = 5):
        self.driver.get(f'https://www.instagram.com/{usuario}')
        url_publi = []

        
        # Realiza rolagens para carregar mais posts
        for _ in range(scrolls):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(2)  # Ajuste conforme sua internet

        # Captura todos os links que são posts (contêm /p/)
        links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')

        url_publi = []
        for link in links:
            href = link.get_attribute('href')
            if href and href not in url_publi:
                url_publi.append(href)
                print(href)

        return url_publi
    
    def reels_usuarios(self, usuario: str, scrolls: int = 8):
        # Acessa o perfil
        self.driver.get(f'https://www.instagram.com/{usuario}/')

        sleep(5)  # Tempo para login manual se necessário

        # Realiza rolagens para carregar mais posts
        for _ in range(scrolls):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(2)  # Ajuste conforme sua internet

        # Captura todos os links que são REELS (contêm /reel/)
        links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')

        url_reels = []
        for link in links:
            href = link.get_attribute('href')
            if href and href not in url_reels:
                url_reels.append(href)
        
        resultado = []
        for item in url_reels:
            if item not in resultado:
                resultado.append(item)

        return resultado
    
    def extrair_curtidas(self, texto):
        resultado = re.search(r'([\d\.,]+)\s+curtidas', texto)
        if resultado:
            return int(resultado.group(1).replace('.', '').replace(',', ''))
        return 0
    
    def get_like_geral(self, list_like, perfil_post):
        for item in list_like:
            if item['nome'] == perfil_post:
                return item['likes']
        return 0
    
    def collect_comments(self, post_url: str, user: str):
        self.driver.get(post_url)
        sleep(5)

        while True:
            try:
                load_more = self.driver.find_element(By.XPATH, '//span[contains(text(), "Ver todos os comentários")]')
                load_more.click()
                sleep(2)
            except:
                break
        # Inicializando a lista para armazenar os dados dos comentários
        post_data = []
        list_like = []  # Armazena o comentário atual antes de vir o like
        existing_data = []
        scrollable_div = self.driver.find_element(By.XPATH, '//ul//span')
        for _ in range(1):  # ajuste quantas vezes quiser rolar
            comentarios_divs = self.driver.find_elements(By.XPATH, '//ul//span')

            # Iterando sobre os comentários capturados
            c = len(comentarios_divs)
            for comment in comentarios_divs:
                try:
                    comment_text = comment.text.strip()
                    comment_html = comment.get_attribute("outerHTML")
                    processed_text = replace_emojis(comment_text)
                    result = sentiment_analysis(processed_text)[0]
                    c=c-1
                    print(f"faltam {c}")
                    try:
                        nome = comment.find_element(By.XPATH, ".//a[starts-with(@href, '/') and not(contains(@href, '/p/'))]").text
                    except:
                        pass
                    if nome and comment_text and nome != comment_text:
                        try:
                            curtida_span = comment.find_element(
                                    By.XPATH, ".//span[contains(text(),'curtida')]"
                                )
                            likes_text = curtida_span.text

                            # 🔥 Extrai número, incluindo separador de milhar com ponto
                            match = re.search(r'[\d\.\,]+', likes_text)
                            numero_de_curtida = int(match.group(0).replace('.', '').replace(',', '')) if match else 0
                            list_like.append({"nome":nome, "likes":numero_de_curtida})
                        except:
                            try:
                                # 🥈 Segunda tentativa — pela primeira classe comum
                                curtida_span = comment.find_element(
                                    By.XPATH, './/span[contains(@class, "x193iq5w") and contains(text(),"curtida")]'
                                )
                                likes_text = curtida_span.text
                                # 🔥 Extrai número, incluindo separador de milhar com ponto
                                match = re.search(r'[\d\.\,]+', likes_text)
                                numero_de_curtida = int(match.group(0).replace('.', '').replace(',', '')) if match else 0
                                list_like.append({"nome":nome, "likes":numero_de_curtida})
                            except:
                                try:
                                    # 🥉 Terceira tentativa — pela outra classe alternativa
                                    curtida_span = comment.find_element(
                                        By.XPATH, './/span[contains(@class, "x1lliihq") and contains(text(),"curtida")]'
                                    )
                                    likes_text = curtida_span.text
                                    # 🔥 Extrai número, incluindo separador de milhar com ponto
                                    match = re.search(r'[\d\.\,]+', likes_text)
                                    numero_de_curtida = int(match.group(0).replace('.', '').replace(',', '')) if match else 0
                                    list_like.append({"nome":nome, "likes":numero_de_curtida})
                                except:
                                    try:
                                        curtida_span = comment.find_element(
                                            By.XPATH, ".//preceding::span[contains(text(),'curtida')][1]"
                                        )
                                        likes_text = curtida_span.text
                                        match = re.search(r'[\d\.\,]+', likes_text)
                                        numero_de_curtida = int(match.group(0).replace('.', '').replace(',', '')) if match else 0
                                        list_like.append({"nome":nome, "likes":numero_de_curtida})
                                    except:
                                        # 🔚 Não encontrou nada
                                        numero_de_curtida = 0
                                        list_like.append({"nome":nome, "likes":numero_de_curtida})

                        comment_html = comment.get_attribute("outerHTML")
                        # ✅ Limpeza do texto bruto
                        comment_text_aux = comment_text.strip()
                        # Remove '5 d', '1 d', '2 d', etc.
                        comment_text_aux = re.sub(r"\b\d+\s*d\b", "", comment_text_aux, flags=re.IGNORECASE)
                        comment_text_aux = re.sub(r"\d+\scurtidas", "", comment_text_aux, flags=re.IGNORECASE)
                        comment_text_aux = re.sub(r"Responder" , "", comment_text_aux, flags=re.IGNORECASE)
                        comment_text_aux = re.sub(r"Ver tradução", "", comment_text_aux, flags=re.IGNORECASE)
                        comment_text_aux = re.sub(r"Ver respostas.*", "", comment_text_aux, flags=re.IGNORECASE)
                        comment_text_aux = re.sub(r"\s{2,}", " ", comment_text_aux)  # Remove espaços duplos
                        comment_text_aux = comment_text_aux.strip()

                        # ✅ Condição para só salvar comentários reais
                        if (
                            "Editado" not in comment_text_aux
                            and not re.match(r"^\d+", comment_text_aux.strip())
                            and "Responder" not in comment_text_aux
                            and "Ver tradução" not in comment_text_aux
                            and not re.match(r"Ver respostas\s*\(\d+\)", comment_text_aux, flags=re.IGNORECASE)
                            and comment_text_aux != ""
                        ):
                            processed_text = emoji.demojize(comment_text_aux)
                            result = sentiment_analysis(processed_text)[0]

                            post_data.append({
                                "comentário": comment_text_aux,
                                "html": comment_html,
                                "perfil": nome,
                                "likes": numero_de_curtida,
                                "sentimento": {
                                    "label": result['label'],
                                    "score": result['score']
                                },
                                "data_recolhimento": datetime.datetime.now().isoformat()
                            })
                except Exception as e:
                    print(f"Erro ao processar o comentário: {e}")
                    continue
                
            resultado = []
            like_index = 0
            controle_publicacao = {}
            for post in post_data:
                perfil = post.get('perfil')

                # Se é a primeira vez que vê esse perfil, provavelmente o primeiro like é o da publicação
                if perfil not in controle_publicacao:
                    controle_publicacao[perfil] = 1  # Marca que já viu uma vez e vai pular o primeiro like
                    while like_index < len(list_like):
                        like_item = list_like[like_index]
                        like_index += 1
                        if like_item['nome'] == perfil:
                            # Pula, é o like da publicação
                            break

                # Agora pega o like do comentário
                while like_index < len(list_like):
                    like_item = list_like[like_index]
                    like_index += 1
                    if like_item['nome'] == perfil:
                        post['likes'] = like_item['likes']
                        break

                resultado.append(post)

            existing_data.extend(resultado)
            self.driver.execute_script("arguments[0].scrollTop += 500", scrollable_div)
            sleep(random.randint(1,3))
        likes_geral = self.get_like_geral(list_like, user)    
        with open('instagram_comments_2.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        return existing_data, likes_geral

    def close(self):
        if self.driver:
            self.driver.quit()