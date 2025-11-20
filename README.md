# TCC - Web Scrapping

Descrição

Repositório para o Trabalho de Conclusão de Curso (TCC) sobre técnicas de web scraping e coleta de dados na web. Aqui estão scripts, notebooks e exemplos usados para extrair, transformar e armazenar dados de sites para análise.

Status

- Em desenvolvimento — ajuste e personalize conforme o avanço do TCC.

Principais funcionalidades

- Coleção de exemplos e padrões de scraping (requests + BeautifulSoup, Selenium, Scrapy).
- Processamento e limpeza básica de dados (pandas).
- Exportação para CSV/JSON.
- Notebooks para exploração e experimentação.

Tecnologias

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- pandas
- selenium (opcional)
- scrapy (opcional)
- tqdm

Estrutura sugerida do repositório

- src/                -> Código fonte (scrapers, utilitários)
- notebooks/          -> Notebooks Jupyter para experimentos e visualizações
- data/               -> Dados brutos e processados (não commitar dados sensíveis)
- configs/            -> Arquivos de configuração (ex.: config.yaml)
- tests/              -> Testes automatizados (se houver)
- requirements.txt    -> Dependências do projeto
- README.md           -> Este arquivo

Pré-requisitos

- Git
- Python 3.8 ou superior
- Navegador e driver (ex.: Chrome + chromedriver) caso utilize Selenium

Instalação (exemplo)

1. Clone o repositório:

   git clone https://github.com/alynenobre/TCC---Web-Scrapping.git
   cd TCC---Web-Scrapping

2. Crie e ative um ambiente virtual:

   python -m venv .venv
   source .venv/bin/activate  # Linux / macOS
   .venv\Scripts\activate     # Windows

3. Instale dependências:

   pip install -r requirements.txt

Exemplo de requirements.txt sugerido

requests
beautifulsoup4
lxml
pandas
tqdm
selenium  # opcional
scrapy    # opcional

Uso (exemplos)

- Executando um scraper simples:

  python src/scraper.py --config configs/config.yaml

- Executando um notebook (exemplo):

  jupyter notebook notebooks/analise_dados.ipynb

Observação: ajuste os nomes dos scripts e caminhos conforme a organização real do repositório.

Boas práticas ao realizar web scraping

- Respeite o arquivo robots.txt do site.
- Use cabeçalhos de User-Agent apropriados.
- Não sobrecarregue o servidor: implemente delays, uso de rate limiting e backoff exponencial.
- Verifique os Termos de Serviço do site antes de coletar dados.
- Evite coletar dados pessoais sensíveis sem consentimento.

Configuração recomendada (ex.: configs/config.yaml)

# Exemplo de opções
# target_urls:
#   - "https://exemplo.com/pagina1"
# output_dir: "data/raw"
# rate_limit: 1.0  # segundos entre requisições
# headless: true

Exemplo de execução direta (shell)

# Execução com variável de ambiente para modo headless
HEADLESS=true python src/scraper.py --config configs/config.yaml

Exemplo de saída esperada

- Arquivos CSV ou JSON em data/ contendo as colunas/atributos extraídos.
- Logs em logs/ com informações de execução e possíveis erros.

Contribuindo

Contribuições são bem-vindas. Siga estas etapas:

1. Fork do repositório
2. Crie uma branch com a sua feature: git checkout -b feature/nome
3. Commit suas alterações: git commit -m "Descrição da feature"
4. Push para a branch: git push origin feature/nome
5. Abra um Pull Request

Licença

Este repositório está licenciado sob a licença MIT — consulte o arquivo LICENSE para detalhes (ou atualize conforme sua preferência).

Autor

Alyne Nobre (AlyneNobre1)

Contato

- GitHub: https://github.com/AlyneNobre1
- Email: (insira seu email aqui)

Citação (se for parte do TCC)

Se utilizar este repositório em trabalhos acadêmicos, por favor cite:

Alyne Nobre. TCC - Web Scrapping. [ano]. Repositório: https://github.com/alynenobre/TCC---Web-Scrapping

Notas finais

- Este README é uma base inicial. Atualize seções como comandos de execução, nomes de scripts, exemplos de saída e dependências de acordo com o conteúdo real do repositório.
- Se quiser, posso também criar um requirements.txt, um exemplo de config.yaml e um template de scraper (src/scraper.py) neste repositório. Basta me pedir
