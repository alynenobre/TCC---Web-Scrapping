import requests

url = "https://sterling-cooper-atlas.nomic.ai/api/endpoint"  # Altere para o endpoint desejado
headers = {
    "Authorization": "Bearer nk-...62sS8"  # Substitua pela sua chave da API
}
response = requests.get(url, headers=headers)

# Verifique o status da resposta
print(f"Status Code: {response.status_code}")
print("Response Text:", response.text)  # Imprima o conteúdo da resposta

if response.status_code == 200:
    print("Login bem-sucedido!")
    try:
        data = response.json()  # Tente converter para JSON
        print(data)
    except ValueError:
        print("Erro ao decodificar a resposta como JSON.")
else:
    print(f"Erro: {response.status_code} - {response.text}")
