import requests

url = "https://atlas.nomic.ai/data/alynenobre/org/keys"  # Altere para o endpoint desejado
headers = {
    "Authorization": "Bearer nk-...62sS8"  # Substitua pela sua chave da API
}
response = requests.get(url, headers=headers)

print("Código de status:", response.status_code)
print("Conteúdo da resposta:", response.text)  # Imprime o conteúdo da resposta
