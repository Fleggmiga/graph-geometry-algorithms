from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from main import Vertex

def draw_pts(ax, ps: List[Vertex], cfg: Dict):
    #zeichnet punkte als scatter, nutzt groesse und farbe aus cfg
    xs = [p.x for p in ps]; ys = [p.y for p in ps]
    ax.scatter(xs, ys, s=cfg["pt_size"], c=cfg["pt_color"], zorder=3)

def draw_edges(ax, ps_by_idx: Dict[int, Vertex], es: List[Tuple[int, int]], cfg: Dict):
    #zeichnet ungerichtete kantenliste, nutzt linienbreite und farbe aus cfg
    for a, b in es:
        pa, pb = ps_by_idx[a], ps_by_idx[b]
        ax.plot([pa.x, pb.x], [pa.y, pb.y], linewidth=cfg["ln_w"], color=cfg["ln_color"], zorder=2)

def draw_tris(ax, tris, cfg):
    #zeichnet dreiecke flach, nur konturen
    for t in tris:
        vs = t.vertices
        xs = [vs[0].x, vs[1].x, vs[2].x, vs[0].x]
        ys = [vs[0].y, vs[1].y, vs[2].y, vs[0].y]
        ax.plot(xs, ys, linewidth=cfg["ln_w"], color=cfg["ln_color"], zorder=1)
