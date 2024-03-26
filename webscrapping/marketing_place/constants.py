# PIP
from random import shuffle


STORE_SAMPLES = False



marketplace = {
    'amazon': "https://amazon.com.br/s?k=Dux+Nutrition+",
    'mercado_livre': "https://lista.mercadolivre.com.br/dux-nutrition-",
    'shopee': "https://shopee.com.br/search?keyword=dux%20nutrition"
}


cleaning = {
    'Whey Protein Concentrado 900g': 'whey 9',
    'Whey Protein Concentrado 1,8kg': 'whey 8',
    'Whey Protein Isolado 900g': 'whey 9',
    'Whey Protein Isolado 1,8kg': 'whey 8',
    'Fresh Whey 900g': 'fresh 9',
    'Energy Kick 1kg': 'energy 1',
}


category = [
        'Whey Protein Concentrado 900g',
        'Whey Protein Concentrado 1,8kg',
        'Whey Protein Isolado 900g',
        'Whey Protein Isolado 1,8kg',
        'Fresh Whey 900g',
        'Energy Kick 1kg',
        'Fresh Whey Sachê',
        'Glutamina 100g',
        'Multivitamínico 30 Cápsulas',
        'Whey Protein Concentrado Sachê',
        'Whey Protein Concentrado 450g',
        'Whey Protein Isolado Sachê',
        'Whey Protein Isolado 450g',
        'Whey Protein Shake 250ml',
        'Energy Kick Sachê',
        'Creatina Monohidratada 100g',
        'Creatina Monohidratada 300g'
    ]

shuffle(category)