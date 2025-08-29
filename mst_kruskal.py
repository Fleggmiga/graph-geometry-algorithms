from typing import List, Tuple
from main import Vertex

def _d2(a: Vertex, b: Vertex) -> float:
    #liefert quadrat der euklidischen distanz
    dx = a.x - b.x; dy = a.y - b.y
    return dx*dx + dy*dy

class _DSU:
    #disjoint set union, pfade komprimieren, rang heuristik
    def __init__(self, vs: List[Vertex]):
        self.parent = {v.idx: v.idx for v in vs}
        self.rank = {v.idx: 0 for v in vs}
    def find(self, x: int) -> int:
        #findet wurzelmenge
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a: int, b: int) -> bool:
        #vereinigt zwei mengen, true wenn vereinigt
        ra, rb = self.find(a), self.find(b)
        if ra == rb: 
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def mstk(ps: List[Vertex]) -> List[Tuple[int, int]]:
    #minimum spanning tree mit kruskal, volle kantenliste nach distanz sortiert
    n = len(ps)
    es = []
    for i in range(n):
        for j in range(i+1, n):
            es.append((_d2(ps[i], ps[j]), ps[i].idx, ps[j].idx))
    es.sort(key=lambda t: t[0])
    dsu = _DSU(ps)
    out = []
    for _, a, b in es:
        if dsu.union(a, b):
            out.append((a, b))
            if len(out) == n - 1:
                break
    return out
