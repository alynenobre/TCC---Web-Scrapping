import nomic

try:
        token = "nk-...62sS8"  # Substitua pela sua chave da API
        nomic.cli.login(token, tenant="production")
        print("Login realizado com sucesso!")
except Exception as e:
        print(f"Erro ao realizar login: {e}")