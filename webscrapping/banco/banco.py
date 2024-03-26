import psycopg2
import rede_social.contantes as CONST

def conecta_banco( database:str):
    con = psycopg2.connect(
                         host='localhost', 
                         database=f'{database}',
                         user=f'{CONST.USUARIO_BC}', 
                         password=f'{CONST.SENHA_BC}'
                         )

def  criar_drop_db(sql):
        con = conecta_banco()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

def inserir_db(sql):
    con = conecta_banco()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()