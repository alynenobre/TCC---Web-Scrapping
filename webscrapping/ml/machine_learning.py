import pandas as pd
import re
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

from webscrapping.banco.banco import Banco



def extrair_score(sentimento):
    try:
        # Expressão regular para capturar o número após "score:"
        resultado = re.search(r'score:\s?([0-9.]+)', sentimento)
        if resultado:
            return float(resultado.group(1))
        else:
            return None
    except:
        return None

def extrair_label(sentimento):
    try:
        resultado = re.search(r'label:\s?(\w+)', sentimento)
        if resultado:
            return resultado.group(1)
        else:
            return None
    except:
        return None


if __name__ == "__main__":
    conexao_banco = Banco()
    
    try:
        query = """
            SELECT 
                c.comentario,
                c.likes AS likes_comentario ,
                p.likes AS likes_publicacao,
                p.perfil as publicador
            FROM public.instagram_comentario AS c
            INNER JOIN public.instagram_publicacao AS p
                ON c.url = p.url
            where p.perfil= 'lulaoficial'
            """
        # Abrindo a conexão corretamente
        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        df = pd.read_sql_query(query, conexao)
        conexao.close()

    except Exception as e:
        print(f"Erro na leitura: {e}")


    if df is not None and not df.empty:
        # (Para português, HuggingFace tem modelos multilingues e alguns específicos)
        analisador = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        
        # ✅ Fazer a análise
        comentarios = df['comentario'].dropna().astype(str).tolist()
        resultados = analisador(comentarios)

        # ✅ Visualizar os resultados
        df_resultado = pd.DataFrame({
            'comentario': comentarios,
            'label': [r['label'] for r in resultados],
            'score': [r['score'] for r in resultados]
        })


        df_final = df[['comentario', 'likes_comentario', 'likes_publicacao', 'publicador']].dropna(subset=['comentario']).copy()
        df_final['comentario'] = df_final['comentario'].astype(str).tolist()
        df_final = df_final.iloc[:len(resultados)]  # garantir alinhamento
        df_final['sentimento_label'] = [r['label'] for r in resultados]
        df_final['sentimento_score'] = [r['score'] for r in resultados]

        print(df_final.head())

        
        
    else:
        print("Não foram encontrados dados na tabela.")