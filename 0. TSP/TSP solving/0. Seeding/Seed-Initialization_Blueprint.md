# ⚙️ Stage 0 — Seed Initialization Blueprint

This blueprint details the design, implementation, and evaluation protocol for optimizing the **$\text{Origo}$ (Seed Initialization) stage**, the fundamental step for shaping search entropy and boosting the performance of path-dependent $\text{TSP}$ heuristics.

---

## 1) Seeding Families $\times$ Design Matrix

This matrix classifies seeding methods by their underlying geometric or informational logic, aligning them with the greedy archetypes they best support.

| Family | Essence | Tunables (examples) | Output | Diversity control | Cost ($\approx$) | Best fit (greedy archetypes) | Expected effect |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Random / Stratified** | Baseline entropy; optionally stratified by space | $n_{\text{seeds}}$; grid/hex stratify; jitter | start node or full order | different $\text{RNG}$ seeds; strata tiling | $O(n)$ per seed | Baseline for **all**; shows $\text{ROI}$ | Variance $\downarrow$ with stratify; mild quality gain |
| **Cluster-Centroid / Medoid** | Start near density cores | $k$ (e.g., $\lceil\sqrt{n}\rceil$); $\text{k-means}$ vs $\text{k-medoids}$; init method | start node or cluster-wise order | rotate cluster visit order; multiple $k$ | $O(k n I)$ per run | $\text{NN}, \text{CI}, \text{GAO}$ | Preserves neighborhoods $\to$ smoother early growth |
| **Voronoi / Poisson-disk ($\text{Blue-noise}$)** | Even spatial coverage | $\text{min\_dist } \lambda$; rejection cap | start set or order by angle | vary $\lambda$; randomized darts | $O(n)$ to $O(n \log n)$ | $\text{Sweep}, \text{GAO}, \text{NN}$ | Angle/radius balance $\to$ fewer early crossings |
| **MST / 1-Tree Skeleton** | Encode global topology first | $\text{root rule}$; $\text{BFS/DFS/Preorder}$; edge-weight bias | full order (traversal) | randomize $\text{root}$ / tie-breakers | $O(n \log n)$ | $\text{CI}, \text{NN}, \text{LK}$ warm-start | Good long-range structure; fast to refine |
| **Angle-Radius Stratified ($\text{GAO-aware}$)** | Even bins in $(r,\theta)$ | $\# \text{radial bins } B_r$; $\# \text{angular bins } B_\theta$; bin visit order | start node or binwise order | permute bin schedules; radial bias | $O(n)$ | $\text{GAO}, \text{Sweep}$ | Rotation-coherent ignition; fewer angular shocks |
| **Spatial SFC ($\text{Hilbert/Z-curve}$)** | Space-filling curve order | $\text{curve type}$; resolution | full order | invert / rotate curves | $O(n \log n)$ | $\text{NN}, \text{Sweep}$ | Good locality; cheap and deterministic |
| **Learned Start ($\text{Lightweight}$)** | Predict promising start(s) from stats | $\text{features}$ (dispersion, skewness, $\text{kNN}$ radii); model | ranked start set | dropout, noise on features | $\text{train } O(nN)$; $\text{infer } O(1)$ | $\text{NN}, \text{GAO}, 2\text{-opt}$ | Directly reduces time-to-$X\%$ optimum |
| **Hybrid (Ensemble)** | Mix multiple archetypes then select | $\text{portfolio weights}$; budget per seed | top-$\text{k}$ seeds | enforce dissimilarity (e.g., $\text{Hamming}/\rho$) | additive | **All** | Robust across instance regimes; variance $\downarrow\downarrow\downarrow$ |

*Output* = either (a) **start node** for algorithms that then pick greedily, or (b) **full ordering** consumed directly by constructive passes ($\text{NN}, \text{Sweep}, \text{MST-traversal}, \text{SFC}$).

---

## 2) Evaluation Metrics (KPIs)

Metrics are stratified by Quality/Speed, Stability, and diagnostic Geometry/Coherence signals.

### Quality & Speed

* **Seed Efficiency**: $\Delta = \frac{\text{best\_random} - \text{best\_seeded}}{\text{best\_random}}$ (Fractional improvement over baseline random seeding).
* **Warm-Start Advantage**: $\text{time}_{\text{random} \to X\%} - \text{time}_{\text{seeded} \to X\%}$ ($X \in \{102\%, 101\%, 100.5\% \text{ of optimum/best-known}\}$).
* **Post-opt Residual**: $\frac{\text{length\_after\_k-opt} - \text{best\_known}}{\text{best\_known}}$ (Gap after refinement).
* **Convergence Area**: $\int \text{gap}(t) \text{ dt}$ over fixed budget (Smaller is better).

### Stability

* **Variance Reduction**: $\frac{\text{stddev}(\text{length})_{\text{seeded}}}{\text{stddev}(\text{length})_{\text{random}}}$
* **Outcome Gini**: Inequality of tour lengths across seeds (Lower is better).

