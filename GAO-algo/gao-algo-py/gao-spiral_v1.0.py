
# gao_spiral.py
# Minimal reference implementation of GAO Spiral + baselines + 2-opt + metrics.
# MIT-licensed (see LICENSE). No external deps beyond numpy.

from __future__ import annotations
import math, time, random
from dataclasses import dataclass
from typing import List, Tuple, Callable, Dict, Any, Optional
import numpy as np
from sklearn.cluster import KMeans

Point = Tuple[float, float]
Tour = List[int]

def euclid(a: Point, b: Point) -> float:
    dx = a[0]-b[0]; dy = a[1]-b[1]
    return (dx*dx + dy*dy) ** 0.5

def tour_length(pts: List[Point], tour: Tour) -> float:
    n = len(tour)
    total = 0.0
    for i in range(n):
        a = pts[tour[i]]
        b = pts[tour[(i+1)%n]]
        total += euclid(a,b)
    return total

def centroid(pts: List[Point]) -> Point:
    arr = np.asarray(pts)
    c = arr.mean(axis=0)
    return float(c[0]), float(c[1])

def to_polar(pts: List[Point], C: Point):
    arr = np.asarray(pts) - np.asarray(C)
    r = np.hypot(arr[:,0], arr[:,1])
    theta = np.arctan2(arr[:,1], arr[:,0]) % (2*math.pi)
    return r, theta

def count_crossings(pts: List[Point], tour: Tour) -> int:
    # Count proper intersections among non-adjacent edges
    def seg_intersect(a,b,c,d):
        # Proper segment intersection test (excluding shared endpoints)
        def orient(p,q,r):
            return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
        def on_seg(p,q,r):
            return min(p[0],r[0]) <= q[0] <= max(p[0],r[0]) and min(p[1],r[1]) <= q[1] <= max(p[1],r[1])
        o1 = orient(a,b,c); o2 = orient(a,b,d)
        o3 = orient(c,d,a); o4 = orient(c,d,b)
        if o1==0 and on_seg(a,c,b): return False
        if o2==0 and on_seg(a,d,b): return False
        if o3==0 and on_seg(c,a,d): return False
        if o4==0 and on_seg(c,b,d): return False
        return (o1>0) != (o2>0) and (o3>0) != (o4>0)
    n = len(tour)
    edges = [(tour[i], tour[(i+1)%n]) for i in range(n)]
    crossings = 0
    for i in range(n):
        a1, a2 = edges[i]
        for j in range(i+1, n):
            b1, b2 = edges[j]
            # skip adjacent edges and sharing vertices
            if len({a1,a2,b1,b2}) < 4: 
                continue
            if (a1==b2 and a2==b1): # same edge reversed
                continue
            if seg_intersect(pts[a1], pts[a2], pts[b1], pts[b2]):
                crossings += 1
    return crossings

def two_opt(pts: List[Point], tour: Tour, max_iters: int = 10_000):
    n = len(tour)
    improved = True
    iters = 0
    def delta(i,k):
        a, b = tour[i], tour[(i+1)%n]
        c, d = tour[k], tour[(k+1)%n]
        return (euclid(pts[a], pts[c]) + euclid(pts[b], pts[d]) -
                (euclid(pts[a], pts[b]) + euclid(pts[c], pts[d])))
    while improved and iters < max_iters:
        improved = False
        best_gain = 0.0
        best_pair = None
        for i in range(n-1):
            for k in range(i+2, n-(i==0)):
                gain = delta(i,k)
                if gain < best_gain:
                    best_gain = gain
                    best_pair = (i,k)
        if best_pair is not None:
            i,k = best_pair
            tour[i+1:k+1] = reversed(tour[i+1:k+1])
            improved = True
        iters += 1
    return tour, iters

