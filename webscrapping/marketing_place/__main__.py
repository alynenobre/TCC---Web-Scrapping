# PIP
import os
from random import shuffle
import pandas as pd
from typing import Union, Dict, List, Tuple, Callable
from datetime import datetime
import json

# Dux
from marketing_place.mercadolivre import MercadoLivre
from marketing_place.amazon import Amazon
from marketing_place.browser import BrowserSoucer


if __name__ == '__main__':
    # Criando uma instância de MercadoLivre
    mercado_livre = MercadoLivre()
    amazon = Amazon()
    # Connect with the DuxDataLake
    

    # Parâmetros para a pesquisa
    product_offering_links_per_page = []
    dux_dlh = BrowserSoucer()
    product = 'Creatina Monohidratada 100g'  # Substitua com o nome do seu produto
    max_pages = 5  # Número máximo de páginas para pesquisar

    # Chamando o método get_product
    amazon.get_link_product(dux_dlh, product, max_pages)
    amazon = amazon.get_link_seller(dux_dlh,max_pages)
    amazon = json.dumps(amazon)
    mercado_livre = mercado_livre.get_link_seller(dux_dlh,max_pages)
    # Convertendo o DataFrame para JSON
    mercado_livre_json = json.dumps(mercado_livre)
