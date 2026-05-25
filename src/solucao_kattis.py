import sys

class UnionFind:
    def __init__(self, n: int):
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, p: int) -> int:
        root = p
        while root != self._parent[root]:
            root = self._parent[root]
        curr = p
        while curr != root:
            nxt = self._parent[curr]
            self._parent[curr] = root
            curr = nxt
        return root

    def union(self, p: int, q: int) -> bool:
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:
            return False

        if self._rank[root_p] < self._rank[root_q]:
            self._parent[root_p] = root_q
        elif self._rank[root_p] > self._rank[root_q]:
            self._parent[root_q] = root_p
        else:
            self._parent[root_q] = root_p
            self._rank[root_p] += 1

        return True


class Edge:
    def __init__(self, v: int, w: int, weight: int):
        self._v = v
        self._w = w
        self._weight = weight

    def weight(self) -> int:
        return self._weight

    def either(self) -> int:
        return self._v

    def other(self, vertex: int) -> int:
        if vertex == self._v:
            return self._w
        return self._v

    def __lt__(self, other: 'Edge') -> bool:
        return self._weight < other._weight


class EdgeWeightedGraph:
    def __init__(self, V: int):
        self._V = V
        self._edges = []

    def V(self) -> int:
        return self._V

    def add_edge(self, edge: Edge) -> None:
        self._edges.append(edge)

    def edges(self):
        return self._edges


class KruskalMST:
    def __init__(self, G: EdgeWeightedGraph, initial_uf: UnionFind, initial_weight: int):
        self._weight = initial_weight
        arestas = sorted(G.edges())
        
        for aresta in arestas:
            v = aresta.either()
            w = aresta.other(v)
            if initial_uf.union(v, w):
                self._weight += aresta.weight()

    def weight(self) -> int:
        return self._weight


def resolver():
    dados = sys.stdin.read().split()
    if not dados:
        return
    
    ponteiro = 0
    total_dados = len(dados)
    
    while ponteiro < total_dados:
        N = int(dados[ponteiro])
        ponteiro += 1
        
        if N <= 0:
            break
            
        pontos = []
        for _ in range(N):
            x = int(dados[ponteiro])
            y = int(dados[ponteiro+1])
            pontos.append((x, y))
            ponteiro += 2
            
        uf = UnionFind(N)
        
        coords_to_idx = {}
        unique_points = []
        mst_weight = 0
        arestas_adicionadas = 0
        
        for i in range(N):
            x, y = pontos[i]
            if (x, y) in coords_to_idx:
                orig_idx = coords_to_idx[(x, y)]
                if uf.union(orig_idx, i):
                    arestas_adicionadas += 1
            else:
                coords_to_idx[(x, y)] = i
                unique_points.append((x, y, i))
                
        if arestas_adicionadas == N - 1:
            print(mst_weight)
            continue
            
        owner = [-1] * 1003001
        dist = [10000] * 1003001
        
        q = []
        for x, y, idx in unique_points:
            cell = x * 1001 + y
            owner[cell] = idx
            dist[cell] = 0
            q.append((x, y))
            
        head = 0
        seen_edges = set()
        grafo = EdgeWeightedGraph(N)
        
        add_edge = grafo.add_edge
        abs_func = abs
        
        while head < len(q):
            x, y = q[head]
            head += 1
            
            curr_cell = x * 1001 + y
            curr_owner = owner[curr_cell]
            curr_dist = dist[curr_cell]
            
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx <= 1000 and 0 <= ny <= 1000:
                    n_cell = nx * 1001 + ny
                    n_owner = owner[n_cell]
                    
                    if n_owner == -1:
                        owner[n_cell] = curr_owner
                        dist[n_cell] = curr_dist + 1
                        q.append((nx, ny))
                    elif n_owner != curr_owner:
                        u, v = curr_owner, n_owner
                        if u > v:
                            u, v = v, u
                        edge_key = u * 100000 + v
                        if edge_key not in seen_edges:
                            seen_edges.add(edge_key)
                            px1, py1 = pontos[u]
                            px2, py2 = pontos[v]
                            w = abs_func(px1 - px2) + abs_func(py1 - py2)
                            add_edge(Edge(u, v, w))
                            
        kruskal = KruskalMST(grafo, uf, mst_weight)
        print(kruskal.weight())

if __name__ == "__main__":
    resolver()