# -----------------------------
# Baselines
# -----------------------------
def nearest_neighbor(pts: List[Point], start: Optional[int] = None) -> Tour:
    n = len(pts)
    if start is None:
        start = 0
    unvis = set(range(n))
    cur = start
    tour = [cur]
    unvis.remove(cur)
    while unvis:
        nxt = min(unvis, key=lambda j: euclid(pts[cur], pts[j]))
        tour.append(nxt)
        unvis.remove(nxt)
        cur = nxt
    return tour

def sweep_then_connect(pts: List[Point]) -> Tour:
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    order = list(range(len(pts)))
    order.sort(key=lambda i: (theta[i], r[i]))
    return order

def cheapest_insertion(pts: List[Point], start: Optional[int] = None) -> Tour:
    n = len(pts)
    if n <= 3:
        return list(range(n))
    if start is None:
        start = 0
    remaining = set(range(n))
    # init with triangle: start + two nearest
    start_pt = start
    remaining.remove(start_pt)
    a = min(remaining, key=lambda j: euclid(pts[start_pt], pts[j]))
    remaining.remove(a)
    b = min(remaining, key=lambda j: euclid(pts[start_pt], pts[j]))
    remaining.remove(b)
    tour = [start_pt, a, b]
    # make it a cycle
    # cheapest insertion loop
    while remaining:
        best_inc = None
        best_pos = None
        best_city = None
        m = len(tour)
        for city in list(remaining):
            inc_best = float('inf')
            pos_best = 0
            for i in range(m):
                u = tour[i]; v = tour[(i+1)%m]
                inc = euclid(pts[u], pts[city]) + euclid(pts[city], pts[v]) - euclid(pts[u], pts[v])
                if inc < inc_best:
                    inc_best = inc; pos_best = i+1
            if best_inc is None or inc_best < best_inc:
                best_inc = inc_best; best_pos = pos_best; best_city = city
        tour.insert(best_pos, best_city)
        remaining.remove(best_city)
    return tour


# -----------------------------
# GAO Spiral
# -----------------------------
@dataclass
class GAOParams:
    def __init__(self,
                 bins=None, w_theta=1.0, w_r=1.0,
                 weave_mode="none",   # "bias", "elastic", "curvature"
                 bias_rate=0.0,
                 k_elast=0.3,
                 k_curvgrid=0.2):
        self.bins = bins
        self.w_theta = w_theta
        self.w_r = w_r
        self.weave_mode = weave_mode
        self.bias_rate = bias_rate       # lattice rotation rate
        self.k_elast = k_elast           # angular elasticity strength
        self.k_curvgrid = k_curvgrid     # curvature-driven re-meshing


