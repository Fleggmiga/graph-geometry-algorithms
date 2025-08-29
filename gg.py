from typing import List, Tuple
from math import hypot
from main import Vertex

#dist2, ohne wurzel
def _d2(a: Vertex, b: Vertex) -> float:
    #liefert quadrat der euklidischen distanz
    dx = a.x - b.x; dy = a.y - b.y
    return dx*dx + dy*dy

def gg(ps: List[Vertex]) -> List[Tuple[int, int]]:
    #gabriel graph, kante ij wenn kreis mit durchmesser ij keinen weiteren punkt enthaelt
    n = len(ps)
    es = []
    for i in range(n):
        for j in range(i+1, n):
            mx = 0.5*(ps[i].x + ps[j].x); my = 0.5*(ps[i].y + ps[j].y)
            r2 = 0.25 * _d2(ps[i], ps[j])
            ok = True
            for k in range(n):
                if k == i or k == j: 
                    continue
                dx = ps[k].x - mx; dy = ps[k].y - my
                if dx*dx + dy*dy < r2:
                    ok = False; break
            if ok:
                es.append((ps[i].idx, ps[j].idx))
    return es
