from src.graph import EdgeWeightedGraph
from src.uf import UnionFind

class KruskalMST:
    def __init__(self, G: EdgeWeightedGraph, initial_uf: UnionFind, initial_weight: int):
        self._weight = initial_weight
        
        # Ordena as arestas candidatas pelo peso
        arestas = sorted(G.edges())
        
        for aresta in arestas:
            v = aresta.either()
            w = aresta.other(v)
            
            # Une e acumula se pertencerem a componentes diferentes
            if initial_uf.union(v, w):
                self._weight += aresta.weight()

    def weight(self) -> int:
        return self._weight
