# 📚 Literature Map: $\text{TSP}$ Initialization Strategies (Seeding $\to$ Refinement)

The body of work on initialization (seeding) for $\text{TSP}$-like solvers is substantial but fragmented. It is scattered across various families, but a single paper systematically mapping **spatial seeding families $\to$ greedy archetypes** is missing, highlighting the novelty of the proposed blueprint.

---

## What's Out There (By Seeding Family)

### 1) Clustering-Driven Seeding ($\text{k-means/DBSCAN/etc.}$) 🧱

* **Core Idea**: Cluster cities first, then use intra-cluster tours and joining strategies (common in **Clustered $\text{TSP}$ ($\text{CTSP}$)**). Also used to initialize populations in metaheuristics ($\text{GA/PSO}$) to accelerate convergence.
* **Takeaway**: **Strong evidence** that “spatial clustering seeds” improve both quality and time, especially on clustered or mixed-density instances. Good precedent for **"cluster-centroid/medoid seeds."**

### 2) Space-Filling Curves ($\text{SFC}$) — $\text{Hilbert/Peano/Z-order}$ Starts 🌀

* **Core Idea**: Order points according to their position on a space-filling curve to exploit **locality preservation** cheaply ($O(n \log n)$).
* **Precedent**: Classic work by **Platzman \& Bartholdi (1989)** established $\text{SFC}$ as a highly efficient planar $\text{TSP}$ heuristic, often used as a quick initializer.
* **Takeaway**: $\text{SFC}$ orders are a documented, cheap **full-order seed**; especially sensible for **Nearest Neighbor ($\text{NN}$)/Sweep** starts and grid-ish instances.

### 3) $\text{MST}$ / $\text{1-tree}$ / Christofides-Style Starts 🌳

* **Core Idea**: Embed **global topological information** into the initial tour by using minimum spanning structures (e.g., $\text{MST}$ preorder).
* **Precedent**: The $\text{MST}$ preorder (a $2$-approximation) is a standard constructive starting tour. **Christofides** and **Held–Karp $\text{1-tree}$** provide structural grounding for topology-aware starts.
* **Takeaway**: Good precedent for **"MST/1-tree inspired seeds"**—they encode global topology early and warm-start **Cheapest Insertion ($\text{CI}$)/Lin–Kernighan ($\text{LK}$)** well.

### 4) Learned Seeding / "Seeder $\to$ Reviser" Pipelines 🤖

* **Core Idea**: Use a data-driven approach (e.g., $\text{DRL}$) where a **Seeder** policy generates a diverse, high-quality set of candidate tours (initial seeds) for a **Reviser** policy ($\text{LK}$-style) to refine.
* **Precedent**: **Kim et al. ($\text{NeurIPS}'21$)** validated this two-policy approach on $\text{TSP}$ and related routing problems, explicitly focusing on seed diversity.
* **Takeaway**: Strong conceptual match to the **"learning-guided seeds + ensemble"** family; evidence is strong, though the seeding mechanism is learned rather than geometrically engineered.

### 5) General Constructive/Initialization Heuristics (Context) 🗺️

* $\text{Lin–Kernighan}$ surveys establish how profoundly the **initial tour quality** affects the performance and runtime of powerful improvement heuristics.
* Studies on $\text{NN}$ and its known pitfalls motivate the need for smarter starts.

### 6) Angle–Radius / Blue-Noise Style Ideas 📐

* **Direct literature on Poisson-disk/blue-noise seeding for $\text{TSP}$ is scarce**; however, $\text{SFC}$ and radial/annulus analyses proxy the **even-coverage** rationale. Blue-noise sampling is well-documented in graphics and transferable.
* **Takeaway**: This is a **clear gap**—a systematic comparison of **Angle–radius stratified** seeding against other families, using diagnostics like **$\Delta\theta$ rhythm** and **$\Delta r$ smoothness**, represents a clean contribution.

---

## Where the Blueprint is New (Gaps = Your Contribution)

| Novelty | Description |
| :--- | :--- |
| **Instance Profiling $\to$ Seeding Policy** | There is no prior work that **classifies $\text{TSPLIB}$ instances by fine-grained geometry** ($\text{anisotropy, angular spectra, ring detection}$) and then uses a deterministic or adaptive rule-set to **choose a seed portfolio** accordingly (i.e., your "ecologies $\to$ portfolio weights"). |
| **Seeding Families $\times$ Greedy Archetypes** | No paper aligns and tests the entire spectrum: e.g., **Angle–radius bins $\to \text{GAO}$, $\text{SFC} \to \text{NN/Sweep}$, $\text{MST} \to \text{CI/LK}$** in a **single, controlled study** with shared $\text{KPIs}$ (like $\text{Variance Reduction}$). |
| **Ensemble/Bandit Over Seed Families** | While learned "seeders" exist, the idea of a **geometric ensemble** combined with a **tiny bandit warm-up** (for portfolio selection) specifically for **greedy starts** is unexplored. |

---

## 💡 Positioning the Stage-0 Paper

* **Title Idea**: "Seeding the $\text{TSP}$: Geometry-aware initialization portfolios for greedy and local heuristics."
* **Claim**: On a $\text{TSPLIB}$ mix, geometry-aware seeding portfolios yield $\mathbf{+2–5\%}$ tour quality and $\mathbf{30–50\%}$ faster convergence for refiners vs. random/semi-naive starts—without touching core heuristics.