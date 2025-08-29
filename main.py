import math
from typing import List, Tuple

#Geometry types
class Vertex:
    def __init__(self, x: float, y: float, idx: int = None):
        self.x = float(x)           #
        self.y = float(y)
        self.idx = idx
    def __repr__(self):
        return f"Vertex({self.idx}, {self.x:.6f}, {self.y:.6f})"

class Triangle:
    def __init__(self, a: 'Vertex', b: 'Vertex', c: 'Vertex'):
        self.vertices = [a, b, c]

#Robust predicates
def orient2d(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def _tri_ccw(a: Vertex, b: Vertex, c: Vertex) -> bool:
    return orient2d(a.x, a.y, b.x, b.y, c.x, c.y) > 0.0

def incircle(a: Vertex, b: Vertex, c: Vertex, p: Vertex) -> bool:
    
    ax, ay = a.x - p.x, a.y - p.y
    bx, by = b.x - p.x, b.y - p.y
    cx, cy = c.x - p.x, c.y - p.y
    a2 = ax*ax + ay*ay
    b2 = bx*bx + by*by
    c2 = cx*cx + cy*cy
    det = ax*(by*c2 - b2*cy) - ay*(bx*c2 - b2*cx) + a2*(bx*cy - by*cx)
    s = orient2d(a.x, a.y, b.x, b.y, c.x, c.y)  # orientation of abc
    # scale-aware epsilon to damp numeric noise
    eps = 1e-14 * (abs(det) + a2 + b2 + c2 + abs(s) + 1.0)
    return det * (1.0 if s > 0.0 else -1.0) > eps

def _super_triangle(ps: List[Vertex]) -> Tuple[Vertex, Vertex, Vertex]:
    min_x = min(p.x for p in ps); max_x = max(p.x for p in ps)
    min_y = min(p.y for p in ps); max_y = max(p.y for p in ps)
    delta = max(max_x - min_x, max_y - min_y) or 1.0
    cx = 0.5 * (min_x + max_x)
    cy = 0.5 * (min_y + max_y)
    R = 1000.0 * delta
    v1 = Vertex(cx - 2*R, cy - R, idx=-1)
    v2 = Vertex(cx + 2*R, cy - R, idx=-2)
    v3 = Vertex(cx,       cy + 2*R, idx=-3)
    return v1, v2, v3

#Bowyer–Watson (2D Delaunay)
def bw(ps: List[Vertex]) -> List[Triangle]:
    if not ps:
        return []

    s1, s2, s3 = _super_triangle(ps)
    verts = list(ps) + [s1, s2, s3]
    i_s1, i_s2, i_s3 = len(verts)-3, len(verts)-2, len(verts)-1

    #store triangles as triplets of indices into verts
    tris = [(i_s1, i_s2, i_s3)]

    for ip, p in enumerate(ps):
        bad = []
        for (ia, ib, ic) in tris:
            a, b, c = verts[ia], verts[ib], verts[ic]
            if incircle(a, b, c, p):
                bad.append((ia, ib, ic))

        #boundary = edges that occur exactly once among "bad" triangles
        from collections import Counter
        cnt = Counter()
        for (ia, ib, ic) in bad:
            for u, v in ((ia, ib), (ib, ic), (ic, ia)):
                if u > v: u, v = v, u
                cnt[(u, v)] += 1
        boundary = [e for e, k in cnt.items() if k == 1]

        #remove bad triangles
        bad_set = set(bad)
        tris = [t for t in tris if t not in bad_set]

        #re-triangulate the hole
        for u, v in boundary:
            ia, ib = u, v
            if not _tri_ccw(verts[ia], verts[ib], p):
                ia, ib = ib, ia
            tris.append((ia, ib, ip))

    # build output triangles, dropping those that touch super-vertices or are degenerate
    def area2_idx(ia, ib, ic):
        ax, ay = verts[ia].x, verts[ia].y
        bx, by = verts[ib].x, verts[ib].y
        cx, cy = verts[ic].x, verts[ic].y
        return abs(orient2d(ax, ay, bx, by, cx, cy))

    out = []
    n = len(ps)
    for ia, ib, ic in tris:
        if ia >= n or ib >= n or ic >= n:
            continue
        if area2_idx(ia, ib, ic) <= 1e-14:
            continue
        out.append(Triangle(ps[ia], ps[ib], ps[ic]))
    return out

#Helpers
def triangles_to_indices(tris: List[Triangle]):
    idxs = []
    for t in tris:
        i, j, k = (v.idx for v in t.vertices)
        idxs.append([i, j, k])
    return idxs

def unique_edges_from_triangles(tri_indices):
    es = set()
    for i, j, k in tri_indices:
        a, b = (i, j) if i < j else (j, i)
        c, d = (j, k) if j < k else (k, j)
        e, f = (k, i) if k < i else (i, k)
        es.add((a, b)); es.add((c, d)); es.add((e, f))
    return list(es)
