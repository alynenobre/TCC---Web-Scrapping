from rede_social.Instagram.Instagram import Instagram
import rede_social.contantes as CONST

if __name__ == "__main__":
    # Instanciando a classe Instagram
    instagram_bot = Instagram()

    # Substitua 'seu_usuario' e 'sua_senha' pelo seu nome de usuário e senha do Instagram
    instagram_bot.login(username=f'{CONST.EMAIL}', password=f'{CONST.SENHA}', hastag="casadedeusoficial")
