# TCC - Web Scrapping

Descrição
- Projeto de TCC para coleta e análise de dados de redes sociais via web scraping, com pipeline de coleta, armazenamento, pré-processamento e aplicação de modelos de Machine Learning (ex.: K-Means e modelos de engajamento).
- Contém código Python, modelos serializados (.pkl), dados de exemplo (.csv / .json) e arquivos auxiliares (ex.: chromedriver, licenças).

Avisos importantes
- O arquivo `ia.py` no repositório contém uma chave de API embutida. Se essa chave for real, revogue-a imediatamente e gere uma nova. Nunca deixe chaves ou credenciais no código-fonte.
- Recomenda-se não versionar binários (ex.: `chromedriver.exe`). Use gerenciadores (webdriver-manager) ou Git LFS quando necessário.

Estrutura principal do repositório
- ia.py — script de demonstração de uso de API (contém chave hardcoded — remover).
- chromedriver.exe — binário do ChromeDriver (recomenda-se remover do repositório).
- LICENSE.chromedriver, THIRD_PARTY_NOTICES.chromedriver — avisos/licenças do ChromeDriver.
- modelo_engajamento.pkl, modelo_kmeans.pkl, pca_kmeans.pkl — modelos serializados.
- scaler.pkl, scaler_kmeans.pkl — scalers serializados para pipelines.
- resultado_completo.csv, resultado_kmeans_teste.csv — datasets / resultados.
- instagram_comments.json, instagram_comments_2.json — dados coletados (ex.: comentários).
- webscrapping/ — pacote com código do scrapper e subpastas (banco, ml, rede_social). Veja `webscrapping/README.md` para detalhes de scripts locais.

Pré-requisitos
- Python 3.8+ (recomendado 3.8–3.11)
- pip
- Google Chrome instalado (compatível com ChromeDriver)
- Acesso à internet (para scraping e uso de APIs)

Dependências sugeridas (ex.: criar requirements.txt)
- selenium
- webdriver-manager
- beautifulsoup4
- requests
- pandas
- numpy
- scikit-learn
- joblib
- openai
- tqdm

Exemplo de requirements.txt
```
selenium
webdriver-manager
beautifulsoup4
requests
pandas
numpy
scikit-learn
joblib
openai
tqdm
```

Sugestão de .gitignore
```
# Python
__pycache__/
*.py[cod]
*.pkl

# Virtual env
.venv/
venv/

# Data & binaries
chromedriver.exe
*.csv
*.json

# Secrets
.env
```

Instalação (passo a passo)
1) Clonar repositório
```
git clone https://github.com/alynenobre/TCC---Web-Scrapping.git
cd TCC---Web-Scrapping
```

2) Criar e ativar ambiente virtual
- Linux / macOS
```
python -m venv .venv
source .venv/bin/activate
```
- Windows (PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- Windows (CMD)
```
python -m venv .venv
.\.venv\Scripts\activate.bat
```

3) Instalar dependências
```
pip install -r requirements.txt
```
Se não houver `requirements.txt`, instale manualmente:
```
pip install selenium webdriver-manager beautifulsoup4 requests pandas numpy scikit-learn joblib openai tqdm
```

Configuração de variáveis sensíveis
- Nunca colocar chaves no código. Use variáveis de ambiente:
  - Linux / macOS:
    ```
    export OPENAI_API_KEY="sua_chave_aqui"
    ```
  - Windows (PowerShell):
    ```
    setx OPENAI_API_KEY "sua_chave_aqui"
    ```

Uso seguro da API OpenAI (exemplo recomendado)
```python
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Exemplo de pergunta"}
    ]
)
print(response["choices"][0]["message"]["content"])
```

