import pandas as pd
import psycopg2
from webscrapping.banco import banco


caminho = 'instagram_comments_2.json'
post_url = 'https://www.instagram.com/p/DI1-rOrx7Tl/'

conexao_banco = banco.Banco()

# Lê e transforma em DataFrame
df = pd.read_json(caminho)

sql = """
    INSERT INTO public.instagram_analise_nl (url, html, sentimento, comentario, perfil, likes, data_recolhimento)
    VALUES (%s,%s, %s, %s, %s, %s, %s)
    ON CONFLICT (html) DO NOTHING;
    """
    
for i in df.index:
        sentimento_dict = df['sentimento'][i]
        sentimento_str = f"sentimento: {sentimento_dict}".replace("'", "")
        valores = (
            post_url,
            df['html'][i],
            sentimento_str,
            df['comentário'][i],
            df['perfil'][i],
            int(df['likes'][i]),
            df['data_recolhimento'][i]
        )
        try:
            conexao_banco.inserir_db(sql, valores)
        except Exception as e:
            print(f"Erro ao inserir dados no banco de dados: {e}")