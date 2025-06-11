import pandas as pd
import re
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

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
                c.url,
                c.perfil,
                c.comentario,
                c.likes AS likes_comentario,
                c.sentimento,
                c.data_recolhimento,
                p.likes AS likes_publicacao
            FROM public.instagram_comentario AS c
            INNER JOIN public.instagram_publicacao AS p
                ON c.url = p.url;
            """
        # Abrindo a conexão corretamente
        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        df = pd.read_sql_query(query, conexao)
        conexao.close()

    except Exception as e:
        print(f"Erro na leitura: {e}")


    if df is not None and not df.empty:
        '''print("Dados lidos com sucesso!")

        # 🎯 Pré-processamento dos dados
        # Extrair o score do sentimento (supondo que o campo sentimento é um JSON/texto do tipo '{"label": "NEGATIVE", "score": 0.88}')

        df['sentimento_score'] = df['sentimento'].apply(extrair_score)
        df['sentimento_label'] = df['sentimento'].apply(extrair_label)
        df['sentimento_invertido'] = 1 - df['sentimento_score']

        # Seleção das features
        features = df[['likes', 'sentimento_invertido']]

        # Normalização
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Clusterização
        kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(scaled_features)

        # PCA para visualização
        pca = PCA(n_components=2)
        components = pca.fit_transform(scaled_features)
        df['pca1'] = components[:, 0]
        df['pca2'] = components[:, 1]

        # 📊 Plot dos clusters
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x="pca1", y="pca2", hue="cluster", style="perfil", s=100)
        plt.title("Clusterização dos Comentários (KMeans)")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.legend(title="Cluster")
        plt.grid(True)
        plt.show()

        # 🗂️ Ver os dados clusterizados
        print(df[['comentario', 'likes', 'sentimento_invertido', 'cluster']])

    else:
        print("Não foram encontrados dados na tabela.")'''
        
        
        # 🎯 Pré-processamento
        df['sentimento_score'] = df['sentimento'].apply(extrair_score)
        df['sentimento_label'] = df['sentimento'].apply(extrair_label)
        df['sentimento_invertido'] = 1 - df['sentimento_score']

        # 🎯 Seleção das features
        features = df[['likes_comentario', 'likes_publicacao', 'sentimento_invertido']]

        # Normalização
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # 🔥 Clusterização
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(scaled_features)

        # 🎨 PCA para visualização
        pca = PCA(n_components=2)
        components = pca.fit_transform(scaled_features)
        df['pca1'] = components[:, 0]
        df['pca2'] = components[:, 1]

        # 📊 Plot dos clusters
        plt.figure(figsize=(10, 7))
        sns.scatterplot(data=df, x="pca1", y="pca2", hue="cluster", style="perfil", s=100)
        plt.title("Clusterização dos Comentários (KMeans) com Likes da Publicação")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.legend(title="Cluster")
        plt.grid(True)
        plt.show()

        # 🗂️ Ver os dados clusterizados
        print(df[['comentario', 'likes_comentario', 'likes_publicacao', 'sentimento_invertido', 'cluster']])
        
        # 💾 Salvar modelo, scaler e pca
        joblib.dump(kmeans, 'modelo_kmeans.pkl')
        joblib.dump(scaler, 'scaler_kmeans.pkl')
        joblib.dump(pca, 'pca_kmeans.pkl')

        print("Modelo KMeans, scaler e PCA salvos com sucesso!")
        
        # Criar a tabela automaticamente com base nas colunas do DataFrame
        colunas = df.columns
        tipos_sql = []

        # Mapeando tipos pandas → SQL
        for col in df.dtypes:
            if pd.api.types.is_integer_dtype(col):
                tipos_sql.append("INTEGER")
            elif pd.api.types.is_float_dtype(col):
                tipos_sql.append("FLOAT")
            elif pd.api.types.is_bool_dtype(col):
                tipos_sql.append("BOOLEAN")
            else:
                tipos_sql.append("TEXT")

        # Criar comando SQL para criar tabela
        conexao_banco = Banco()
        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        campos_sql = ", ".join([f"{col} {tipo}" for col, tipo in zip(colunas, tipos_sql)])
        sql_create = f"CREATE TABLE IF NOT EXISTS KMeans ({campos_sql});"

        conexao_banco.criar_drop_db(sql_create)
        conexao.commit()

        # Inserir os dados do DataFrame no PostgreSQL
        for _, row in df.iterrows():
            values_placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO KMeans ({', '.join(colunas)}) VALUES ({values_placeholders});"
            conexao_banco.inserir_db(insert_query, tuple(row))
        
        
    else:
        print("Não foram encontrados dados na tabela.")