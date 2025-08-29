from typing import List, Tuple
from main import Vertex

def _d2(a: Vertex, b: Vertex) -> float:
    #liefert quadrat der euklidischen distanz
    dx = a.x - b.x; dy = a.y - b.y
    return dx*dx + dy*dy

def rng(ps: List[Vertex]) -> List[Tuple[int, int]]:
    #relative neighborhood, kante ij falls kein punkt k mit max(dik,djk) < dij existiert
    n = len(ps)
    es = []
    for i in range(n):
        for j in range(i+1, n):
            dij = _d2(ps[i], ps[j])
            ok = True
            for k in range(n):
                if k == i or k == j:
                    continue
                if max(_d2(ps[i], ps[k]), _d2(ps[j], ps[k])) < dij:
                    ok = False; break
            if ok:
                es.append((ps[i].idx, ps[j].idx))
    return es
