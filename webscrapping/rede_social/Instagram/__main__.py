import json
import pandas as pd
import sys
sys.path.append(r'C:\Users\alyne.custodio\Documents\GitHub\TCC---Web-Scrapping\webscrapping')

# Pacotes
from rede_social.Instagram.Instagram import Instagram
import rede_social.contantes as CONST
from banco import banco

if __name__ == "__main__":
    # Instanciando a classe Instagram
    instagram_bot = Instagram()

    # Substitua 'seu_usuario' e 'sua_senha' pelo seu nome de usuário e senha do Instagram
    instagram_bot.login(username=f'{CONST.EMAIL}', password=f'{CONST.SENHA}')

    resultado = instagram_bot.get_post_hashtag(hashtag='casadedeusoficial')
    
    df = pd.DataFrame(resultado)
    for col in df.columns:
        df[col] = df[col].apply(str)

    # Conectando ao banco de dados
    conexao_banco = banco.Banco()
    conexao_banco.conecta_banco(database="rede_social")
    # SQL para criar a tabela 'instagram' no esquema 'public'
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS public.instagram (
        id SERIAL PRIMARY KEY,
        hashtag VARCHAR(255) NOT NULL,
        image_url TEXT NOT NULL,
        likes TEXT NOT NULL,
        data_execution TIMESTAMP NOT NULL
    );
    """

    # Criar a tabela 'instagram' no esquema 'public'
    conexao_banco.criar_drop_db(sql_create_table)
    
    # Inserindo os dados no banco de dados
    for i in df.index:
        sql = """
        INSERT INTO public.instagram (hashtag, image_url, likes, data_execution) 
        VALUES ('%s', '%s', '%s', '%s');
        """ % (df['hashtag'][i], df['image_url'][i], df['likes'][i], df['data_execution'][i])
        conexao_banco.inserir_db(sql)