def gao_spiral(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    Golden-Angle Greedy (GAO) Spiral Heuristic for Euclidean TSP.
    Greedy in direction (angle) with adaptive radial smoothing.
    Steps:
      1. Convert points to polar coords around centroid.
      2. Build angular bins (Trinitas/Textura structure).
      3. Iterate using golden-angle rotation (Ecologia rhythm).
      4. For each step, pick the next candidate minimizing
         combined angular deviation + radial smoothness.
      5. Add optional Adaptatio refinements:
         - radial-band filter (limit |Δr| jumps)
         - quantile pre-filter (soft constraint)
         - momentum penalty (avoid in↔out ping-pong)
      6. Validate tour completeness.
    """

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    B = params.bins or max(8, int(2 * math.sqrt(n)))
    bins = [[] for _ in range(B)]
    for i in range(n):
        b = int((theta[i] / (2 * math.pi)) * B) % B
        bins[b].append(i)

    visited = [False] * n
    current = min(range(n), key=lambda i: r[i])  # start near center
    tour: List[int] = []
    alpha = 0.0
    phi = math.tau * (1 - 1 / ((1 + 5 ** 0.5) / 2))  # golden angle (≈137.5°)
    r_med = float(np.median(r)) or 1.0

    # Precompute a typical edge scale (for adaptive band width)
    nn_scale = np.median([np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
                          for i in range(min(n, 50)) for j in range(i+1, min(n, 50))])
    tau0 = 0.25 * nn_scale  # starting radial band
    grow = 1.8              # widening factor

    # --- local helpers ---
    def ang_diff(a, b):
        """Absolute minimal angular difference (radians)."""
        d = abs(a - b) % (2 * math.pi)
        return min(d, 2 * math.pi - d)

    def pop_candidate(alpha):
        """Find next unvisited index from bins near target angle alpha."""
        center = int((alpha / (2 * math.pi)) * B) % B
        for radius in range(B // 2 + 1):
            for sgn in (0, 1):
                b = (center + (radius if sgn == 0 else -radius)) % B
                while bins[b] and visited[bins[b][0]]:
                    bins[b].pop(0)
                if bins[b]:
                    return b, bins[b][0]
        return None, None

    def choose_candidate(alpha, current, candidates, last_sign):
        """Select best candidate using Adaptatio refinements."""
        tau = tau0
        cand = None

        # (A) radial-band filter — progressively relax
        for _ in range(3):
            filt = [j for j in candidates if abs(r[j] - r[current]) <= tau and not visited[j]]
            if filt:
                candidates = filt
                break
            tau *= grow

        if not candidates:
            return None

        # (B) quantile filter by |Δr|
        drs = np.array([abs(r[j] - r[current]) for j in candidates])
        thr = np.quantile(drs, 0.35)
        pool = [j for j, dj in zip(candidates, drs) if dj <= thr] or candidates

        # (C) momentum penalty — avoid alternating direction
        def momentum_penalty(j):
            s = np.sign(r[j] - r[current])
            return 0.15 if (last_sign != 0 and s != last_sign) else 0.0

        # final composite score
        cand = min(
            pool,
            key=lambda j:
                params.w_theta * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + momentum_penalty(j)
        )
        return cand

    # --- main loop ---
    last_sign = 0
    for _ in range(n):
        tour.append(current)
        visited[current] = True
        alpha = (alpha + phi) % (2 * math.pi)

        b, cand = pop_candidate(alpha)
        if b is not None:
            # refine within this bin
            k = min(10, len(bins[b]))
            candidates = [idx for idx in bins[b][:k] if not visited[idx]]
        else:
            candidates = [i for i in range(n) if not visited[i]]

        if not candidates:
            break

        # choose with Adaptatio refinements
        cand = choose_candidate(alpha, current, candidates, last_sign)
        if cand is None:
            # fallback: any unvisited min angle diff
            unvis = [i for i in range(n) if not visited[i]]
            if not unvis:
                break
            cand = min(unvis, key=lambda j: ang_diff(theta[j], alpha))

        last_sign = np.sign(r[cand] - r[current])
        current = cand

    # --- Validation & repair ---
    unique_tour = []
    seen = set()
    for i in tour:
        if i not in seen:
            unique_tour.append(i)
            seen.add(i)
    if len(unique_tour) < n:
        missed = [i for i in range(n) if i not in seen]
        unique_tour.extend(missed)

    assert len(unique_tour) == n
    assert len(set(unique_tour)) == n

    return unique_tour


# -----------------------------
# Evaluation utilities
# -----------------------------
def evaluate_algorithm(name: str, builder: Callable[[List[Point]], Tour],
                       pts: List[Point],
                       run_2opt: bool = True,
                       two_opt_budget: int = 10000) -> Dict[str, Any]:
    t0 = time.time()
    tour = builder(pts)
    t1 = time.time()
    init_len = tour_length(pts, tour)
    init_cross = count_crossings(pts, tour)
    two_moves = 0
    if run_2opt:
        tour, moves = two_opt(pts, tour, max_iters=two_opt_budget)
        two_moves = moves
    t2 = time.time()
    final_len = tour_length(pts, tour)
    final_cross = count_crossings(pts, tour)
    return {
        "name": name,
        "build_time_ms": (t1 - t0)*1000.0,
        "opt_time_ms": (t2 - t1)*1000.0,
        "init_length": init_len,
        "init_crossings": init_cross,
        "final_length": final_len,
        "final_crossings": final_cross,
        "two_opt_moves": two_moves
    }
