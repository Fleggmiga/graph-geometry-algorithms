from typing import List, Tuple
import heapq
from main import Vertex

def _d2(a: Vertex, b: Vertex) -> float:
    #liefert quadrat der euklidischen distanz
    dx = a.x - b.x; dy = a.y - b.y
    return dx*dx + dy*dy

def mstp(ps: List[Vertex]) -> List[Tuple[int, int]]:
    #minimum spanning tree mit prim, start bei index 0
    if not ps:
        return []
    n = len(ps)
    inT = set()
    out = []
    start = ps[0].idx
    inT.add(start)
    heap = []
    idx_to_v = {v.idx: v for v in ps}
    for v in ps[1:]:
        heap.append((_d2(idx_to_v[start], v), start, v.idx))
    heapq.heapify(heap)
    while len(inT) < n and heap:
        w, a, b = heapq.heappop(heap)
        if b in inT:
            continue
        inT.add(b)
        out.append((a, b))
        for v in ps:
            if v.idx not in inT:
                heapq.heappush(heap, (_d2(idx_to_v[b], v), b, v.idx))
    return out
