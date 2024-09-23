# PIP
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import time
from langdetect import detect
import datetime
import re

# Pacotes
from rede_social.browser import Browser
import rede_social.contantes as CONST

class Instagram:
    def __init__(self):
        self.browser = None

    def login(self, username: str, password: str):
        self.username = username
        self.password = password
        self.browser = Browser(api_name="INSTAGRAM").open_browser()
        self.browser.get('https://www.instagram.com/')

        # Login da rede social
        self.username_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        self.password_input = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        self.username_input.send_keys(username)
        time.sleep(2)
        self.password_input.send_keys(password)
        time.sleep(2)
        self.password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        9,time.sleep(2)

    def click_more_comments(self):
        timeout = 10  # in seconds
        while True:
            try:
                button = WebDriverWait(self.browser, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".x9f619.xjbqb8w.x78zum5"))
                )
                button.click()
                time.sleep(2)
            except NoSuchElementException:
                break
            except ElementNotVisibleException:
                time.sleep(2)
                continue
            except Exception as e:
                print(f"Exception occurred: {e}")
                break

    def get_comments(self, url_post: str):
        self.browser.get(url_post)
        time.sleep(2)
        
        #self.click_more_comments()
        
        plain_html = self.browser.page_source
        soup = bs(plain_html, 'html.parser')
        comments_elements = soup.find_all('ul', {'class': 'Mr508'})
        
        all_comments = []
        for element in comments_elements:
            try:
                user = element.find('a', {'class': 'sqdOP'}).text
                comment = element.find('span').text
                all_comments.append({"user": user, "comment": comment, "post_url": url_post})
            except AttributeError:
                continue
        
        return all_comments


    def get_post_hashtag(self, hashtag: str):
        if self.browser is None:
            print("Você precisa fazer login primeiro.")
            return []

        self.browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        post_data = []

        for _ in range(5):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            elements_xpath1 = self.browser.find_elements(By.CSS_SELECTOR, 'article > div > div:nth-child(2)')
            
            for post in elements_xpath1:
                img_element = post.find_element(By.CLASS_NAME, '_aagv')
                image_url = img_element.get_attribute('src')

                link_element = post.find_element(By.CLASS_NAME, '_a6hd')
                url = link_element.get_attribute('href')

                self.browser.get(f'{url}')
                time.sleep(2)  # Aguarde a página carregar após clicar no post
                
                likes_element = self.browser.find_element(By.XPATH, "//*[contains(text(),'curtidas')]")
                likes = likes_element.text

                likes = re.findall(r'\d+', likes)
                likes = likes[0]

                comments = self.get_comments(url)

                post_data.append({
                    "hashtag": hashtag,
                    "image_url": image_url,
                    "likes": likes,
                    "url": url, 
                    "comments": comments,
                    "data_execution": datetime.datetime.now().isoformat()
                })

                self.browser.execute_script("window.history.go(-1)")
                time.sleep(2)  # Aguarde a página voltar antes de continuar

        return post_data