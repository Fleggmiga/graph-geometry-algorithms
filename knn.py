from typing import List, Tuple
from math import hypot
from main import Vertex

def knn(ps: List[Vertex], k: int) -> List[Tuple[int, int]]:
    #knaechste nachbarn, ungerichtet, vereinigt beide richtungen
    n = len(ps)
    es = set()
    for i in range(n):
        djs = []
        for j in range(n):
            if i == j: 
                continue
            dx = ps[i].x - ps[j].x; dy = ps[i].y - ps[j].y
            d2 = dx*dx + dy*dy
            djs.append((d2, j))
        djs.sort(key=lambda t: t[0])
        for _, j in djs[:max(0, min(k, n-1))]:
            a, b = ps[i].idx, ps[j].idx
            if a > b: a, b = b, a
            es.add((a, b))
    return sorted(es)