### Geometry / Coherence (Diagnostics)

Use $m \approx 0.2n$ for “early” diagnostics; report both early and full-tour numbers.

* **Early Crossing Rate**: $\frac{\text{crossings after first } m \text{ steps}}{m}$
* **$\Delta r$ Smoothness**: $\text{mean } |r_i - r_{i-1}|$ over first $m$ steps
* **Angular Rhythm**: $\text{variance of } \Delta\theta$ over first $m$ steps

---

## 3) Experiment Plan (Instance-Stratified, Algorithm-Aligned)

### A. Instance Strata (Cover common $\text{TSP}$ “ecologies”)
* **Uniform random** (structure-poor)
* **Clustered** ($k=5–15$, varying spread)
* **Rings/annuli** (radial structure)
* **Grids + jitter** (man-made layouts)
* **Spiral/rotational** ($\text{GAO}$-friendly)
* **TSPLIB mix** (e.g., $\text{eil51}, \text{kroA100}, \text{pcb442}, \text{pr1002}$)

### B. Candidate Algorithms (Greedy Archetypes)
* **NN** (pure local)
* **Cheapest Insertion ($\text{CI}$)** (constructive with global peeks)
* **Sweep / Angular sort** (planar/angle-driven)
* **GAO ($\text{v1 \& v7}$)** (rotation-aware, windowed candidate set)
* (+ Optional) $\text{2-opt} / \text{LK}$ as **refiners** after each constructive pass

### C. Protocol

1.  **Portfolio Build**: Choose $S$ seeds per family (e.g., $S=32$). For $\text{Hybrid}$, allocate a budget across families (e.g., $40\%\ \text{GAO-aware}, 20\%\ \text{MST}, 20\%\ \text{clusters}, 20\%\ \text{blue-noise}$).
2.  **Constructive Run**: For each seed $\to$ run target greedy ($\text{NN/CI/Sweep/GAO}$) to completion. Record: length, time, early-geometry diagnostics.
3.  **Optional Refinement**: Run $\text{k-opt}$ ($\text{2-opt}$ or $\text{LK}$) for a fixed budget $B$ (e.g., $0.5–2.0\text{ s}$ per $1\text{k}$ nodes). Record convergence curves.
4.  **Selection Rules (for Hybrid)**:
    * $\text{Top-k keep}$: keep $k=3$ best tours per family for refiner.
    * $\text{Diversity guard}$: enforce $\ge \rho$ correlation distance between kept tours (e.g., $\rho=0.1$ by edge-overlap).
5.  **Scoring**: Compute $\text{KPIs}$ per ($\text{instance, family, algorithm}$). Aggregate by instance class and overall.

### D. Statistical Analysis
* Paired tests across seeds within same instance: bootstrap mean differences with $10\text{k}$ resamples.
* Across instances: repeated-measures $\text{ANOVA}$ or $\text{Friedman} + \text{Nemenyi post-hoc}$.
* Report **effect sizes** ($\text{Cliff’s } \delta$) and **win-rate matrices** ($\%$ times family $\text{A}$ beats $\text{B}$).

---

## 4) Alignment Hypotheses (What to Expect & What to Test)

| Greedy algo | Hypothesis-aligned seeds | Anti-patterns to detect |
| :--- | :--- | :--- |
| **NN** | Cluster-medoid, $\text{SFC, MST-preorder}$ | Pure random (variance high), overly angular seeds (early crossings) |
| **CI** | $\text{MST/1-tree traversal}$, cluster-wise order | $\text{Blue-noise}$ with too-sparse neighborhoods (costly insertions) |
| **Sweep** | Poisson-disk / $\text{blue-noise}$, angle-radius stratified | Cluster-only (angular clumping) |
| **GAO (v1)** | Angle-radius stratified, $\text{blue-noise, SFC}$ | Dense centroid starts (radial shocks) |
| **GAO (v7)** | Angle-radius stratified + light $\text{MST}$ hybrid | Random (unsteady $\Delta\theta$ rhythm) |

*Use diagnostics to confirm:* **early crossing rate** should fall for $\text{Sweep/GAO}$ seeds; **$\Delta r$ smoothness** should improve for $\text{NN/GAO}$; **angular rhythm** variance should drop for $\text{GAO}$.

---

## 5) Minimal Harness (Pseudocode)

```python
for instance in instances:
    seeds = {}
    for family in families:
        seeds[family] = generate_seeds(family, S, params[family])

    records = []
    for algo in algos:
        for family, seedset in seeds.items():
            for s in seedset:
                tour0 = run_constructive(algo, instance, s)
                diag0 = early_diagnostics(tour0, instance)
                tour, curve = optional_refine(tour0, budget=B)
                records.append(metrics(tour, curve, diag0, family, algo))
    save(records)
summarize_all()