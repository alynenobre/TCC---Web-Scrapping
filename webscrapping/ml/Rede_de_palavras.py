import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
import re
from nltk.corpus import stopwords
import nltk
from webscrapping.banco.banco import Banco
# Detecção de comunidades
from networkx.algorithms.community import greedy_modularity_communities

nltk.download('stopwords')

# Consulta no banco para pegar os comentários diretamente
query = """
    SELECT c.comentario, c.likes
    FROM instagram_comentario c
    INNER JOIN public.instagram_publicacao p ON c.url = p.url
    WHERE p.perfil = 'lulaoficial'
    GROUP BY c.html, c.comentario
	order by c.likes desc
    LIMIT 30;
"""

# Conecta ao banco e lê os dados
conexao_banco = Banco()
conexao = conexao_banco.conecta_banco(conexao_banco.database)
df = pd.read_sql_query(query, conexao)
conexao.close()

# Pré-processamento
stopwords_pt = set(stopwords.words('portuguese'))

def preprocess(texto):
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    palavras = texto.split()
    palavras = [p for p in palavras if p not in stopwords_pt and len(p) > 3 and not p.startswith('@') and not p[0].isdigit()]
    return palavras

# Geração dos pares de coocorrência
pares = []
for comentario in df['comentario']:
    palavras = preprocess(comentario)
    pares.extend(combinations(set(palavras), 2))  # combinações únicas por comentário

contagem = Counter(pares)

# Construção do grafo
G = nx.Graph()
for (pal1, pal2), peso in contagem.items():
    G.add_edge(pal1, pal2, weight=peso)

# Cálculo de centralidade
centralidade = nx.degree_centrality(G)


comunidades = list(greedy_modularity_communities(G))
cores = {}
for i, grupo in enumerate(comunidades):
    for palavra in grupo:
        cores[palavra] = i

# Layout do grafo
pos = nx.spring_layout(G, k=0.35, seed=42)

# Visualização aprimorada
plt.figure(figsize=(18, 12))
for node in G.nodes():
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[node],
        node_size=500 + 2000 * centralidade[node],
        node_color=[cores[node]],
        cmap=plt.cm.Set3,
        alpha=0.9
    )

# Desenha arestas
nx.draw_networkx_edges(G, pos, alpha=0.2)

# Rótulos
nx.draw_networkx_labels(G, pos, font_size=10)

# Finalização
plt.title("Rede de Coocorrência de Palavras – Comentários @lulaoficial", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()



# Cria um dicionário para mapeamento comunidade-palavra
comunidade_map = {}
for i, grupo in enumerate(comunidades):
    for palavra in grupo:
        comunidade_map[palavra] = i

# Tamanho e modularidade
modularidade = nx.algorithms.community.quality.modularity(G, comunidades)
print(f"Modularidade da rede: {modularidade:.4f}")
print(f"Número de comunidades detectadas: {len(comunidades)}")


densidade = nx.density(G)
print(f"Densidade da rede: {densidade:.4f}")

# Checar se a rede é conexa antes de calcular o diâmetro
if nx.is_connected(G):
    diametro = nx.diameter(G)
    print(f"Diâmetro da rede: {diametro}")
else:
    componentes = list(nx.connected_components(G))
    maior_componente = G.subgraph(componentes[0])
    diametro = nx.diameter(maior_componente)
    print(f"Diâmetro da maior componente conectada: {diametro}")
