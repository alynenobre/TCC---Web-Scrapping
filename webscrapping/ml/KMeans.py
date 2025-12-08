import pandas as pd
import re
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

from webscrapping.banco.banco import Banco


def extrair_score(sentimento):
    try:
        # Expressão regular para capturar o número após "score:"
        resultado = re.search(r'score:\s?([0-9.]+)', str(sentimento))
        if resultado:
            return float(resultado.group(1))
        else:
            return None
    except Exception:
        return None


def extrair_label(sentimento):
    try:
        resultado = re.search(r'label:\s?(\w+)', str(sentimento))
        if resultado:
            return resultado.group(1)
        else:
            return None
    except Exception:
        return None


if __name__ == "__main__":
    conexao_banco = Banco()

    try:
        query = """
            SELECT DISTINCT
                c.url,
                c.perfil,
                c.comentario,
                c.likes AS likes_comentario,
                c.sentimento,
                c.data_recolhimento,
                p.likes AS likes_publicacao
            FROM public.instagram_comentario AS c
            INNER JOIN public.instagram_publicacao AS p
                ON c.url = p.url
            WHERE p.perfil = 'lulaoficial';
        """

        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        df = pd.read_sql_query(query, conexao)
        conexao.close()

    except Exception as e:
        print(f"Erro na leitura: {e}")
        df = None

    if df is not None and not df.empty:

        # 🎯 Pré-processamento
        df["sentimento_score"] = df["sentimento"].apply(extrair_score)
        df["sentimento_label"] = df["sentimento"].apply(extrair_label)
        df["sentimento_invertido"] = 1 - df["sentimento_score"]

        # Remove linhas com NaN nas features principais
        df = df.dropna(subset=["likes_comentario", "likes_publicacao", "sentimento_invertido"])

        # 🎯 Seleção das features
        features = df[["likes_comentario", "likes_publicacao", "sentimento_invertido"]]

        # Normalização
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # 🎨 PCA para visualização
        pca = PCA(n_components=2)
        components = pca.fit_transform(scaled_features)
        df["pca1"] = components[:, 0]
        df["pca2"] = components[:, 1]


        # 🔥 Clusterização (KMeans)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df["cluster"] = kmeans.fit_predict(components)

        
        # 👉 Configuração de fonte (tudo maior e sem LaTeX)
        rcParams.update({
            "text.usetex": False,       # desliga LaTeX
            "font.family": "serif",
            "font.size": 14,            # fonte base
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "mathtext.fontset": "cm",
        })

        # 📊 Plot dos clusters
        plt.figure(figsize=(10, 7))

        sns.scatterplot(
            data=df,
            x="pca1",
            y="pca2",
            hue="cluster",
            s=80,
            alpha=0.8,
            
        )

        # plt.title("Clusterização dos Comentários (KMeans) com Likes da Publicação")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")

        # Ticks com fonte maior
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # Legenda com fonte maior
        plt.legend(
            title="Cluster",
            loc="best",
            title_fontsize=13,
            fontsize=12
        )

        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 🗂️ Ver os dados clusterizados (opcional)
        print(df[[
            "comentario",
            "likes_comentario",
            "likes_publicacao",
            "sentimento_invertido",
            "cluster"
        ]])

        # 💾 Salvar modelo, scaler e PCA
        joblib.dump(kmeans, "modelo_kmeans.pkl")
        joblib.dump(scaler, "scaler_kmeans.pkl")
        joblib.dump(pca, "pca_kmeans.pkl")

        print("Modelo KMeans, scaler e PCA salvos com sucesso!")

        # ============================
        # 🔻 Persistência no PostgreSQL
        # ============================
        colunas = df.columns
        tipos_sql = []

        # Mapeando tipos pandas → SQL
        for tipo in df.dtypes:
            if pd.api.types.is_integer_dtype(tipo):
                tipos_sql.append("INTEGER")
            elif pd.api.types.is_float_dtype(tipo):
                tipos_sql.append("FLOAT")
            elif pd.api.types.is_bool_dtype(tipo):
                tipos_sql.append("BOOLEAN")
            else:
                tipos_sql.append("TEXT")

        # Criar comando SQL para criar tabela
        conexao_banco = Banco()
        conexao = conexao_banco.conecta_banco(conexao_banco.database)

        campos_sql = ", ".join(
            [f"{col} {tipo}" for col, tipo in zip(colunas, tipos_sql)]
        )
        sql_create = f"CREATE TABLE IF NOT EXISTS KMeans ({campos_sql});"

        conexao_banco.criar_drop_db(sql_create)
        conexao.commit()

        # Inserir os dados do DataFrame no PostgreSQL
        for _, row in df.iterrows():
            values_placeholders = ", ".join(["%s"] * len(row))
            insert_query = (
                f"INSERT INTO KMeans ({', '.join(colunas)}) "
                f"VALUES ({values_placeholders});"
            )
            conexao_banco.inserir_db(insert_query, tuple(row))

        conexao.close()

    else:
        print("Não foram encontrados dados na tabela.")
