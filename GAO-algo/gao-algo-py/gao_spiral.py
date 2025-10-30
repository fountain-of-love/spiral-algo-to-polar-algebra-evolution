
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


def gao_spiral_v2(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v2: introduces 2D Textura (θ × r) binning.
    Each point is indexed by its angular bin and radial band, ensuring
    smoother Adaptatio (radial continuity) without losing angular rhythm.

    Changes vs v1:
      - Two-dimensional bin structure (Bθ × Br)
      - Candidate search explores angular ±range and radial ±range
      - Adaptive fallback if bins are sparse
      - Reuses Adaptatio refinements (band, quantile, momentum)
    """

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r)
    theta = np.array(theta)
    r_max = r.max() + 1e-9

    # --- define 2D bins ---
    Bθ = params.bins or max(8, int(2 * math.sqrt(n)))
    Br = max(4, int(0.5 * math.sqrt(n)))   # radial layers
    bins = [[[] for _ in range(Br)] for _ in range(Bθ)]

    for i in range(n):
        bθ = int((theta[i] / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[i] / r_max) * Br)
        br = min(br, Br - 1)
        bins[bθ][br].append(i)

    visited = [False] * n
    current = min(range(n), key=lambda i: r[i])
    tour: List[int] = []
    alpha = 0.0
    phi = math.tau * (1 - 1 / ((1 + 5 ** 0.5) / 2))  # golden angle
    r_med = float(np.median(r)) or 1.0

    # baseline radial-band smoothing scale
    nn_scale = np.median([np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
                          for i in range(min(n, 50)) for j in range(i + 1, min(n, 50))])
    tau0 = 0.25 * nn_scale
    grow = 1.8

    def ang_diff(a, b):
        d = abs(a - b) % (2 * math.pi)
        return min(d, 2 * math.pi - d)

    def choose_candidate(alpha, current, last_sign):
        """Find next unvisited point considering both θ and r bins."""
        bθ = int((alpha / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[current] / r_max) * Br)
        cand_pool = []

        # Explore local angular ±2 bins and radial ±1 bands
        for dθ in range(-2, 3):
            for dr in range(-1, 2):
                iθ = (bθ + dθ) % Bθ
                ir = min(max(br + dr, 0), Br - 1)
                cand_pool.extend([idx for idx in bins[iθ][ir] if not visited[idx]])

        if not cand_pool:
            # fallback: any unvisited nearest in angle
            cand_pool = [i for i in range(n) if not visited[i]]
            if not cand_pool:
                return None

        # (A) Radial-band filter
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt
                break
            tau *= grow

        if not cand_pool:
            return None

        # (B) Quantile filter by |Δr|
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        thr = np.quantile(drs, 0.35)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # (C) Momentum penalty
        def momentum_penalty(j):
            s = np.sign(r[j] - r[current])
            return 0.1 if (last_sign != 0 and s != last_sign) else 0.0

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
        cand = choose_candidate(alpha, current, last_sign)
        if cand is None:
            break
        last_sign = np.sign(r[cand] - r[current])
        current = cand

    # --- validation ---
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



def gao_spiral_v2_1(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v2.1 — refined θ×r binning with smoother Adaptatio flow.
    Enhancements:
      A. Finer radial resolution (Br ≈ √n)
      B. Wider neighborhood search (±3θ, ±2r)
      C. Relaxed quantile filter (top 60%)
      D. Momentum persistence bias (encourages stable |Δr| amplitude)

    Expected effect: smoother radial progression (Adaptatio ↑),
    stable angular rhythm (Ecologia ↑), and overall higher coherence.
    """

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r)
    theta = np.array(theta)
    r_max = r.max() + 1e-9

    # --- define finer 2D bins (θ × r) ---
    Bθ = params.bins or max(8, int(2 * math.sqrt(n)))
    Br = max(10, int(math.sqrt(n)))   # finer radial layering
    bins = [[[] for _ in range(Br)] for _ in range(Bθ)]

    for i in range(n):
        bθ = int((theta[i] / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[i] / r_max) * Br)
        br = min(br, Br - 1)
        bins[bθ][br].append(i)

    visited = [False] * n
    current = min(range(n), key=lambda i: r[i])
    tour: List[int] = []
    alpha = 0.0
    phi = math.tau * (1 - 1 / ((1 + 5 ** 0.5) / 2))  # golden angle
    r_med = float(np.median(r)) or 1.0

    # baseline radial-band scale for Adaptatio
    nn_scale = np.median([np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
                          for i in range(min(n, 50)) for j in range(i + 1, min(n, 50))])
    tau0 = 0.25 * nn_scale
    grow = 1.8

    def ang_diff(a, b):
        d = abs(a - b) % (2 * math.pi)
        return min(d, 2 * math.pi - d)

    def choose_candidate(alpha, current, last_sign, prev_dr):
        """Pick next unvisited candidate based on θ×r proximity and Adaptatio refinements."""
        bθ = int((alpha / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[current] / r_max) * Br)
        cand_pool = []

        # (B) Wider local search window
        for dθ in range(-3, 4):     # ±3 angular bins
            for dr in range(-2, 3): # ±2 radial bands
                iθ = (bθ + dθ) % Bθ
                ir = min(max(br + dr, 0), Br - 1)
                cand_pool.extend([idx for idx in bins[iθ][ir] if not visited[idx]])

        if not cand_pool:
            # fallback: any unvisited nearest in angle
            cand_pool = [i for i in range(n) if not visited[i]]
            if not cand_pool:
                return None

        # (A) Radial-band filter (progressive)
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt
                break
            tau *= grow

        if not cand_pool:
            return None

        # (C) Relaxed quantile (keep 60% closest in radius)
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        thr = np.quantile(drs, 0.6)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # (D) Momentum persistence penalty: discourage abrupt |Δr| amplitude shifts
        def momentum_penalty(j):
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_penalty = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            return base + amp_penalty

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
    prev_dr = 0.0
    for _ in range(n):
        tour.append(current)
        visited[current] = True
        alpha = (alpha + phi) % (2 * math.pi)
        cand = choose_candidate(alpha, current, last_sign, prev_dr)
        if cand is None:
            break
        prev_dr = abs(r[cand] - r[current])
        last_sign = np.sign(r[cand] - r[current])
        current = cand

    # --- validation ---
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



