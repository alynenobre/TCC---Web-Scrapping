import requests

url = "https://sterling-cooper-atlas.nomic.ai/api/endpoint"  # Altere para o endpoint desejado
headers = {
    "Authorization": "Bearer nk-...62sS8"  # Substitua pela sua chave da API
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Login bem-sucedido!")
    data = response.json()
    print(data)
else:
    print(f"Erro: {response.status_code} - {response.text}")