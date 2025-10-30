# 📊 Metrics per Run

Each row in `results.csv` corresponds to one algorithm (`algo`) run on one dataset instance (`dataset`, `seed`, `n`). All metrics are numeric except for `dataset`/`algo` labels.

---

## Metric Definitions

| Metric | Meaning | How it’s Computed | Typical Range | “Better” Direction |
| :--- | :--- | :--- | :--- | :--- |
| **build_time_ms** | Construction time in milliseconds | Wall-clock time for building the initial tour (no 2-opt) | 1 – 1000 ms depending on $n$ | **Lower** means faster construction |
| **opt_time_ms** | Time spent in local optimization (2-opt refinement) | Wall-clock time for 2-opt swaps | 10 – 10000 ms depending on budget | **Lower** = faster convergence (if quality comparable) |
| **init_length** | Total length of the initial tour before 2-opt | Sum of Euclidean edge distances | Normalized to problem scale | **Lower** is better |
| **init_crossings** | Number of edge crossings in initial tour | Counts intersecting non-adjacent edges | Typically 0 – hundreds | **Lower** (0 is planar) |
| **final_length** | Length after 2-opt refinement | Same formula after optimization | Should approach or match best-known | **Lower** is better |
| **final_crossings** | Crossings after 2-opt | Usually 0 (2-opt eliminates crossings) | 0 if converged | — (diagnostic) |
| **two_opt_moves** | Number of improving 2-opt swaps performed | Count of accepted swaps during 2-opt loop | 0 – 10000 (depends on budget) | **Lower** means the initial tour was closer to optimal (less to fix) |

---

## 🔍 How to Interpret a Run Across Metrics

This table provides key scenarios to understand the performance profile of an algorithm run by looking at the combination of metric values.

| Situation | What it Means | Typical Cause |
| :--- | :--- | :--- |
| **Low build\_time + Low init\_length + Low init\_crossings** | Efficient and geometrically coherent construction | Well-balanced heuristic (GAO Spiral target) |
| **Low build\_time** but **High init\_crossings / long init\_length** | Fast but chaotic start | Classic Nearest Neighbor behavior |
| **High two\_opt\_moves, large opt\_time** | Many crossings or poor initial geometry → 2-opt has to fix a lot | Sweep or NN on clustered data |
| **Low two\_opt\_moves, similar final\_length** | Good initial order → faster convergence | GAO Spiral’s smooth angular coherence |
| **Lower final\_length** but **higher build\_time** | Costlier construction algorithm (e.g., Cheapest Insertion) achieves slightly better length | Trade-off: build cost vs. tour quality |

---

## Trade-offs Summary

* **Speed vs. quality:** **NN** and **Sweep** build fastest but need heavy 2-opt cleanup. **GAO** builds slower than NN but faster than CI, and converges faster overall.
* **Crossings vs. refinement:** Fewer initial crossings $\implies$ fewer 2-opt moves $\implies$ shorter `opt_time`.
* **Stability vs. randomness:** **GAO** is deterministic; **NN** varies with start point.