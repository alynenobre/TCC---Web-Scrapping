import pandas as pd
import re
import joblib
from matplotlib import rcParams
import seaborn as sns
import matplotlib.pyplot as plt

from webscrapping.banco.banco import Banco


# ✅ Funções auxiliares
def extrair_score(sentimento):
    try:
        if pd.isnull(sentimento):
            return None
        sentimento = str(sentimento).replace("\n", " ").strip()
        resultado = re.search(r"score:\s?([0-9]*\.?[0-9]+)", sentimento)
        if resultado:
            return float(resultado.group(1))
        return None
    except Exception:
        return None


def extrair_label(sentimento):
    try:
        if pd.isnull(sentimento):
            return None
        sentimento = str(sentimento).replace("\n", " ").strip()
        resultado = re.search(r"label:\s?(\w+)", sentimento)
        if resultado:
            return resultado.group(1)
        return None
    except Exception:
        return None


# ✅ Pipeline de inferência
if __name__ == "__main__":
    conexao_banco = Banco()

    try:
        query = """
            SELECT DISTINCT
                c.url,
                c.perfil AS comentador,
                c.comentario,
                c.likes AS likes_comentario,
                c.sentimento,
                c.data_recolhimento,
                p.likes AS likes_publicacao,
                p.perfil AS publicador
            FROM public.instagram_comentario AS c
            INNER JOIN public.instagram_publicacao AS p
                ON c.url = p.url
            WHERE p.perfil = 'eduardopaes';
        """
        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        df = pd.read_sql_query(query, conexao)
        conexao.close()
    except Exception as e:
        print(f"Erro na leitura: {e}")
        df = None

    if df is not None and not df.empty:
        # ✅ Carregar o modelo, scaler e PCA salvos (treinados no outro script)
        kmeans = joblib.load("modelo_kmeans.pkl")
        scaler = joblib.load("scaler_kmeans.pkl")
        pca = joblib.load("pca_kmeans.pkl")

        # ✅ Pré-processamento igual ao treino
        df["sentimento_score"] = df["sentimento"].apply(extrair_score)
        df["sentimento_label"] = df["sentimento"].apply(extrair_label)
        df["sentimento_invertido"] = 1 - df["sentimento_score"]

        # Remove linhas com NaN nas features usadas
        df = df.dropna(subset=["likes_comentario", "likes_publicacao", "sentimento_invertido"])

        # ✅ Seleção das features
        X = df[["likes_comentario", "likes_publicacao", "sentimento_invertido"]]

        # ✅ Aplicar o mesmo scaler
        X_scaled = scaler.transform(X)
        
        # ✅ Redução PCA para visualização
        components = pca.transform(X_scaled)

        # ✅ Predição dos clusters
        clusters = kmeans.predict(components)

        # ✅ Adicionar resultados no DataFrame
        df["pca1"] = components[:, 0]
        df["pca2"] = components[:, 1]
        df["cluster"] = clusters

        # ✅ Mostrar os resultados
        print(
            df[
                [
                    "comentario",
                    "likes_comentario",
                    "likes_publicacao",
                    "sentimento_invertido",
                    "cluster",
                ]
            ]
        )

        # 👉 Configuração global de fonte (tudo maior, sem LaTeX)
        rcParams.update(
            {
                "text.usetex": False,
                "font.family": "serif",
                "font.size": 14,        # base
                "axes.titlesize": 16,
                "axes.labelsize": 14,
                "xtick.labelsize": 12,
                "ytick.labelsize": 12,
                "legend.fontsize": 12,
                "mathtext.fontset": "cm",
            }
        )

        # 📊 Plot dos clusters
        plt.figure(figsize=(10, 7))
        sns.scatterplot(
            data=df,
            x="pca1",
            y="pca2",
            hue="cluster",
            s=100,
        )

        # plt.title("Clusterização dos Comentários (KMeans) com Likes da Publicação")
        plt.xlabel("Componente Principal 1", fontsize=14)
        plt.ylabel("Componente Principal 2", fontsize=14)

        # Ticks com fonte maior
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # Legenda com fonte maior
        plt.legend(
            title="Cluster",
            loc="best",
            title_fontsize=13,
            fontsize=12,
        )

        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # ✅ Salvar resultado como CSV
        df.to_csv("resultado_kmeans_teste.csv", index=False)
        print("\nResultado salvo como 'resultado_kmeans_teste.csv'")

        # =====================================
        # 🔻 Persistência no PostgreSQL (kmeans)
        # =====================================
        # Tipagem SQL com base nos dtypes
        tipos_sql = []
        for tipo in df.dtypes:
            if pd.api.types.is_integer_dtype(tipo):
                tipos_sql.append("INTEGER")
            elif pd.api.types.is_float_dtype(tipo):
                tipos_sql.append("FLOAT")
            elif pd.api.types.is_bool_dtype(tipo):
                tipos_sql.append("BOOLEAN")
            else:
                tipos_sql.append("TEXT")

        conexao_banco = Banco()
        conexao = conexao_banco.conecta_banco(conexao_banco.database)

        # Lista de colunas da tabela e as correspondentes no DataFrame
        colunas_tabela = [
            "url",
            "perfil",
            "comentario",
            "likes_comentario",
            "sentimento",
            "data_recolhimento",
            "likes_publicacao",
            "sentimento_score",
            "sentimento_label",
            "sentimento_invertido",
            "cluster",
            "pca1",
            "pca2",
        ]

        colunas_df = [
            "url",
            "comentador",
            "comentario",
            "likes_comentario",
            "sentimento",
            "data_recolhimento",
            "likes_publicacao",
            "sentimento_score",
            "sentimento_label",
            "sentimento_invertido",
            "cluster",
            "pca1",
            "pca2",
        ]

        # Monte o SQL fora do loop
        placeholders = ", ".join(["%s"] * len(colunas_tabela))
        colunas_sql = ", ".join(colunas_tabela)
        sql = f"INSERT INTO public.kmeans ({colunas_sql}) VALUES ({placeholders});"

        # Tratar NaNs para None
        df = df.where(pd.notnull(df), None)

        # Inserir no banco
        for _, row in df.iterrows():
            valores = tuple(row[col] for col in colunas_df)
            conexao_banco.inserir_db(sql, valores)

        conexao.close()

    else:
        print("Nenhum dado encontrado na consulta.")
