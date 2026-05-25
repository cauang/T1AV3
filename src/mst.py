from src.graph import EdgeWeightedGraph
from src.uf import UnionFind

class KruskalMST:
    def __init__(self, G: EdgeWeightedGraph):
        self._weight = 0

        # Ordena as arestas pelo peso
        arestas = sorted(G.edges())
        
        uf = UnionFind(G.V())
        arestas_adicionadas = 0
        
        for aresta in arestas:
            v = aresta.either()
            w = aresta.other(v)
            
            # Une e adiciona o peso se não formar ciclo
            if uf.union(v, w):
                self._weight += aresta.weight()
                arestas_adicionadas += 1
                if arestas_adicionadas == G.V() - 1:
                    break

    def weight(self) -> int:
        return self._weight