Selenium + ChromeDriver (recomendado: webdriver-manager)
- Exemplo para iniciar Chrome (dispensa download manual de chromedriver):
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")  # remova se quiser ver o navegador
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)
```
- Se quiser gerenciar chromedriver manualmente, baixe a versão compatível e aponte o caminho:
```python
driver = webdriver.Chrome(executable_path=r"C:\caminho\para\chromedriver.exe")
```

Execução de scripts
- Verifique `webscrapping/README.md` para instruções específicas dos scripts dentro da pasta `webscrapping`.
- Exemplos genéricos:
  - Executar um script de scraping:
    ```
    python webscrapping/nome_do_script.py --entrada caminho_entrada --saida caminho_saida
    ```
    (Substitua `nome_do_script.py` pelo arquivo real e informe os parâmetros suportados.)
  - Rodar módulo como pacote (se aplicável):
    ```
    python -m webscrapping.modulo
    ```

Carregar modelos e fazer predições (exemplo)
```python
import joblib
import pandas as pd

modelo = joblib.load("modelo_engajamento.pkl")
scaler = joblib.load("scaler.pkl")

# Preparar DataFrame com as colunas/ordem esperadas pelo scaler/modelo
df = pd.DataFrame([{
    "feature1": 0.1,
    "feature2": 5,
    # ...
}])
X_scaled = scaler.transform(df)
pred = modelo.predict(X_scaled)
print(pred)
```
Observação: valide as colunas e ordem de features exigidas pelos modelos serializados.

Observações sobre artefatos (.pkl, .csv, .json)
- Arquivos `.pkl` podem ter sido gerados com versões específicas de scikit-learn/joblib. Em caso de erro ao carregar, verifique versões e recrie o ambiente compatível.
- Os CSV/JSON no repositório podem conter amostras ou resultados finais — sempre valide e limpe os dados antes de usar.
- Se pretende re-treinar os modelos, documente o pipeline de pré-processamento e parâmetros do treinamento.

Segurança e remoção de segredos do histórico Git
1) Revogar imediatamente qualquer chave exposta (p.ex., a chave presente em `ia.py`) no serviço correspondente.
2) Para remover do histórico:
   - Usando BFG (recomenda-se):
     ```
     # baixar bfg.jar
     java -jar bfg.jar --delete-files ia.py
     git reflog expire --expire=now --all
     git gc --prune=now --aggressive
     git push --force
     ```
   - Ou usar git filter-repo (mais flexível):
     Consulte a documentação oficial do git-filter-repo para comandos precisos.
3) Forçar push para o remoto pode reescrever o histórico — coordene com colaboradores.

Remover binários e adicionar ao .gitignore
```
git rm --cached chromedriver.exe
echo "chromedriver.exe" >> .gitignore
git commit -m "Remover chromedriver binário do repositório e adicionar ao .gitignore"
git push
```

Boas práticas e recomendações
- Respeite robots.txt e termos de uso dos sites ao realizar scraping.
- Use delays, backoff e limite de taxa para evitar sobrecarregar servidores.
- Anonimize dados pessoais quando necessário e respeite legislações de privacidade.
- Adicione `requirements.txt` com versões fixas para reprodutibilidade.
- Considere adicionar `LICENSE` (ex.: MIT) e `CONTRIBUTING.md`.
- Padronize estilo de código (Black, isort) e adicione testes unitários para módulos críticos.

Sugestões de melhorias para o repositório
- Remover segredos do código e do histórico do Git.
- Remover `chromedriver.exe` do repositório (usar webdriver-manager ou Git LFS).
- Preencher/atualizar `webscrapping/README.md` com documentação detalhada de cada script (entrada, saída, parâmetros).
- Adicionar notebooks de exemplo demonstrando fluxo de coleta → pré-processamento → predição.
- Adicionar CI (GitHub Actions) para lint e execução de testes.

Contribuição
- Abra uma issue descrevendo a alteração/feature proposta antes de enviar PR.
- Siga as convenções de estilo do projeto e inclua testes para mudanças significativas.
- Documente como reproduzir e validar alterações.

Licença
- Existe `LICENSE.chromedriver` referente ao chromedriver. Adicione também um `LICENSE` para o restante do projeto (ex.: MIT, Apache-2.0) conforme desejar.

Contato
- Repositório: https://github.com/alynenobre/TCC---Web-Scrapping
- Mantenedor: alynenobre
