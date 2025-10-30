# GAO Spiral – Golden-Angle Greedy Algorithm for Euclidean TSP

MIT-licensed reference implementation accompanying the paper:

> **“The Golden-Angle Greedy Algorithm for the Euclidean Travelling Salesman Problem (GAO Spiral)” (2025)**

---

## 🌻 Overview
GAO Spiral is a **directional greedy heuristic** for the Euclidean Travelling Salesman Problem (TSP).  
Instead of choosing the *nearest* next point (as in Nearest Neighbor), GAO Spiral chooses the point **nearest along a rotating golden-angle direction**—a rule that balances local greediness with global spatial coherence.

- **Input:** 2D coordinates of `n` points  
- **Output:** One TSP tour (a sequence visiting each point exactly once)  
- **Complexity:** O(n log n) expected  
- **Core idea:** “Greedy without chaos”—each step greedily reduces angular disorder, following the golden-angle rotation (≈137.5°).

---

## 🌀 Visual intuition (toy instance)

| Step | Nearest Neighbor | GAO Spiral |
|------|------------------|------------|
| Start at centroid or innermost point | ![Step1](figs/nn_step1.png) | ![Step1](figs/gao_step1.png) |
| After 5 steps | ![Step2](figs/nn_step5.png) | ![Step2](figs/gao_step5.png) |
| After 10 steps | ![Step3](figs/nn_step10.png) | ![Step3](figs/gao_step10.png) |
| Final tour (before 2-opt) | ![NN_final](figs/nn_final.png) | ![GAO_final](figs/gao_final.png) |

*Illustration:* NN tends to zig-zag within local clusters (producing crossings); GAO advances smoothly in angular order, forming a near-spiral layout with minimal crossings.

*(Figures generated with `plots_toy.ipynb`; see appendix for script.)*

---

## ⚙️ Running experiments

```bash
# Install deps (numpy only)
pip install numpy

# Run the benchmark suite
python runner.py

# Results appear in results/results.csv
