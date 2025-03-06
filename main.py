import random

import igraph as ig
import matplotlib.pyplot as plt

grafo = ig.Graph(directed=True)

competidores = ["João", "Gabriel", "Gustavo", "Guilherme", "Lucas", "André", "Matheus", "Carlos"]

grafo.add_vertices(competidores)


def simular_fases(competidores):
    vencedores = []
    partidas = []
    random.shuffle(competidores)

    for i in range(0, len(competidores), 2):
        if i + 1 < len(competidores):
            competidor1, competidor2 = competidores[i], competidores[i + 1]
            vencedor = random.choice([competidor1, competidor2])
            partidas.append((competidor1, competidor2, vencedor))
            vencedores.append(vencedor)

    return vencedores, partidas


todas_partidas = []
fase_atual = competidores[:]

while len(fase_atual) > 1:
    fase_atual, partidas = simular_fases(fase_atual)
    todas_partidas.extend(partidas)

for competidor1, competidor2, vencedor in todas_partidas:
    perdedor = competidor1 if vencedor == competidor2 else competidor2
    grafo.add_edges([(perdedor, vencedor)])

ranking = grafo.pagerank(directed=True, damping=0.85)
ranking_ordenado = sorted(zip(competidores, ranking), key=lambda x: x[1], reverse=True)

print("Ranking final do torneio:")
for i, (competidor, score) in enumerate(ranking_ordenado, 1):
    print(f"{i}. {competidor} (Pontos: {score:.4f})")

grafo.vs["label"] = competidores
grafo.vs["color"] = "lightblue"

layout = grafo.layout("fr")
fig, ax = plt.subplots(figsize=(10, 7))
ig.plot(grafo, target=ax, layout=layout, vertex_size=30, edge_color="gray", vertex_color="lightblue", bbox=(600, 600),
        margin=50)

plt.show()
