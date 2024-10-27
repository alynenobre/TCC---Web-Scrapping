import requests

url = "https://atlas.nomic.ai/data/alynenobre/org/keys"  # Altere para o endpoint desejado
headers = {
    "Authorization": "Bearer nk-...62sS8"  # Substitua pela sua chave da API
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Login bem-sucedido!")
    print("Conteúdo da resposta:", response.text)  # Imprime o conteúdo da resposta
    try:
        data = response.json()
        print(data)
    except ValueError as e:
        print(f"Erro ao decodificar JSON: {e}")
else:
    print(f"Erro: {response.status_code} - {response.text}")
