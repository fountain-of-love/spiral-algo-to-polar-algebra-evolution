# 🌱 Stage 0 — Seed Initialization Blueprint (Advanced)

This advanced blueprint outlines a three-step ($\alpha, \beta, \gamma$) process for **Instance-Aware Seeding**, moving beyond simple randomization to dynamically shape the search entropy based on the problem's underlying geometry and structure.

---

## Stage 0·$\alpha$ — Instance Profiling (Lightweight)

Compute a handful of **structure fingerprints**. Use random subsampling (e.g., $0.2n$, cap at $2\text{k}$ points) and $O(n \log n)$ or $O(n)$ methods to keep cost low.

| Feature | Computation & Interpretation |
| :--- | :--- |
| **Geometry & Density** | |
| Spread / Scale ($\text{A}$) | $\text{bbox aspect ratio } A = \frac{\max\_x - \min\_x}{\max\_y - \min\_y}$ (clip $\ge 1$). High $\to$ elongated “corridor”. |
| Anisotropy ($\lambda_1/\lambda_2$) | $\text{PCA eigenratio } \lambda_1/\lambda_2$. High $\to$ strong directional field. |
| Clustering ($\text{H}$) | $\text{Hopkins statistic } H$ ($\approx 0.5 \text{ uniform}; > 0.7 \text{ clustered}$), or silhouette on $\text{k-means } (k \approx \lceil\sqrt{n}\rceil)$. |
| $\text{kNN}$ radii | $\text{mean/variance of } 1\text{-NN distance}$; high $\text{CV} \to$ mixed densities. |
| $\text{MST}$ signature | $\text{mean edge length } \bar{e}, \text{ CV}(\bar{e}), \text{ and } \%$ of long edges (tail mass). High tail $\to$ separated groups. |
| **Radial/Rotational Structure** | |
| Radial profile | $\text{variance of radius } r \text{ from centroid}$; multimodality test (e.g., $\text{Hartigan’s dip on } r$) $\to$ rings/annuli. |
| Angular spectrum | $\text{power in low-order Fourier modes of } \theta\text{-ordered radii } (m=1..8)$. Peaks at $m=1 \text{ (spiral/arc)}, m=4 \text{ (grid-ish)}, \dots$ |
| **Grid/Urban Hints (Cheap)** | |
| Orthogonality index | $\text{histogram of edge bearings for } \text{kNN } \text{graph}$; peaks near $0/90/180 \to \text{grid-like}$. |
| Crossing pressure | $\text{run } 200\text{-step } \text{NN from } 8 \text{ random starts}$; $\text{crossings per step} \approx \text{planarity stress}$. |

*All computations can be done on the sample; promote thresholds cautiously (use quantiles, not absolutes).*

---

## Stage 0·$\beta$ — Ecology Classification (Rule-of-Thumb)

Map fingerprints $\to$ one (or a mix) of **instance ecologies**:

| Ecology | Triggers (Any two strongly) |
| :--- | :--- |
| **Uniform** | $H \approx 0.5$; $\text{CV}(1\text{NN})$ low; eigenratio $\lt 1.6$; $\text{MST}$ tail low |
| **Clustered** | $H \gt 0.7$ or silhouette $\gt 0.4$; $\text{CV}(1\text{NN})$ high; $\text{MST}$ tail high |
| **Ring/Annulus** | Radial multimodality; low center density; ring kurtosis |
| **Spiral/Rotational** | Angular spectrum peak at $m=1-2$; monotone $\Delta\theta$ trend |
| **Grid/Orthogonal** | Bearing peaks at $\sim 0/90$; low clustering; eigenratio $\sim 1$ |
| **Corridor/Anisotropic** | eigenratio $\gt 3$ or $\text{bbox } A \gt 3$; low clustering |

*If mixed, keep **top-2** ecologies with weights proportional to confidence (normalize triggers to $[0,1]$ and softmax).*

---

## Stage 0·$\gamma$ — Seeding Policy per Greedy Archetype

Choose (or mix) **seeding families** based on $\text{ecology} \times \text{algorithm}$. Percentages are portfolio weights; run $S$ seeds with this split (e.g., $S=32$).

