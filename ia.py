import openai
import openai.error 
from openai import OpenAI

openai.api_key = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Qual é o modelo ideal para o GPT Plus?"}
        ]
    )
print(response["choices"][0]["message"]["content"])