def gao_spiral_v3(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v3 — θ×r bins + Adaptive Phase Feedback (dynamic Δθ)

    What’s new vs v2.1:
      • Adaptive rotation step φ_t = φ0 * (1 + control), where:
          control = k_r * (EMA |Δr| / scale_r)
                  + k_den * density_signal
                  + k_phase * phase_error   (phase_error = (φ0 - EMA Δθ)/φ0)
      • Clamping keeps φ_t within [φ0 * (1 - φ_clamp), φ0 * (1 + φ_clamp)]
      • Goal: lift Adaptatio (smooth |Δr|) and Ecologia (stable spiral rhythm)
      • Deterministic, same overall complexity as v2.1

    Tunables (set below):
      - k_r:    how much radial jump influences phase
      - k_den:  how local density (bins occupancy) influences phase
      - k_phase:phase feedback strength (nudges Δθ toward φ0)
      - φ_clamp: max ±% change per step
      - ema_*:  EMA factors for |Δr| and Δθ

    """

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r)
    theta = np.array(theta)
    r_max = r.max() + 1e-9

    # --- 2D θ×r binning (Textura) ---
    Bθ = params.bins or max(8, int(2 * math.sqrt(n)))
    Br = max(10, int(math.sqrt(n)))   # finer radial layering (as in v2.1)
    bins = [[[] for _ in range(Br)] for _ in range(Bθ)]
    for i in range(n):
        bθ = int((theta[i] / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[i] / r_max) * Br)
        br = min(br, Br - 1)
        bins[bθ][br].append(i)

    visited = [False] * n
    current = min(range(n), key=lambda i: r[i])  # start near center
    tour: List[int] = []

    # --- Golden-angle baseline & feedback state (Ecologia) ---
    phi0 = math.tau * (1 - 1 / ((1 + 5 ** 0.5) / 2))  # ≈ 137.50776°
    alpha = 0.0

    # Feedback gains (safe defaults)
    k_r = 0.35       # coupling from |Δr| to phase
    k_den = 0.20     # coupling from local density to phase
    k_phase = 0.40   # phase error feedback (nudges Δθ toward φ0)
    phi_clamp = 0.20 # allow ±20% change around φ0

    # EMAs for flow & rhythm
    ema_r = 0.0
    ema_dtheta = phi0
    ema_r_beta = 0.85      # smoother EMA for |Δr|
    ema_theta_beta = 0.85  # smoother EMA for Δθ

    # Radial scale for normalization (Adaptatio)
    nn_scale = np.median([np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
                          for i in range(min(n, 50)) for j in range(i + 1, min(n, 50))]) or 1.0
    r_med = float(np.median(r)) or 1.0

    # Band filter (as in v2.1)
    tau0 = 0.25 * nn_scale
    grow = 1.8

    def ang_diff(a, b):
        d = abs(a - b) % (2 * math.pi)
        return min(d, 2 * math.pi - d)

    def local_density_signal(bθ_center: int, br_center: int) -> float:
        """
        A simple, deterministic density proxy in the local θ×r neighborhood.
        Returns a normalized value ~ [0, 1.5], where >1 means locally dense.
        """
        total = 0
        cells = 0
        for dθ in range(-2, 3):
            for dr in range(-1, 2):
                iθ = (bθ_center + dθ) % Bθ
                ir = min(max(br_center + dr, 0), Br - 1)
                total += len(bins[iθ][ir])
                cells += 1
        mean_bin = (n / (Bθ * Br))  # expected avg occupancy
        return (total / max(1, cells)) / max(1e-9, mean_bin)  # >1 -> denser than avg

    def choose_candidate(alpha, current, last_sign, prev_dr):
        """Pick next point using θ×r neighborhood + Adaptatio refinements."""
        bθ = int((alpha / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[current] / r_max) * Br)
        cand_pool = []

        # Wider local search window (as in v2.1): ±3θ × ±2r
        for dθ in range(-3, 4):
            for dr in range(-2, 3):
                iθ = (bθ + dθ) % Bθ
                ir = min(max(br + dr, 0), Br - 1)
                if bins[iθ][ir]:
                    cand_pool.extend([idx for idx in bins[iθ][ir] if not visited[idx]])

        if not cand_pool:
            # Fallback: any unvisited nearest in angle
            cand_pool = [i for i in range(n) if not visited[i]]
            if not cand_pool:
                return None

        # Radial-band filter (progressive widening)
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt
                break
            tau *= grow

        if not cand_pool:
            return None

        # Relaxed quantile filter: keep closest 60% in |Δr|
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        thr = np.quantile(drs, 0.6)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # Momentum persistence (discourage sign flip and amplitude jumps)
        def momentum_penalty(j):
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_penalty = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            return base + amp_penalty

        cand = min(
            pool,
            key=lambda j:
                params.w_theta * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + momentum_penalty(j)
        )
        return cand

    # --- main loop with adaptive phase ---
    last_sign = 0
    prev_dr = 0.0

    for step in range(n):
        tour.append(current)
        visited[current] = True

        # Compute density near current location (for phase control)
        bθ_now = int((alpha / (2 * math.pi)) * Bθ) % Bθ
        br_now = int((r[current] / r_max) * Br)
        den_sig = local_density_signal(bθ_now, br_now)  # ~ 1 in average areas

        # Build next candidate with current alpha
        cand = choose_candidate(alpha, current, last_sign, prev_dr)
        if cand is None:
            break

        # Update flow EMAs (|Δr| and Δθ) based on the move we're about to take
        d_r = abs(r[cand] - r[current])
        # estimated Δθ if we were to move (for phase feedback)
        # (Note: use target alpha as proxy; on average this tracks realized Δθ)
        d_theta_est = ang_diff(theta[cand], alpha)

        ema_r = ema_r_beta * ema_r + (1 - ema_r_beta) * d_r
        ema_dtheta = ema_theta_beta * ema_dtheta + (1 - ema_theta_beta) * d_theta_est

        # --- Adaptive phase controller (clamped) ---
        # Normalize |Δr| by scale; density >1 means "crowded"
        flow_term   = k_r * (ema_r / max(1e-9, nn_scale))
        density_term= k_den * (den_sig - 1.0)          # negative if sparse, positive if dense
        phase_err   = (phi0 - ema_dtheta) / max(1e-9, phi0)
        phase_term  = k_phase * phase_err

        control = flow_term + density_term + phase_term
        control = max(-phi_clamp, min(phi_clamp, control))   # clamp to ±20% by default

        phi_t = phi0 * (1.0 + control)
        alpha = (alpha + phi_t) % (2 * math.pi)

        # Commit the move
        prev_dr = d_r
        last_sign = np.sign(r[cand] - r[current])
        current = cand

    # --- Validation & repair (same as v2.1) ---
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


def gao_spiral_v3_1(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v3.1 — Self-Regulating Flow Triad (Adaptatio–Textura–Ecologia)

    Improvements over v3:
      • Dynamic Textura  — bin weighting by local density
      • Adaptive Quantile — flow-sensitive |Δr| filtering
      • Curvature penalty — rhythm stabilization
      • Safe candidate handling + graceful fallback

    Expected gains:
        Adaptatio ↑ 0.65–0.75
        Textura   ↑ 0.65–0.70
        Ecologia  ↑ 0.25–0.30
        Overall   ↑ 0.67–0.72
    """

    # --- Initialization ---
    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r, theta = np.array(r), np.array(theta)
    r_max = r.max() + 1e-9

    # θ×r bin lattice (Textura structure)
    Bθ = params.bins or max(8, int(2 * math.sqrt(n)))
    Br = max(10, int(math.sqrt(n)))
    bins = [[[] for _ in range(Br)] for _ in range(Bθ)]
    for i in range(n):
        bθ = int((theta[i] / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[i] / r_max) * Br)
        br = min(br, Br - 1)
        bins[bθ][br].append(i)

    visited = [False] * n
    current = min(range(n), key=lambda i: r[i])  # start near center
    tour: List[int] = []

    # --- Constants & feedback parameters ---
    phi0 = math.tau * (1 - 1 / ((1 + 5 ** 0.5) / 2))  # golden angle
    alpha = 0.0

    # Phase feedback (Ecologia)
    # k_r, k_den, k_phase = 0.35, 0.20, 0.40
    # phi_clamp = 0.20

    # Flow-structure couplings
    # k_tex = 0.5   # density → angular weight
    # k_q = 0.5     # density → quantile scaling
    # k_curv = 0.1  # curvature penalty

    # Exponentially-weighted averages
    ema_r, ema_dtheta = 0.0, phi0
    # ema_r_beta, ema_theta_beta = 0.85, 0.85

    # Feedback coefficients
    k_r, k_den, k_phase = 0.35, 0.25, 0.40
    phi_clamp = 0.20

    # Flow-structure couplings
    k_tex = 0.9  # stronger texture feedback
    k_q = 0.25  # gentler quantile adaptivity
    k_curv = 0.06  # softer curvature damping

    # Faster response
    ema_r_beta, ema_theta_beta = 0.78, 0.78

    # Scale references
    nn_scale = np.median([
        np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
        for i in range(min(n, 50))
        for j in range(i + 1, min(n, 50))
    ]) or 1.0
    r_med = float(np.median(r)) or 1.0
    tau0, grow = 0.25 * nn_scale, 1.8

    # --- Utility helpers ---
    def ang_diff(a, b):
        d = abs(a - b) % (2 * math.pi)
        return min(d, 2 * math.pi - d)

    def local_density(bθ_c, br_c):
        total = 0
        for dθ in range(-2, 3):
            for dr in range(-1, 2):
                iθ = (bθ_c + dθ) % Bθ
                ir = min(max(br_c + dr, 0), Br - 1)
                total += len(bins[iθ][ir])
        mean_bin = n / (Bθ * Br)
        return (total / 25) / max(1e-9, mean_bin)

    # --- Candidate selection with adaptivity ---
    def choose_candidate(alpha, current, last_sign, prev_dr, ema_dtheta):
        bθ = int((alpha / (2 * math.pi)) * Bθ) % Bθ
        br = int((r[current] / r_max) * Br)
        den_sig = local_density(bθ, br)

        # Collect neighborhood
        cand_pool = []
        for dθ in range(-3, 4):
            for dr in range(-2, 3):
                iθ = (bθ + dθ) % Bθ
                ir = min(max(br + dr, 0), Br - 1)
                cand_pool.extend([idx for idx in bins[iθ][ir] if not visited[idx]])

        if not cand_pool:
            return None

        # Radial-band filter
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt
                break
            tau *= grow
        if not cand_pool:
            return None

        # Adaptive quantile based on density
        q = max(0.25, min(0.8, 0.6 * (1 - k_q * (den_sig - 1))))
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        thr = np.quantile(drs, q)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # Penalties
        def penalties(j):
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_penalty = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            curv_penalty = k_curv * abs(ang_diff(theta[j], alpha) - ema_dtheta) / phi0
            return base + amp_penalty + curv_penalty

        # Dynamic Textura weighting
        tex_weight = 1 / (1 + k_tex * (den_sig - 1))

        cand = min(
            pool,
            key=lambda j: (
                params.w_theta * tex_weight * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + penalties(j)
            ),
        )
        return (cand, den_sig)

    # --- Main spiral loop (with robust fallback) ---
    last_sign, prev_dr = 0, 0.0
    for _ in range(n):
        tour.append(current)
        visited[current] = True

        out = choose_candidate(alpha, current, last_sign, prev_dr, ema_dtheta)
        if out is None:
            remaining = [i for i in range(n) if not visited[i]]
            if not remaining:
                break
            cand = min(
                remaining,
                key=lambda j: np.linalg.norm(np.asarray(pts[j]) - np.asarray(pts[current]))
            )
            den_sig = 1.0
        else:
            cand, den_sig = out

        # --- Feedback updates ---
        d_r = abs(r[cand] - r[current])
        d_theta_est = ang_diff(theta[cand], alpha)
        ema_r = ema_r_beta * ema_r + (1 - ema_r_beta) * d_r
        ema_dtheta = ema_theta_beta * ema_dtheta + (1 - ema_theta_beta) * d_theta_est

        flow_term = k_r * (ema_r / max(1e-9, nn_scale))
        density_term = k_den * (den_sig - 1.0)
        phase_err = (phi0 - ema_dtheta) / max(1e-9, phi0)
        phase_term = k_phase * phase_err

        control = flow_term + density_term + phase_term
        control = max(-phi_clamp, min(phi_clamp, control))
        phi_t = phi0 * (1.0 + control)
        alpha = (alpha + phi_t) % (2 * math.pi)

        prev_dr = d_r
        last_sign = np.sign(r[cand] - r[current])
        current = cand

    # --- Validation & repair ---
    unique_tour, seen = [], set()
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


class GAOParams:
    def __init__(self,
                 bins=None, w_theta=1.0, w_r=1.0,
                 weave_mode="none",     # "bias", "elastic", "curvature", or combo
                 bias_rate=0.0,
                 k_elast=0.25,
                 k_curvgrid=0.15):
        self.bins = bins
        self.w_theta = w_theta
        self.w_r = w_r
        self.weave_mode = weave_mode
        self.bias_rate = bias_rate
        self.k_elast = k_elast
        self.k_curvgrid = k_curvgrid



def centroid(pts: List[Point]) -> Point:
    arr = np.asarray(pts)
    return tuple(arr.mean(axis=0))


def to_polar(pts: List[Point], C: Point):
    arr = np.asarray(pts) - np.asarray(C)
    r = np.linalg.norm(arr, axis=1)
    theta = (np.arctan2(arr[:,1], arr[:,0]) + 2*np.pi) % (2*np.pi)
    return r.tolist(), theta.tolist()


def gao_spiral_v4_fib_weave(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v4 — Fibonacci-Woven Spiral
    - Fibonacci-weighted θ×r lattice (Textura activation)
    - Weave modulation: twill beats + plain-weave alternation (Ecologia↔Textura resonance)
    - Optional twill look-ahead buffer (diagonal continuity)
    Runtime: ~O(n log n) typical with local neighborhoods
    """

    # ---------- Setup ----------
    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r); theta = np.array(theta)
    r_max = float(r.max() + 1e-9)
    phi = (1 + 5**0.5) / 2
    golden = math.tau * (1 - 1/phi)  # ≈ 137.5°
    alpha = 0.0

    # Lattice sizes
    Bθ = params.bins or max(16, int(2.5 * math.sqrt(n)))
    # Radial bands via Fibonacci cumulative spacing (alive texture)
    fib = np.array([1,1,2,3,5,8,13,21,34,55], dtype=float)
    # choose enough bands but cap to sqrt(n)
    Br = min(max(12, int(math.sqrt(n))+2), len(fib)+6)
    # build cumulative fib up to Br, then normalize to r_max
    f = np.pad(fib, (0, max(0, Br - len(fib))), mode='edge')[:Br]
    f_cum = np.cumsum(f)
    r_bounds = (f_cum / f_cum[-1]) * r_max  # Br bands expanding with fib law

    # θ×r bins
    bins = [[[] for _ in range(Br)] for _ in range(Bθ)]
    def r_to_br(rv: float) -> int:
        # locate fib band
        return min(int(np.searchsorted(r_bounds, rv, side='right')), Br-1)
    for i in range(n):
        bθ = int((theta[i] / (2*np.pi)) * Bθ) % Bθ
        br = r_to_br(r[i])
        bins[bθ][br].append(i)

    visited = [False]*n
    current = int(np.argmin(r))   # start near center
    tour: List[int] = []

    # Feedback + adaptivity parameters (inherit v3.2 spirit)
    # Phase control
    k_r, k_den, k_phase = 0.35, 0.25, 0.40
    phi_clamp = 0.20
    ema_r = 0.0; ema_dtheta = golden
    ema_r_beta = 0.78; ema_theta_beta = 0.78

    # Flow/texture couplings (v3.2 tuned base)
    k_q = 0.25         # adaptive quantile softness
    k_curv = 0.06      # gentle curvature moderation

    # Weave modulation
    k_twill = max(7, int(0.5*math.sqrt(n)))     # twill beat period
    twill_offset = golden / 3.0                 # small phase nudge
    plain_alt_bias = 0.06                       # mild +/- angular sign bias
    last_band = r_to_br(r[current]); weave_sign = 1

    # Scale refs
    # robust neighbor scale estimate
    sample = min(n, 60)
    nn_scale = np.median([
        np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
        for i in range(sample) for j in range(i+1, sample)
    ]) or 1.0
    r_med = float(np.median(r)) or 1.0
    tau0, grow = 0.25*nn_scale, 1.8

    def ang_diff(a, b):
        d = abs(a - b) % (2*np.pi)
        return min(d, 2*np.pi - d)

    def local_density(bθ_c, br_c):
        total = 0; cells = 0
        for dθ in range(-2, 3):
            for dr in range(-1, 2):
                iθ = (bθ_c + dθ) % Bθ
                ir = min(max(br_c + dr, 0), Br-1)
                total += len(bins[iθ][ir]); cells += 1
        mean_bin = n / (Bθ*Br)
        return (total/max(1, cells)) / max(1e-9, mean_bin)  # ~1 at average

    # Optional: tiny look-ahead (L=1) to preserve diagonal trend (twill feel)
    L_look = 1

    def choose_candidate(alpha, current, last_sign, prev_dr, ema_dtheta, step):
        bθ = int((alpha / (2*np.pi)) * Bθ) % Bθ
        br = r_to_br(r[current])
        den_sig = local_density(bθ, br)

        # neighborhood
        cand_pool = []
        for dθ in range(-3, 4):
            for dr in range(-2, 3):
                iθ = (bθ + dθ) % Bθ
                ir = min(max(br + dr, 0), Br-1)
                cand_pool.extend([idx for idx in bins[iθ][ir] if not visited[idx]])
        if not cand_pool:
            return None

        # radial band within tolerance
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt; break
            tau *= grow
        if not cand_pool:
            return None

        # adaptive quantile on |Δr|
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        q = max(0.25, min(0.8, 0.6 * (1 - k_q * (den_sig - 1.0))))
        thr = np.quantile(drs, q)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # Fibonacci angular weight: inner rings get stronger angular discipline
        #   (r/r_max)^(1/phi) ∈ (0,1) → scales angular term higher near center, softer at edge.
        tex_fib_weight = (max(1e-9, r[current]) / r_max) ** (1.0/phi)

        # Plain-weave alternation bias: flip sign when crossing band boundaries
        nonlocal last_band, weave_sign
        cur_band = r_to_br(r[current])
        if cur_band != last_band:
            weave_sign *= -1
            last_band = cur_band

        def penalties(j):
            # momentum + curvature moderation
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_penalty = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            curv_penalty = k_curv * abs(ang_diff(theta[j], alpha) - ema_dtheta) / golden
            # plain-weave bias: small push toward current weave_sign
            # favor candidates whose angular delta agrees with bias
            angle_to_alpha = (theta[j] - alpha + 2*np.pi) % (2*np.pi)
            angle_sign = 1 if angle_to_alpha < np.pi else -1
            weave_penalty = 0.0 if angle_sign == weave_sign else 0.03
            return base + amp_penalty + curv_penalty + weave_penalty

        # tiny twill look-ahead (L=1): prefer candidates that keep Δθ near ema_dtheta
        def lookahead_cost(j):
            dθ_now = ang_diff(theta[j], alpha)
            return abs(dθ_now - ema_dtheta) / golden

        cand = min(
            pool,
            key=lambda j: (
                params.w_theta * tex_fib_weight * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + penalties(j)
                + (0.05 * lookahead_cost(j) if L_look == 1 else 0.0)
            )
        )
        return (cand, den_sig)

    # ---------- Main loop ----------
    visited[current] = True
    tour.append(current)
    last_sign, prev_dr = 0, 0.0

    for step in range(1, n):
        # periodic twill beat (phase nudge)
        if step % k_twill == 0:
            alpha = (alpha + twill_offset) % (2*np.pi)

        out = choose_candidate(alpha, current, last_sign, prev_dr, ema_dtheta, step)
        if out is None:
            # graceful fallback: any remaining nearest unvisited
            rem = [i for i in range(n) if not visited[i]]
            if not rem: break
            cand = min(rem, key=lambda j: np.linalg.norm(np.asarray(pts[j]) - np.asarray(pts[current])))
            den_sig = 1.0
        else:
            cand, den_sig = out

        d_r = abs(r[cand] - r[current])
        d_theta_est = ang_diff(theta[cand], alpha)
        ema_r = ema_r_beta * ema_r + (1 - ema_r_beta) * d_r
        ema_dtheta = ema_theta_beta * ema_dtheta + (1 - ema_theta_beta) * d_theta_est

        # adaptive phase (as in v3.2)
        flow_term =  k_r * (ema_r / max(1e-9, nn_scale))
        density_term = k_den * (den_sig - 1.0)
        phase_err = (golden - ema_dtheta) / max(1e-9, golden)
        phase_term = k_phase * phase_err
        control = max(-phi_clamp, min(phi_clamp, flow_term + density_term + phase_term))
        phi_t = golden * (1.0 + control)
        alpha = (alpha + phi_t) % (2*np.pi)

        last_sign = np.sign(r[cand] - r[current])
        prev_dr = d_r
        current = cand
        visited[current] = True
        tour.append(current)

    # repair uniqueness if needed
    seen = set(); uniq = []
    for i in tour:
        if i not in seen:
            uniq.append(i); seen.add(i)
    if len(uniq) < n:
        uniq.extend([i for i in range(n) if i not in seen])
    return uniq


def gao_spiral_v5_dynamic_weave(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v5 — Dynamic Fibonacci Weave
      • Dynamic golden angle φ(t) = φ0 * (1 + ε*sin(ω t))  (Ecologia breathing)
      • Soft Fibonacci radial bands (Gaussian membership, no hard walls)  (Textura alive)
      • Stronger twill drift (periodic phase nudge) + plain-weave alternation on band crossings
      • Adaptive quantile on |Δr|, gentle curvature moderation, robust fallbacks
    """

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r); theta = np.array(theta)
    r_max = float(r.max() + 1e-9)

    phi = (1 + 5**0.5) / 2
    phi0 = math.tau * (1 - 1/phi)  # ~137.5°
    alpha = 0.0

    # ---------------- Lattice (θ×r) ----------------
    Bθ = params.bins or max(16, int(2.5 * math.sqrt(n)))
    Br_target = max(12, int(math.sqrt(n)) + 2)

    # Fibonacci cumulative boundaries (base)
    fib = np.array([1,1,2,3,5,8,13,21,34,55,89], dtype=float)
    fib = np.pad(fib, (0, max(0, Br_target - len(fib))), mode='edge')[:Br_target]
    fib_c = np.cumsum(fib); fib_c = fib_c / fib_c[-1] * r_max
    Br = len(fib_c)

    # Prebin only by angle for locality; radial is handled softly
    binsθ = [[] for _ in range(Bθ)]
    for i in range(n):
        bθ = int((theta[i] / (2*np.pi)) * Bθ) % Bθ
        binsθ[bθ].append(i)

    visited = [False]*n
    current = int(np.argmin(r))  # start near center
    tour: List[int] = [current]
    visited[current] = True

    # ---------------- Feedback / runtime helpers ----------------
    # Local density via angular neighborhood counts (fast)
    def local_density(bθ_c: int) -> float:
        total = 0; cells = 0
        for dθ in (-2,-1,0,1,2):
            total += sum(1 for idx in binsθ[(bθ_c + dθ) % Bθ] if not visited[idx])
            cells += 1
        mean_bin = n / Bθ
        return (total/max(1,cells)) / max(1e-9, mean_bin)  # ~1 at average

    # Soft Fibonacci band membership weight for candidate j at radius rj:
    # Gaussian around closest fib boundary → smooth band influence (no walls)
    sigma_r = max(1e-9, 0.12 * (r_max / math.sqrt(Br)))  # soft width ~12% of avg band
    def fib_soft_weight(rj: float) -> float:
        # distance to nearest fib boundary
        d = np.min(np.abs(fib_c - rj))
        # higher weight near boundary to encourage smooth inter-band weaving
        return math.exp(-(d*d) / (2*sigma_r*sigma_r))

    # Mild curvature moderation (keeps rhythm coherent)
    k_curv = 0.05

    # Adaptive quantile softness (lets |Δr| breathe)
    k_q = 0.25

    # Phase controller (as in v3.2) + dynamic φ(t)
    k_r, k_den, k_phase = 0.35, 0.25, 0.40
    phi_clamp = 0.20
    ema_r, ema_dtheta = 0.0, phi0
    # ema_r_beta, ema_theta_beta = 0.78, 0.78

    # Dynamic φ(t) params (Ecologia breathing)
    # eps_phi = 0.10     # ±10% modulation
    omega_phi = 2 * math.pi / max(10, int(0.6*math.sqrt(n)))  # slow wave vs steps

    # Weave modulation (twill drift + plain-weave alternation)
    k_twill = max(6, int(0.45 * math.sqrt(n)))     # beat period
    # twill_offset = 0.12 * phi0                      # ~12% of golden
    weave_sign = 1
    last_band_idx = int(np.searchsorted(fib_c, r[current], side='right'))

    # --- parameter retunes ---
    eps_phi = 0.05  # gentler breathing (was 0.10)
    twill_offset = 0.08 * phi0  # smaller twill drift (was 0.12)
    sigma_r = 0.20 * (r_max / math.sqrt(Br))  # wider band overlap (was 0.12)
    ema_r_beta = 0.74
    ema_theta_beta = 0.74

    # Scales
    sample = min(n, 60)
    nn_scale = np.median([
        np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
        for i in range(sample) for j in range(i+1, sample)
    ]) or 1.0
    r_med = float(np.median(r)) or 1.0
    tau0, grow = 0.25*nn_scale, 1.8

    def ang_diff(a, b):
        d = abs(a-b) % (2*np.pi)
        return min(d, 2*np.pi - d)

    # -------- Candidate chooser (soft bands, twill-aware) --------
    def choose_candidate(step, alpha, current, last_sign, prev_dr, ema_dtheta):
        bθ = int((alpha / (2*np.pi)) * Bθ) % Bθ
        den_sig = local_density(bθ)

        # Collect angular neighborhood (±3 bins)
        cand_pool = []
        for dθ in (-3,-2,-1,0,1,2,3):
            cand_pool.extend([idx for idx in binsθ[(bθ + dθ) % Bθ] if not visited[idx]])
        if not cand_pool:
            return None

        # Gentle radial tolerance funnel
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt; break
            tau *= grow
        if not cand_pool:
            return None

        # Adaptive quantile on |Δr|
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        q = max(0.25, min(0.8, 0.6 * (1 - k_q * (den_sig - 1.0))))
        thr = np.quantile(drs, q)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # Plain-weave alternation on band crossings (toggle sign near new band)
        nonlocal weave_sign, last_band_idx
        cur_band_idx = int(np.searchsorted(fib_c, r[current], side='right'))
        if cur_band_idx != last_band_idx:
            weave_sign *= -1
            last_band_idx = cur_band_idx

        def penalties(j):
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_pen = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            curv = k_curv * abs(ang_diff(theta[j], alpha) - ema_dtheta) / phi0
            # encourage angular move agreeing with current weave_sign
            angle_to_alpha = (theta[j] - alpha + 2*np.pi) % (2*np.pi)
            angle_sign = 1 if angle_to_alpha < np.pi else -1
            weave_pen = 0.0 if angle_sign == weave_sign else 0.03
            # soft Fibonacci weight (higher near band edges to blend rings)
            # band_soft = 1.0 - 0.15 * fib_soft_weight(r[j])  # ≤15% relief near edges
            # in penalties(): soften band term
            band_soft = 1.0 - 0.06 * fib_soft_weight(r[j])  # was 0.15
            return base + amp_pen + curv + weave_pen + band_soft

        # Fibonacci angular discipline: stronger near center, softer outward (dynamic)
        # dynamic exponent via φ(t): (r/r_max)^(1/φ(t))
        phi_t_dyn = phi * (1 + 0.15 * math.sin(omega_phi * step))
        tex_fib = (max(1e-9, r[current]) / r_max) ** (1.0 / phi_t_dyn)

        cand = min(
            pool,
            key=lambda j: (
                params.w_theta * tex_fib * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + penalties(j)
            )
        )
        return (cand, den_sig)

    # ---------------- Main spiral growth ----------------
    last_sign, prev_dr = 0, 0.0
    for step in range(1, n):
        # Stronger twill drift (periodic phase nudge)
        if step % k_twill == 0:
            alpha = (alpha + twill_offset) % (2*np.pi)

        out = choose_candidate(step, alpha, current, last_sign, prev_dr, ema_dtheta)
        if out is None:
            # graceful fallback: nearest unvisited in Euclidean space
            remaining = [i for i in range(n) if not visited[i]]
            if not remaining: break
            cand = min(remaining, key=lambda j: np.linalg.norm(np.asarray(pts[j]) - np.asarray(pts[current])))
            den_sig = 1.0
        else:
            cand, den_sig = out

        # Flow feedback updates
        d_r = abs(r[cand] - r[current])
        d_theta_est = ang_diff(theta[cand], alpha)
        ema_r = ema_r_beta * ema_r + (1 - ema_r_beta) * d_r
        ema_dtheta = ema_theta_beta * ema_dtheta + (1 - ema_theta_beta) * d_theta_est

        # Dynamic φ(t) (breathing)
        phi_breathe = phi0 * (1.0 + eps_phi * math.sin(omega_phi * step))

        # Phase controller (as v3.2 but with breathing φ)
        flow_term  = k_r * (ema_r / max(1e-9, nn_scale))
        density_term = k_den * (den_sig - 1.0)
        phase_err = (phi_breathe - ema_dtheta) / max(1e-9, phi_breathe)
        phase_term = k_phase * phase_err
        control = max(-phi_clamp, min(phi_clamp, flow_term + density_term + phase_term))
        # --- Optional: fine-weave phase damping ---
        # Prevent over-strong corrective swings in the breathing loop
        if abs(control) > 0.15:
            control *= 0.8
        phi_step = phi_breathe * (1.0 + control)

        alpha = (alpha + phi_step) % (2*np.pi)

        last_sign = np.sign(r[cand] - r[current])
        prev_dr = d_r
        current = cand
        visited[current] = True
        tour.append(current)

    # Uniqueness repair
    seen, uniq = set(), []
    for i in tour:
        if i not in seen:
            uniq.append(i); seen.add(i)
    if len(uniq) < n:
        uniq.extend([i for i in range(n) if i not in seen])
    return uniq



def gao_spiral_v6_adaptive_weave(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    """
    GAO Spiral v6 — Adaptive Breathing Weave
      • φ(t) amplitude ε_t responds to recent Var(|Δr|)
      • Dynamic Textura band_weights from live occupancy of unvisited radii
      • Soft Fibonacci bands retained; twill & weave alternation kept gentle
      • Robust fallbacks; v3.2-class runtime

    Expected (n≈200 first pass):
      Dualitas ~0.94–0.95
      Adaptatio ~0.56–0.64
      Textura   ~0.61–0.66
      Ecologia  ~0.22–0.27
      Overall   ~0.63–0.70
    """
    import math, numpy as np

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r); theta = np.array(theta)
    r_max = float(r.max() + 1e-9)

    phi = (1 + 5**0.5) / 2
    phi0 = math.tau * (1 - 1/phi)
    alpha = 0.0

    # ---------- Lattice: angle bins + Fibonacci radial references ----------
    Bθ = params.bins or max(16, int(2.5 * math.sqrt(n)))
    Br_target = max(12, int(math.sqrt(n)) + 2)
    fib = np.array([1,1,2,3,5,8,13,21,34,55,89], dtype=float)
    fib = np.pad(fib, (0, max(0, Br_target - len(fib))), mode='edge')[:Br_target]
    fib_c = np.cumsum(fib); fib_c = fib_c / fib_c[-1] * r_max
    Br = len(fib_c)

    # Angular bins only (fast locality); radial is soft + weighted
    binsθ = [[] for _ in range(Bθ)]
    for i in range(n):
        bθ = int((theta[i] / (2*np.pi)) * Bθ) % Bθ
        binsθ[bθ].append(i)

    visited = [False]*n
    current = int(np.argmin(r))
    visited[current] = True
    tour: List[int] = [current]

    # ---------- Feedback params ----------
    # Phase controller (as v3.2 baseline)
    k_r, k_den, k_phase = 0.35, 0.25, 0.40
    phi_clamp = 0.20
    ema_r, ema_dtheta = 0.0, phi0
    ema_r_beta, ema_theta_beta = 0.65, 0.65  # shorter memory to re-energize flow

    # Adaptive φ(t) amplitude via recent Var(|Δr|)
    eps0 = 0.05                 # base amplitude
    ema_var_beta = 0.80
    var_dr = 0.0                # EW variance of |Δr|
    # breathing frequency
    omega_phi = 2 * math.pi / max(10, int(0.6 * math.sqrt(n)))

    # Twill & weave alternation (mild)
    k_twill = max(6, int(0.45 * math.sqrt(n)))
    twill_offset = 0.08 * phi0
    weave_sign = 1
    last_band_idx = int(np.searchsorted(fib_c, r[current], side='right'))

    # Soft-band Gaussian width (broader overlap)
    sigma_r = 0.20 * (r_max / math.sqrt(Br))

    def fib_soft_weight(rv: float) -> float:
        d = np.min(np.abs(fib_c - rv))
        return math.exp(-(d*d) / (2 * sigma_r * sigma_r))

    # Dynamic Textura band weights (regridded)
    band_weights = np.ones(Br)  # start neutral
    k_regrid = max(8, int(0.4 * math.sqrt(n)))   # how often to re-estimate
    bw_clip = (0.85, 1.20)                       # keep weights stable

    # Scales
    sample = min(n, 60)
    nn_scale = np.median([
        np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
        for i in range(sample) for j in range(i+1, sample)
    ]) or 1.0
    r_med = float(np.median(r)) or 1.0
    tau0, grow = 0.25*nn_scale, 1.8

    def ang_diff(a, b):
        d = abs(a - b) % (2*np.pi)
        return min(d, 2*np.pi - d)

    def local_density(bθ_c: int) -> float:
        total = 0; cells = 0
        for dθ in (-2,-1,0,1,2):
            total += sum(1 for idx in binsθ[(bθ_c + dθ) % Bθ] if not visited[idx])
            cells += 1
        mean_bin = n / Bθ
        return (total/max(1,cells)) / max(1e-9, mean_bin)

    def current_band_idx(rv: float) -> int:
        return int(np.searchsorted(fib_c, rv, side='right'))

    # ---------- Candidate selection ----------
    def choose_candidate(step, alpha, current, last_sign, prev_dr, ema_dtheta):
        bθ = int((alpha / (2*np.pi)) * Bθ) % Bθ
        den_sig = local_density(bθ)

        # Angular neighborhood
        cand_pool = []
        for dθ in (-3,-2,-1,0,1,2,3):
            cand_pool.extend([idx for idx in binsθ[(bθ + dθ) % Bθ] if not visited[idx]])
        if not cand_pool:
            return None

        # Soft radial funnel
        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j] - r[current]) <= tau]
            if filt:
                cand_pool = filt; break
            tau *= grow
        if not cand_pool:
            return None

        # Adaptive quantile on |Δr|
        k_q = 0.25
        drs = np.array([abs(r[j] - r[current]) for j in cand_pool])
        q = max(0.25, min(0.8, 0.6 * (1 - k_q * (den_sig - 1.0))))
        thr = np.quantile(drs, q)
        pool = [j for j, dj in zip(cand_pool, drs) if dj <= thr] or cand_pool

        # Weave alternation on ring crossings
        nonlocal weave_sign, last_band_idx
        cur_b = current_band_idx(r[current])
        if cur_b != last_band_idx:
            weave_sign *= -1
            last_band_idx = cur_b

        # Penalties + soft-band, plus dynamic band weight for angular term
        def penalties(j):
            s = np.sign(r[j] - r[current])
            base = 0.1 if (last_sign != 0 and s != last_sign) else 0.0
            amp_pen = abs(abs(r[j] - r[current]) - prev_dr) * 0.1
            curv = 0.05 * abs(ang_diff(theta[j], alpha) - ema_dtheta) / phi0
            # weave sign encouragement
            angle_to_alpha = (theta[j] - alpha + 2*np.pi) % (2*np.pi)
            angle_sign = 1 if angle_to_alpha < np.pi else -1
            weave_pen = 0.0 if angle_sign == weave_sign else 0.03
            # soft Fibonacci relief near band edges (lighter than v5)
            band_soft = 1.0 - 0.06 * fib_soft_weight(r[j])
            return base + amp_pen + curv + weave_pen + band_soft

        # Angular discipline with live band weight (Textura feedback)
        band_w = band_weights[cur_b]  # >1 tightens angle; <1 loosens
        tex_scale = band_w * (max(1e-9, r[current]) / r_max) ** (1.0 / phi)  # inner tighter

        cand = min(
            pool,
            key=lambda j: (
                params.w_theta * tex_scale * ang_diff(theta[j], alpha)
                + params.w_r * abs(r[j] - r[current]) / max(1e-9, r_med)
                + penalties(j)
            )
        )
        return (cand, den_sig)

    # ---------- Main growth ----------
    last_sign, prev_dr = 0, 0.0

    for step in range(1, n):
        # Slight twill drift
        if step % k_twill == 0:
            alpha = (alpha + twill_offset) % (2*np.pi)

        # Live Textura regrid
        if step % k_regrid == 0:
            # estimate occupancy per ring from unvisited points
            rem_idx = [i for i in range(n) if not visited[i]]
            if rem_idx:
                ring_ids = np.searchsorted(fib_c, r[rem_idx], side='right')
                occ = np.bincount(ring_ids, minlength=Br).astype(float) + 1.0  # +1 avoid zero
                occ_norm = occ / occ.mean()
                new_bw = 1.0 / occ_norm                      # dense→tighten (>1), sparse→loosen (<1)
                new_bw = np.clip(new_bw, *bw_clip)
                # smooth update to avoid jitter
                band_weights = 0.7 * band_weights + 0.3 * new_bw

        out = choose_candidate(step, alpha, current, last_sign, prev_dr, ema_dtheta)
        if out is None:
            rem = [i for i in range(n) if not visited[i]]
            if not rem: break
            cand = min(rem, key=lambda j: np.linalg.norm(np.asarray(pts[j]) - np.asarray(pts[current])))
            den_sig = 1.0
        else:
            cand, den_sig = out

        # Flow observations
        d_r = abs(r[cand] - r[current])
        d_theta_est = ang_diff(theta[cand], alpha)

        # EW variance of |Δr|
        var_dr = ema_var_beta * var_dr + (1 - ema_var_beta) * (d_r - ema_r)**2
        ema_r = ema_r_beta * ema_r + (1 - ema_r_beta) * d_r
        ema_dtheta = ema_theta_beta * ema_dtheta + (1 - ema_theta_beta) * d_theta_est

        # Adaptive breathing amplitude ε_t (bounded)
        eps_dyn = eps0 * math.tanh(var_dr / max(1e-9, (0.5 * sigma_r)**2))
        phi_breathe = phi0 * (1.0 + eps_dyn * math.sin(omega_phi * step))

        # Phase controller with breathing φ
        flow_term   = k_r   * (ema_r / max(1e-9, nn_scale))
        density_term= k_den * (den_sig - 1.0)
        phase_err   = (phi_breathe - ema_dtheta) / max(1e-9, phi_breathe)
        phase_term  = k_phase * phase_err
        control = max(-phi_clamp, min(phi_clamp, flow_term + density_term + phase_term))

        # Optional: damp rare overcorrections
        if abs(control) > 0.15:
            control *= 0.8

        phi_step = phi_breathe * (1.0 + control)
        alpha = (alpha + phi_step) % (2*np.pi)

        last_sign = np.sign(r[cand] - r[current])
        prev_dr = d_r
        current = cand
        visited[current] = True
        tour.append(current)

    # Uniqueness repair
    seen, uniq = set(), []
    for i in tour:
        if i not in seen:
            uniq.append(i); seen.add(i)
    if len(uniq) < n:
        uniq.extend([i for i in range(n) if i not in seen])
    return uniq


