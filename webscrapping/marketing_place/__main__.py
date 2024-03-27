# PIP
import os
import sys
from random import shuffle
import pandas as pd
from typing import Union, Dict, List, Tuple, Callable
from datetime import datetime
import json
sys.path.append(r'C:\Users\alyne.custodio\Documents\GitHub\TCC---Web-Scrapping\webscrapping')



# Dux
from marketing_place.mercadolivre import MercadoLivre
from marketing_place.amazon import Amazon
from marketing_place.browser import BrowserSoucer
from banco import banco


if __name__ == '__main__':
    # Criando uma instância de MercadoLivre
    mercado_livre = MercadoLivre()
    amazon = Amazon()
    banco = banco.Banco()
    # Connect with the DuxDataLake
    

    # Parâmetros para a pesquisa
    product_offering_links_per_page = []
    dux_dlh = BrowserSoucer()
    product = 'Creatina Monohidratada 100g'  # Substitua com o nome do seu produto
    max_pages = 5  # Número máximo de páginas para pesquisar
    banco.conecta_banco(database='marketing_place')

    # Chamando o método get_product
    amazon.get_link_product(dux_dlh, product, max_pages)
    amazon = amazon.get_link_seller(dux_dlh,max_pages)
    amazon = json.dumps(amazon)
    data = json.loads(amazon)
    df = pd.DataFrame(data)
    banco.conecta_banco(database='marketing_place')
    for i in df.index:
        sql = """
        INSERT into public.amazon (marketplace_site, datetime, range_hour, page, link, link_number, content, seller_link) 
        values('%s','%s','%s','%s','%s','%s','%s','%s');
        """ % (df['marketplace_site'][i],df['datetime'][i],df['range_hour'][i],df['page'][i],
                df['link'][i],df['link_number'][i],df['content'][i],df['seller_link'][i])
        banco.inserir_db(sql)

    mercado_livre = mercado_livre.get_link_seller(dux_dlh,max_pages)
    # Convertendo o DataFrame para JSON
    mercado_livre_json = json.dumps(mercado_livre)
    df = pd.DataFrame(mercado_livre_json)
    banco.conecta_banco(database='marketing_place')
    for i in df.index:
        sql = """
        INSERT into public.mercado_livre (marketplace_site, datetime, range_hour, page, link, link_number, content, seller_link) 
        values('%s','%s','%s','%s','%s','%s','%s','%s');
        """ % (df['marketplace_site'][i],df['datetime'][i],df['range_hour'][i],df['page'][i],
                df['link'][i],df['link_number'][i],df['content'][i],df['seller_link'][i])
        banco.inserir_db(sql)

