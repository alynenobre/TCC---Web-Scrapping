import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import seaborn as sns
import matplotlib.pyplot as plt

from webscrapping.banco.banco import Banco


# ✅ Funções auxiliares
def extrair_score(sentimento):
    try:
        if pd.isnull(sentimento):
            return None
        sentimento = str(sentimento).replace('\n', ' ').strip()
        resultado = re.search(r'score:\s?([0-9]*\.?[0-9]+)', sentimento)
        if resultado:
            return float(resultado.group(1))
        else:
            return None
    except:
        return None


def extrair_label(sentimento):
    try:
        if pd.isnull(sentimento):
            return None
        sentimento = str(sentimento).replace('\n', ' ').strip()
        resultado = re.search(r'label:\s?(\w+)', sentimento)
        if resultado:
            return resultado.group(1)
        else:
            return None
    except:
        return None


# ✅ Pipeline de treino
if __name__ == "__main__":
    conexao_banco = Banco()

    try:
        query = """
            SELECT distinct
                c.url,
                c.perfil,
                c.comentario,
                c.likes AS likes,
                c.sentimento,
                c.data_recolhimento,
                p.likes AS likes_pub 
            FROM public.instagram_comentario AS c
            INNER JOIN public.instagram_publicacao AS p
                ON c.url = p.url
            where p.perfil= 'lulaoficial';
        """
        conexao = conexao_banco.conecta_banco(conexao_banco.database)
        df = pd.read_sql_query(query, conexao)
        conexao.close()

    except Exception as e:
        print(f"Erro na leitura: {e}")

    if df is not None and not df.empty:
        df['sentimento_score'] = df['sentimento'].apply(extrair_score)
        df['sentimento_label'] = df['sentimento'].apply(extrair_label)
        df['sentimento_invertido'] = 1 - df['sentimento_score']
        df = df.dropna(subset=['sentimento_invertido', 'likes_pub'])

        media_likes = df['likes'].mean()
        df['engajamento_alto'] = (df['likes'] >= media_likes).astype(int)

        print(f'Média de likes nos comentários: {media_likes:.2f}')

        X = df[['likes_pub', 'sentimento_invertido']]
        y = df['engajamento_alto']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        sm = SMOTE(random_state=42)
        X_res, y_res = sm.fit_resample(X_train_scaled, y_train)

        modelo = RandomForestClassifier(class_weight='balanced', random_state=42)
        modelo.fit(X_res, y_res)

        y_pred = modelo.predict(X_test_scaled)

        print("\nMatriz de Confusão:")
        print(confusion_matrix(y_test, y_pred))

        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred))
        # Ajusta a fonte da legenda
        leg = plt.legend(prop={
            "family": "serif",  # fonte serifada
            "size": 12
        })

        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
        # Rótulos dos eixos com fonte maior
        plt.xlabel("Classe prevista", fontsize=14)
        plt.ylabel("Classe real", fontsize=14)

        # Ticks dos eixos (nomes das classes) com fonte maior
        plt.xticks(rotation=0, fontsize=12)
        plt.yticks(rotation=0, fontsize=12)

        # Opcional: título com fonte maior
        # plt.title("Matriz de Confusão - Random Forest", fontsize=16)

        # Deixar a barra de cores (colorbar) com fonte maior também
        cbar = plt.gcf().axes[-1]
        cbar.tick_params(labelsize=12)
        plt.show()

        # ✅ Salvar modelo e scaler
        joblib.dump(modelo, 'modelo_engajamento.pkl')
        joblib.dump(scaler, 'scaler.pkl')
        print("Modelo e scaler salvos com sucesso!")
        
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
        sql_create = f"CREATE TABLE IF NOT EXISTS classificação_supervisionada ({campos_sql});"

        conexao_banco.criar_drop_db(sql_create)
        conexao.commit()

        # Inserir os dados do DataFrame no PostgreSQL
        for _, row in df.iterrows():
            values_placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO classificação_supervisionada ({', '.join(colunas)}) VALUES ({values_placeholders});"
            conexao_banco.inserir_db(insert_query, tuple(row))

    else:
        print("Nenhum dado encontrado na consulta.")
