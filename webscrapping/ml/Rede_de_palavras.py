import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams
from itertools import combinations
from collections import Counter
import re
from nltk.corpus import stopwords
import nltk

from webscrapping.banco.banco import Banco
from networkx.algorithms.community import greedy_modularity_communities

# Baixar stopwords (só precisa na primeira vez)
nltk.download("stopwords")

# ============================
# 1. Consulta ao banco de dados
# ============================
query = """
    SELECT DISTINCT 
        c.comentario, 
        c.likes
    FROM instagram_comentario c
    INNER JOIN public.instagram_publicacao p 
        ON c.url = p.url
    WHERE p.perfil = 'lulaoficial'
    GROUP BY c.html, c.comentario
    ORDER BY c.likes DESC
    LIMIT 30;
"""

conexao_banco = Banco()
conexao = conexao_banco.conecta_banco(conexao_banco.database)
df = pd.read_sql_query(query, conexao)
conexao.close()

# ============================
# 2. Pré-processamento de texto
# ============================
stopwords_pt = set(stopwords.words("portuguese"))

def preprocess(texto: str):
    """Limpa o texto, remove stopwords, menções e tokens muito curtos."""
    texto = re.sub(r"[^\w\s]", "", str(texto).lower())
    palavras = texto.split()
    palavras = [
        p
        for p in palavras
        if p not in stopwords_pt
        and len(p) > 3
        and not p.startswith("@")
        and not p[0].isdigit()
    ]
    return palavras

# ============================
# 3. Geração dos pares de coocorrência
# ============================
pares = []
for comentario in df["comentario"]:
    palavras = preprocess(comentario)
    pares.extend(combinations(set(palavras), 2))  # combinações únicas por comentário

contagem = Counter(pares)

# ============================
# 4. Construção do grafo
# ============================
G = nx.Graph()
for (pal1, pal2), peso in contagem.items():
    G.add_edge(pal1, pal2, weight=peso)

# Centralidade de grau
centralidade = nx.degree_centrality(G)

# Detecção de comunidades
comunidades = list(greedy_modularity_communities(G))
cores = {}
for i, grupo in enumerate(comunidades):
    for palavra in grupo:
        cores[palavra] = i

# Layout
pos = nx.spring_layout(G, k=0.35, seed=42)

# ============================
# 5. Configuração visual (fontes maiores)
# ============================
rcParams.update(
    {
        "text.usetex": False,
        "font.family": "serif",
        "font.size": 14,        # tamanho base
        "axes.titlesize": 18,   # título maior
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
    }
)

# ============================
# 6. Visualização do grafo
# ============================
plt.figure(figsize=(18, 12))

# Nós (com tamanho proporcional à centralidade)
for node in G.nodes():
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[node],
        node_size=500 + 2000 * centralidade[node],
        node_color=[cores[node]],
        cmap=plt.cm.Set3,
        alpha=0.9,
    )

# Arestas
nx.draw_networkx_edges(G, pos, alpha=0.2)

# Rótulos dos nós – fonte maior
nx.draw_networkx_labels(
    G,
    pos,
    font_size=11,
    font_family="serif",
)

#plt.title(
#    "Rede de Coocorrência de Palavras – Comentários @eduardopaes",
#    fontsize=18,
#)
plt.axis("off")
plt.tight_layout()
plt.show()

# ============================
# 7. Métricas da rede
# ============================
# Mapa comunidade -> palavra (se quiser usar depois)
comunidade_map = {}
for i, grupo in enumerate(comunidades):
    for palavra in grupo:
        comunidade_map[palavra] = i

# Modularidade
modularidade = nx.algorithms.community.quality.modularity(G, comunidades)
print(f"Modularidade da rede: {modularidade:.4f}")
print(f"Número de comunidades detectadas: {len(comunidades)}")

# Densidade
densidade = nx.density(G)
print(f"Densidade da rede: {densidade:.4f}")

# Diâmetro (considerando componente gigante)
if nx.is_connected(G):
    diametro = nx.diameter(G)
    print(f"Diâmetro da rede: {diametro}")
else:
    componentes = list(nx.connected_components(G))
    maior_componente = G.subgraph(componentes[0])
    diametro = nx.diameter(maior_componente)
    print(f"Diâmetro da maior componente conectada: {diametro}")
