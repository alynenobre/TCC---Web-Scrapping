# STDLib
from random import shuffle
from datetime import datetime
from typing import Dict, List, Any

# DUX
from dux_datalake import DuxDatalake

# PIP
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dux_modules.webscraping.bronze.browser import BrowserSoucer
import dux_modules.webscraping.bronze.constants  as const




class Amazon(BrowserSoucer):
    def __init__(self) -> None:
        self.product_offering_links_per_page = []
        self.search_pages = []

    def get_link_product(self, dux_dlh:BrowserSoucer, product:str, max_pages:int):
        clean_product_name = product.strip().lower().replace(' ', '-') # cleaning[product]
        search_pages = self.search_pages
        result_list = []
        with dux_dlh.get_driver() as navegador:

            for page in range(max_pages):
                desde = sum(len(i) for i in self.product_offering_links_per_page)
                if desde == 0: 
                    desde = ''
                else: 
                    desde = f'_Desde_{desde+1}'

                # Make the link of the SEARCH of the product
                search_link = const.marketplace["amazon"]+clean_product_name +desde+f'_OrderId_PRICE_NoIndex_True#D[A:Dux%20Nutrition%20'+product.strip().replace(' ', '%20')+']'

                # Log the first link
                #if desde == '':
                #    print('\t', search_link)

                # Get the search page, that has a list of product postings
                navegador.get(search_link)
                dux_dlh.randwait(12,18)  # Wait to avoid blocking and let the browser load the page
                navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
                dux_dlh.randwait(1,3)
                html_search_page = navegador.page_source  # FULL HTML OF THE SEARCH PAGE
                search_pages.append(html_search_page)  # Store the search page

                # XPath 1
                xpath1 = '//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]'

                # XPath 2
                #xpath2 = '//*[@id=":R459b9:"]/div[2]/div[1]/a[1]'

                # Lista para armazenar os links
                links = []

                # XPath 1
                elements_xpath1 = navegador.find_elements(By.XPATH, xpath1)

                # XPath 2
                #elements_xpath2 = navegador.find_elements(By.XPATH, xpath2)
                links_xpath1 = [elem.get_attribute('href') for elem in elements_xpath1] 
                #+ [elem.get_attribute('href') for elem in  elements_xpath2]
                links.extend(links_xpath1)

                # Filter the links in the search page - we only want product offering links. So we must remove the rest
                links = [l for l in links if l is not None]
                links = [str(l) for l in links if all([
                        l.startswith('https://www.amazon.com.br/'),
                        'dux' in l or 'DUX' in l or 'Dux' in l,
                        len(l) > len('https://www.amazon.com.br/')
                    ])]
                # Store only the links we want, that point at products offerings
                self.product_offering_links_per_page.append(links)  # LIST OF LIST OF LINKS

                result = {
                    'product_offering_links_per_page': links,
                    'html_search_page': html_search_page
                }
                result_list.append(result)

        #return result_list
    
    
    def get_link_seller(self, dux_dlh:BrowserSoucer, max_pages:int):
        # For each link, get its content and save its metadata
        retrieved_links = set()
        retrieved_pages = []
        sellers_cache = {}
        result_list=[]

        with dux_dlh.get_driver() as navegador:
            for page, all_links_in_page in enumerate(self.product_offering_links_per_page):
                for link_product_offering in all_links_in_page[:10]:
                    # Get the product offfering page
                    navegador.get(link_product_offering)
                    dux_dlh.randwait(12,18)  # Wait to avoid blocking and let the browser load the page
                    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
                    dux_dlh.randwait(1,3)
                    html_product_offering_page_link = navegador.page_source

                    # XPath 1
                    xpath1 = '//*[@id="merchantInfoFeature_feature_div"]/div[2]/div/span'
                    xpath2 = '//*[@class="a-size-small offer-display-feature-text-message"]'

                    # Lista para armazenar os links
                    links = []

                    # XPath 1
                    elements_xpath1 = navegador.find_elements(By.XPATH, xpath1)
                    elements_xpath2 = navegador.find_elements(By.XPATH, xpath2)

                    links_xpath = [elem.get_attribute('href') for elem in elements_xpath1] + [elem.get_attribute('href') for elem in  elements_xpath2]
                    links.extend(links_xpath)

                    links = [l for l in links if l is not None]

                    # Add metadata and append to the buffer
                
                    hour = datetime.now().hour

                    result = {
                        'marketplace_site': "Amazon",
                        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'range_hour': 'Manhã' if 6 <= hour < 12
                                            else ('Tarde' if 12 <= hour < 18
                                                            else ('Noite' if 18 <= hour
                                                                        else 'Madrugada')),
                        'page': page,
                        'link': link_product_offering,
                        'link_number': len(retrieved_links),
                        'content': html_product_offering_page_link,
                        'seller_link': links
                    }
                    result_list.append(result)

        return result_list