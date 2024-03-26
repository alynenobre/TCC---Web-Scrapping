import json
import pandas as pd
#Pacotes
from rede_social.Instagram.Instagram import Instagram
import rede_social.contantes as CONST
import banco as BD

if __name__ == "__main__":
    # Instanciando a classe Instagram
    instagram_bot = Instagram()

    # Substitua 'seu_usuario' e 'sua_senha' pelo seu nome de usuário e senha do Instagram
    instagram_bot.login(username=f'{CONST.EMAIL}', password=f'{CONST.SENHA}')

    resultado = instagram_bot.get_post_hashtag(hashtag='casadedeusoficial')
    data = json.loads(resultado)
    df = pd.DataFrame(data)
    for col in df.columns:
        df[col] = df[col].apply(str)

    BD.conecta_banco("rede_social")
    for i in df.index:
        sql = """
        INSERT into public.instagram (hashtag,image_url,likes,data_execution) 
        values('%s','%s','%s','%s');
        """ % (df['hashtag'][i], df['image_url'][i], df['likes'][i], df['data_execution'][i])
        BD.inserir_db(sql)