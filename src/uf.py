class UnionFind:
    def __init__(self, n: int):
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, p: int) -> int:
        # Encontra o representante com compressão de caminhos
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
        # Une os conjuntos de p e q. Retorna True se houve união.
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