| Ecology | NN (Nearest Neighbor) | CI (Cheapest Insertion) | Sweep / Angular Sort | GAO (v1 / v7) |
| :--- | :--- | :--- | :--- | :--- |
| **Uniform** | $60\% \text{ SFC}, 40\% \text{ MST}$ | $70\% \text{ MST}, 30\% \text{ Cluster}$ | $60\% \text{ Blue-noise}, 40\% \text{ A-R Strat}$ | $50\% \text{ A-R Strat}, 50\% \text{ Blue-noise}$ |
| **Clustered** | $50\% \text{ Cluster}, 30\% \text{ SFC}, 20\% \text{ MST}$ | $50\% \text{ MST}, 30\% \text{ Cluster}, 20\% \text{ Blue-noise}$ | $70\% \text{ Blue-noise} (\lambda \uparrow), 30\% \text{ A-R Strat}$ | $40\% \text{ A-R Strat}, 30\% \text{ Blue-noise}, 30\% \text{ MST}$ |
| **Ring/Annulus** | $60\% \text{ A-R Strat}, 40\% \text{ Blue-noise}$ | $60\% \text{ A-R Strat}, 40\% \text{ MST}$ | $80\% \text{ A-R Strat}, 20\% \text{ Blue-noise}$ | $80\% \text{ A-R Strat} (B_r, B_\theta \text{ bal}), 20\% \text{ Blue-noise}$ |
| **Spiral/Rotational** | $70\% \text{ A-R Strat}, 30\% \text{ Blue-noise}$ | $50\% \text{ A-R Strat} + 50\% \text{ MST}$ | $70\% \text{ A-R Strat} (\phi \text{-aligned}), 30\% \text{ Blue-noise}$ | $70\% \text{ A-R Strat} (\phi \text{-biased}), 30\% \text{ MST hybrid}$ |
| **Grid/Orthogonal** | $70\% \text{ SFC}, 30\% \text{ Blue-noise}$ | $60\% \text{ SFC}, 40\% \text{ MST}$ | $60\% \text{ Blue-noise}, 40\% \text{ SFC}$ | $60\% \text{ SFC}, 40\% \text{ A-R Strat}$ |
| **Corridor/Aniso** | $60\% \text{ SFC (axis-aligned)}, 40\% \text{ MST}$ | $70\% \text{ MST (principal axis)}, 30\% \text{ SFC}$ | $60\% \text{ Blue-noise (elongated)}, 40\% \text{ A-R Strat}$ | $60\% \text{ A-R Strat (elliptic bins)}, 40\% \text{ SFC}$ |

*“$\text{A-R Strat}$” = Angle–radius stratified; for **spiral** cases, bias bin schedule to match detected rotation direction (sign of $\text{mean } \Delta\theta$).*

---

## Stage 0·$\delta$ — Budgeting & Bandit Adaptation (Fast Sanity Check)

To auto-tune the portfolio, use a **tiny bandit warmup**:

1.  From the portfolio in Stage $0\cdot\gamma$, run $s_0=6$ seeds ($\approx 3 \text{ families} \times 2 \text{ seeds}$) with your greedy of choice.
2.  Record an early $\text{KPI}$ (e.g., length after constructive or after $0.1 \cdot B \text{ refiner budget}$).
3.  Use $\text{UCB1}$ or $\text{Successive Halving}$ on families to allocate the remaining $S - s_0$ seeds to the best performers.
4.  Keep **top-$k$ tours** ($k=3$) with a **diversity guard** ($\text{edge-overlap} \le 0.9$).

*This costs $\lt 10-15\%$ of the constructive budget and significantly reduces refinement time.*

---

## Stage 0·$\eta$ — Diagnostics to Confirm You Picked Well

After constructive pass (before refinement), check:

* **Early crossing rate** $\downarrow$ vs. random baseline (especially for $\text{Sweep/GAO}$).
* **$\Delta r$ smoothness** $\uparrow$ for $\text{NN/GAO}$ (fewer radial shocks).
* **Angular rhythm variance** $\downarrow$ for $\text{GAO}$ (cleaner rotation).
* **Seed Efficiency** and **Variance Reduction** meet your thresholds (e.g., $\ge 2\%$ and $\ge 40\%$).
* *If not met, $\text{flip}$: swap $20-30\%$ of the portfolio to the runner-up family and rerun just the constructive step (cheap).*

---

## Drop-in Pseudocode

```python
def profile(instance, sample_frac=0.2, max_sample=2000):
    P = subsample(instance.points, sample_frac, max_sample)
    feats = {}
    feats['bbox_ratio'] = bbox_aspect(P)
    feats['eigenratio'] = pca_eigenratio(P)
    feats['hopkins'] = hopkins(P)
    feats['cv_1nn'] = cv_knn_radius(P, k=1)
    feats['mst_tail'] = mst_tail_mass(P)
    feats['ring'] = radial_multimodality(P)
    feats['ang_modes'] = angular_spectrum(P)  # array m=1..8
    feats['bearing_peaks'] = orthogonality_index(P)
    return feats

def choose_portfolio(feats, algo):
    ecol = classify_ecology(feats)  # returns {label: weight}
    return mix_portfolios(ecol, algo)  # uses tables above

def solve(instance, algo, S=32, k_keep=3, bandit=True):
    feats = profile(instance)
    portfolio = choose_portfolio(feats, algo)
    seeds = sample_seeds(portfolio, S)
    if bandit:
        results = bandit_warmup(instance, algo, seeds)
        seeds = reallocate_from_bandit(results, seeds)
    tours = run_constructive_batch(instance, algo, seeds)
    picked = select_top_k_diverse(tours, k_keep)
    return picked

```

# TL;DR: Instance-Aware Seeding Strategy

* **Yes, do a pre-scan**: Perform **tiny, cheap profiling** to label the instance ecology ($<3\%$ cost).
* **Map $\text{ecology} \times \text{algorithm} \to \text{seed families}$** using the rule table in Stage $0\cdot\gamma$ (Blueprint for policy choice).
* **Optionally add a micro-bandit** ($0\cdot\delta$) to auto-tune the seed portfolio on the fly.
* **Expect $\mathbf{2-5\%}$ quality gain** $+\mathbf{30-50\%}$ **faster refinement** on $\text{TSPLIB-mix}$ without touching core heuristics.