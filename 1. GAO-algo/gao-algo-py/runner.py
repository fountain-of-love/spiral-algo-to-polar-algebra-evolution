
# runner.py
# Reproducible experiments for GAO Spiral vs baselines.
# Generates datasets, runs algorithms, and writes CSVs.

import os, csv, json, math, random, time
from typing import List, Tuple, Dict, Any
import numpy as np
from gao_spiral import (
    Point, Tour, GAOParams, gao_spiral, gao_spiral_v6_adaptive_weave,
    nearest_neighbor, cheapest_insertion, sweep_then_connect,
    evaluate_algorithm
)

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)

def gen_uniform(n: int) -> List[Point]:
    return [(random.random(), random.random()) for _ in range(n)]

def gen_clusters(n: int, k: int = 5, spread: float = 0.05) -> List[Point]:
    centers = [(random.random(), random.random()) for _ in range(k)]
    pts = []
    per = n // k
    for cx, cy in centers:
        for _ in range(per):
            x = random.gauss(cx, spread)
            y = random.gauss(cy, spread)
            # clamp to [0,1]
            x = max(0.0, min(1.0, x)); y = max(0.0, min(1.0, y))
            pts.append((x,y))
    while len(pts) < n:
        pts.append((random.random(), random.random()))
    return pts

def gen_grid_jitter(n_side: int, jitter: float = 0.02) -> List[Point]:
    pts = []
    for i in range(n_side):
        for j in range(n_side):
            x = (i + 0.5)/n_side + random.uniform(-jitter, jitter)
            y = (j + 0.5)/n_side + random.uniform(-jitter, jitter)
            x = max(0.0, min(1.0, x)); y = max(0.0, min(1.0, y))
            pts.append((x,y))
    return pts

def write_csv(path: str, rows: List[Dict[str, Any]], fieldnames: List[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def run_suite(output_dir: str,
              seeds: List[int],
              sizes: List[int],
              two_opt_budget: int = 10000):
    os.makedirs(output_dir, exist_ok=True)
    fieldnames = [
        "dataset","seed","n","algo","build_time_ms","opt_time_ms",
        "init_length","init_crossings","final_length","final_crossings","two_opt_moves"
    ]

    rows = []

    for seed in seeds:

        print("Starting next SEED")

        set_seed(seed)

        # UNIFORM
        for n in sizes:
            pts = gen_uniform(n)
            rows += eval_all("uniform", seed, pts, two_opt_budget)

        print("UNIFORM finished")

        # CLUSTERS
        for n in sizes:
            pts = gen_clusters(n, k=max(3, int(math.sqrt(n)//3) or 3), spread=0.06)
            rows += eval_all("clusters", seed, pts, two_opt_budget)

        print("CLUSTERS finished")

        # GRID+JITTER (square sizes only)
        grid_sizes = [s for s in sizes if int(math.sqrt(s))**2 == s]
        for n in grid_sizes:
            pts = gen_grid_jitter(int(math.sqrt(n)), jitter=0.02)
            rows += eval_all("grid_jitter", seed, pts, two_opt_budget)

        print("GRID+JITTER finished")

    write_csv(os.path.join(output_dir, "results.csv"), rows, fieldnames)

def eval_all(dataset: str, seed: int, pts: List[Point], two_opt_budget: int):
    builders = {
        "GAO": lambda P: gao_spiral(P),
        "GAO v6": lambda P: gao_spiral_v6_adaptive_weave(P),
        "NN":  lambda P: nearest_neighbor(P, start=0),
        "SWEEP": lambda P: sweep_then_connect(P),
        "CI": lambda P: cheapest_insertion(P, start=0),
    }
    rows = []
    n = len(pts)
    for name, builder in builders.items():
        res = evaluate_algorithm(name, builder, pts, run_2opt=True, two_opt_budget=two_opt_budget)
        row = {
            "dataset": dataset,
            "seed": seed,
            "n": n,
            "algo": res["name"],
            "build_time_ms": f"{res['build_time_ms']:.3f}",
            "opt_time_ms": f"{res['opt_time_ms']:.3f}",
            "init_length": f"{res['init_length']:.6f}",
            "init_crossings": res["init_crossings"],
            "final_length": f"{res['final_length']:.6f}",
            "final_crossings": res["final_crossings"],
            "two_opt_moves": res["two_opt_moves"],
        }
        rows.append(row)
    return rows

if __name__ == "__main__":
    # Default quick suite; adjust as needed
    print(f"Starting running tests")
    out = os.path.join(os.getcwd(), "results")
    seeds = [1,2]          # increase for paper-scale
    sizes = [200, 400, 900]  # include a square for grid+jitter
    run_suite(out, seeds, sizes, two_opt_budget=0)
    print(f"Done. Results at: {out}/results.csv")