def gao_spiral_v6_adaptive_weave_2(pts: List[Point], params: GAOParams = GAOParams()) -> Tour:
    import math, numpy as np

    n = len(pts)
    C = centroid(pts)
    r, theta = to_polar(pts, C)
    r = np.array(r); theta = np.array(theta)
    r_max = float(r.max() + 1e-9)

    phi = (1 + 5**0.5) / 2
    phi0 = math.tau * (1 - 1/phi)
    alpha = 0.0

    # ---------- lattice ----------
    Bθ = params.bins or max(16, int(2.5 * math.sqrt(n)))
    Br_target = max(12, int(math.sqrt(n)) + 2)
    fib = np.array([1,1,2,3,5,8,13,21,34,55,89], dtype=float)
    fib = np.pad(fib, (0, max(0, Br_target - len(fib))), mode='edge')[:Br_target]
    fib_c = np.cumsum(fib); fib_c = fib_c / fib_c[-1] * r_max
    Br = len(fib_c)

    binsθ = [[] for _ in range(Bθ)]
    for i in range(n):
        bθ = int((theta[i] / (2*np.pi)) * Bθ) % Bθ
        binsθ[bθ].append(i)

    visited = [False]*n
    current = int(np.argmin(r))
    visited[current] = True
    tour = [current]

    # ---------- feedback ----------
    k_r, k_den, k_phase = 0.35, 0.25, 0.40
    phi_clamp = 0.20
    ema_r, ema_dtheta = 0.0, phi0
    ema_r_beta, ema_theta_beta = 0.65, 0.65
    eps0 = 0.05
    ema_var_beta = 0.80; var_dr = 0.0
    omega_phi = 2 * math.pi / max(10, int(0.6*math.sqrt(n)))

    # Twill / weave alternation
    k_twill = max(6, int(0.45 * math.sqrt(n)))
    twill_offset = 0.08 * phi0
    weave_sign = 1
    last_band_idx = int(np.searchsorted(fib_c, r[current], side='right'))

    sigma_r = 0.20 * (r_max / math.sqrt(Br))

    def fib_soft_weight(rv):
        d = np.min(np.abs(fib_c - rv))
        return math.exp(-(d*d) / (2*sigma_r*sigma_r))

    band_weights = np.ones(Br)
    k_regrid = max(8, int(0.4 * math.sqrt(n)))
    bw_clip = (0.85, 1.20)

    sample = min(n, 60)
    nn_scale = np.median([
        np.linalg.norm(np.asarray(pts[i]) - np.asarray(pts[j]))
        for i in range(sample) for j in range(i+1, sample)
    ]) or 1.0
    r_med = float(np.median(r)) or 1.0
    tau0, grow = 0.25*nn_scale, 1.8

    def ang_diff(a,b):
        d = abs(a-b) % (2*np.pi)
        return min(d, 2*np.pi - d)

    def local_density(bθ_c):
        total = 0
        for dθ in (-2,-1,0,1,2):
            total += sum(1 for idx in binsθ[(bθ_c + dθ) % Bθ] if not visited[idx])
        mean_bin = n / Bθ
        return (total/5) / max(1e-9, mean_bin)

    def current_band_idx(rv): return int(np.searchsorted(fib_c, rv, side='right'))

    # ---------- candidate ----------
    def choose_candidate(step, alpha, current, last_sign, prev_dr, ema_dtheta):
        nonlocal weave_sign, last_band_idx
        # --- Weave modes -------------
        if params.weave_mode == "bias":
            theta_shift = params.bias_rate * step
            bθ = int(((alpha + theta_shift) % (2*np.pi)) / (2*np.pi) * Bθ) % Bθ
        elif params.weave_mode == "elastic":
            bθ = int((alpha / (2*np.pi)) * Bθ) % Bθ
            den_sig = local_density(bθ)
            Bθ_eff = int(Bθ * (1 - params.k_elast * (den_sig - 1)))
            Bθ_eff = max(6, min(3*int(np.sqrt(n)), Bθ_eff))
            bθ = int((alpha / (2*np.pi)) * Bθ_eff) % Bθ_eff
        else:
            bθ = int((alpha / (2*np.pi)) * Bθ) % Bθ
        # -----------------------------

        den_sig = local_density(bθ)
        cand_pool = []
        for dθ in (-3,-2,-1,0,1,2,3):
            cand_pool.extend([idx for idx in binsθ[(bθ + dθ) % Bθ] if not visited[idx]])
        if not cand_pool: return None

        tau = tau0
        for _ in range(3):
            filt = [j for j in cand_pool if abs(r[j]-r[current]) <= tau]
            if filt: cand_pool=filt; break
            tau*=grow
        if not cand_pool: return None

        k_q=0.25
        drs=np.array([abs(r[j]-r[current]) for j in cand_pool])
        q=max(0.25,min(0.8,0.6*(1-k_q*(den_sig-1.0))))
        thr=np.quantile(drs,q)
        pool=[j for j,dj in zip(cand_pool,drs) if dj<=thr] or cand_pool

        cur_b=current_band_idx(r[current])
        if cur_b!=last_band_idx:
            weave_sign*=-1; last_band_idx=cur_b

        def penalties(j):
            s=np.sign(r[j]-r[current])
            base=0.1 if (last_sign!=0 and s!=last_sign) else 0.0
            amp_pen=abs(abs(r[j]-r[current])-prev_dr)*0.1
            curv=0.05*abs(ang_diff(theta[j],alpha)-ema_dtheta)/phi0
            angle_to_alpha=(theta[j]-alpha+2*np.pi)%(2*np.pi)
            angle_sign=1 if angle_to_alpha<np.pi else -1
            weave_pen=0.0 if angle_sign==weave_sign else 0.03
            band_soft=1.0-0.06*fib_soft_weight(r[j])
            return base+amp_pen+curv+weave_pen+band_soft

        # curvature-mode dynamic bands
        if params.weave_mode == "curvature":
            curv_term = params.k_curvgrid * abs(ema_dtheta - phi0) / phi0
            fib_c_shift = fib_c * (1 + curv_term)
            cur_b = int(np.searchsorted(fib_c_shift, r[current], side='right'))

        band_w = band_weights[cur_b]
        tex_scale = band_w * (max(1e-9, r[current])/r_max)**(1.0/phi)

        cand=min(pool,key=lambda j:
                 params.w_theta*tex_scale*ang_diff(theta[j],alpha)
                +params.w_r*abs(r[j]-r[current])/max(1e-9,r_med)
                +penalties(j))
        return (cand,den_sig)

    # ---------- main ----------
    last_sign, prev_dr = 0, 0.0
    for step in range(1,n):
        if step % k_twill == 0:
            alpha = (alpha + twill_offset) % (2*np.pi)

        if step % k_regrid == 0:
            rem_idx=[i for i in range(n) if not visited[i]]
            if rem_idx:
                ring_ids=np.searchsorted(fib_c,r[rem_idx],side='right')
                occ=np.bincount(ring_ids,minlength=Br).astype(float)+1.0
                occ_norm=occ/occ.mean()
                new_bw=np.clip(1.0/occ_norm,*bw_clip)
                band_weights=0.7*band_weights+0.3*new_bw

        out=choose_candidate(step,alpha,current,last_sign,prev_dr,ema_dtheta)
        if out is None:
            rem=[i for i in range(n) if not visited[i]]
            if not rem: break
            cand=min(rem,key=lambda j:np.linalg.norm(np.asarray(pts[j])-np.asarray(pts[current])))
            den_sig=1.0
        else: cand,den_sig=out

        d_r=abs(r[cand]-r[current])
        d_theta_est=abs(theta[cand]-alpha)
        var_dr=ema_var_beta*var_dr+(1-ema_var_beta)*(d_r-ema_r)**2
        ema_r=ema_r_beta*ema_r+(1-ema_r_beta)*d_r
        ema_dtheta=ema_theta_beta*ema_dtheta+(1-ema_theta_beta)*d_theta_est
        eps_dyn=eps0*math.tanh(var_dr/max(1e-9,(0.5*sigma_r)**2))
        phi_breathe=phi0*(1.0+eps_dyn*math.sin(omega_phi*step))
        flow_term=k_r*(ema_r/max(1e-9,nn_scale))
        density_term=k_den*(den_sig-1.0)
        phase_err=(phi_breathe-ema_dtheta)/max(1e-9,phi_breathe)
        phase_term=k_phase*phase_err
        control=max(-phi_clamp,min(phi_clamp,flow_term+density_term+phase_term))
        if abs(control)>0.15: control*=0.8
        phi_step=phi_breathe*(1.0+control)
        alpha=(alpha+phi_step)%(2*np.pi)
        last_sign=np.sign(r[cand]-r[current])
        prev_dr=d_r
        current=cand
        visited[current]=True
        tour.append(current)

    # repair uniqueness
    seen=set(); uniq=[]
    for i in tour:
        if i not in seen:
            uniq.append(i); seen.add(i)
    if len(uniq)<n:
        uniq.extend([i for i in range(n) if i not in seen])
    return uniq



def gao_spiral_v7_hierarchical(pts: List[Point], params: GAOParams = GAOParams(), k_clusters: int = 5) -> Tour:
    n = len(pts)
    pts_arr = np.array(pts)
    # --- cluster step ---
    kmeans = KMeans(n_clusters=k_clusters, n_init=5, random_state=0).fit(pts_arr)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_.tolist()

    # --- local spirals ---
    local_tours = []
    index_map = {}
    for c in range(k_clusters):
        cluster_idx = np.where(labels==c)[0]
        sub_pts = pts_arr[cluster_idx].tolist()
        local_params = GAOParams(**vars(params))  # preserve weave settings per cluster
        sub_tour = gao_spiral_v6_adaptive_weave(sub_pts, local_params)
        # map local order to global indices
        local_tours.append([cluster_idx[i] for i in sub_tour])
        index_map[c] = cluster_idx

    # --- meta-spiral connecting cluster centroids ---
    meta_tour = gao_spiral_v6_adaptive_weave(centroids, params)
    # flatten to full path
    tour = []
    for c in meta_tour:
        tour.extend(local_tours[c])
    return tour



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
