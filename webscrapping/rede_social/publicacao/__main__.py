import datetime
import pandas as pd
from webscrapping.banco import banco

# Pacotes
from webscrapping.rede_social.Instagram_v2.Instagram import Instagram
import webscrapping.rede_social.contantes as CONST
from webscrapping.banco import banco

if __name__ == "__main__":
    username = CONST.EMAIL
    password = CONST.SENHA
    perfil_geral = 'lulaoficial'

    instagram_bot = Instagram(username, password)
    instagram_bot.login()    
    list_pub = instagram_bot.publicações_usuarios(perfil_geral)
    
    for url in list_pub:
        resultado, likes_geral = instagram_bot.collect_comments(url, perfil_geral)

        df = pd.DataFrame(resultado)
        for col in df.columns:
            df[col] = df[col].apply(str)

        df = pd.DataFrame(resultado)
        df['likes'] = df['likes'].astype(int)

        conexao_banco = banco.Banco()
        conexao_banco.conecta_banco(database="rede_social")

        sql_create_table = """
        CREATE TABLE IF NOT EXISTS public.instagram_comentario (
            url TEXT NOT NuLL,
            html TEXT PRIMARY KEY,
            sentimento TEXT NOT NULL,
            comentario TEXT NOT NULL,
            perfil TEXT NOT NULL,
            likes INT NOT NULL,
            data_recolhimento TIMESTAMP NOT NULL
        );
        """
        conexao_banco.criar_drop_db(sql_create_table)

        sql = """
        INSERT INTO public.instagram_comentario (url, html, sentimento, comentario, perfil, likes, data_recolhimento)
        VALUES (%s,%s, %s, %s, %s, %s, %s)
        ON CONFLICT (html) DO NOTHING;
        """

        for i in df.index:
            sentimento_dict = df['sentimento'][i]
            sentimento_str = f"sentimento: {sentimento_dict}".replace("'", "")
            valores = (
                url,
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
                
        
        create_table_publicacao = """
            CREATE TABLE IF NOT EXISTS public.instagram_publicacao (
                url TEXT NOT NULL,
                perfil TEXT NOT NULL,
                likes INT NOT NULL,
                data_recolhimento TIMESTAMP NOT NULL,
                PRIMARY KEY (url)
            );
        """
        conexao_banco.criar_drop_db(create_table_publicacao)

        sql = """
            INSERT INTO public.instagram_publicacao (url, perfil, likes, data_recolhimento)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) 
            DO UPDATE SET 
                likes = EXCLUDED.likes,
                data_recolhimento = EXCLUDED.data_recolhimento;
        """
        valores = (
            url,
            perfil_geral,
            likes_geral,
            datetime.datetime.now().isoformat()
        )

        try:
            conexao_banco.inserir_db(sql, valores)
        except Exception as e:
            print(f"Erro ao inserir dados no banco de dados: {e}")

    instagram_bot.close()