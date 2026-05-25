from typing import List, Generator

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
        self._edges: List[Edge] = []

    def V(self) -> int:
        return self._V

    def add_edge(self, edge: Edge) -> None:
        self._edges.append(edge)

    def edges(self) -> List[Edge]:
        return self._edges
