import psycopg2
import rede_social.contantes as CONST

class Banco:
    def __init__(self):
        self.database = None

    def conecta_banco(self, database: str):
        try:
            con = psycopg2.connect(
                host='localhost',
                database=database,
                user=CONST.USUARIO_BC,
                password=CONST.SENHA_BC,
                client_encoding='utf8'  # Especifica a codificação como UTF-8
            )
            return con
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None

    def criar_drop_db(self, sql):
        con = self.conecta_banco(self.database)
        if con:
            cur = con.cursor()
            try:
                cur.execute(sql)
                con.commit()
            except psycopg2.Error as e:
                print("Erro ao criar ou excluir banco de dados:", e)
            finally:
                con.close()

    def inserir_db(self, sql):
        con = self.conecta_banco(self.database)
        if con:
            cur = con.cursor()
            try:
                cur.execute(sql)
                con.commit()
            except (psycopg2.Error, UnicodeDecodeError) as e:
                print("Erro ao inserir dados no banco de dados:", e)
                con.rollback()
            finally:
                con.close()
