import sys
import os
from src.graph import EdgeWeightedGraph, Edge
from src.mst import KruskalMST

def resolver():
    # Se rodar direto no terminal (interativo), busca o arquivo local
    if sys.stdin.isatty():
        caminho = os.path.join("dados", "entradas_do_problema.txt")
        if os.path.exists(caminho):
            with open(caminho, "r") as f:
                dados = f.read().split()
        else:
            dados = []
    else:
        dados = sys.stdin.read().split()

    if not dados:
        return
    
    N = int(dados[0])
    pontos = []
    ponteiro = 1
    for _ in range(N):
        x = int(dados[ponteiro])
        y = int(dados[ponteiro+1])
        pontos.append((x, y))
        ponteiro += 2
        
    grafo = EdgeWeightedGraph(N)
    
    for i in range(N):
        x1, y1 = pontos[i]
        for j in range(i + 1, N):
            x2, y2 = pontos[j]
            distancia = abs(x1 - x2) + abs(y1 - y2)
            grafo.add_edge(Edge(i, j, distancia))
            
    kruskal = KruskalMST(grafo)
    print(kruskal.weight())

if __name__ == "__main__":
    resolver()
