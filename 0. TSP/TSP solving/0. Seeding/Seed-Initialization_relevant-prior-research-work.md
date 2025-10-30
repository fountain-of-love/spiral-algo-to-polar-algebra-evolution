# ✅ Relevant Prior Work on Initialization Strategies in TSP

This summary reviews existing research related to "seeding" or initialization in the $\text{Travelling Salesman Problem}$ ($\text{TSP}$) domain, highlighting alignment with and gaps addressed by the proposed systematic blueprint.

---

## 🔍 Relevant Prior Work

| Study/Concept | Core Idea | Alignment with Blueprint | Gap/Context |
| :--- | :--- | :--- | :--- |
| **Alkafaween (2024)**: Seeding Genetic Algorithms ($\text{GA}$) | Initializing $\text{GA}$ population with better-than-random solutions (e.g., greedy-route generation from extreme points). | Aligns with the general idea of **"improved seeding"** to reduce initial entropy. | Context is **population-based metaheuristics ($\text{GA}$)**, not optimizing the starting point for single-run constructive/local search heuristics ($\text{NN, LK, GAO}$). |
| **Anaya Fuentes (2017)**: Clustering $\to$ Multi-Restart $\text{ILS}$ | Clustering cities first, then using heuristic insertion / meta-search ($\text{MRSILS}$) to build the initial tour. | Directly matches one of the **"spatial clustering seed"** families in the $\text{Origo}$ blueprint. | Focuses only on clustering as the spatial seed; lacks systematic comparison to other geometric seeds (e.g., $\text{blue-noise, A-R stratified}$). |
| **Rego (2011)**: $\text{TSP}$ Heuristics Survey | Broad review of constructive heuristics ($\text{NN, CI}$), local search ($\text{k-opt}$), and metaheuristics. | Provides necessary **background and context** on the downstream $\text{TSP}$ algorithms. | Does **not** focus on the systematic design, comparison, or tuning of initialization/seeding *families* themselves. |
| **Kim et al. (2021)**: Learned Collaborative Policies | Uses a "seeder" policy (Neural Network) to generate diverse candidate tours (initial seeds), followed by a "reviser" ($\text{LK}$) for refinement. | Philosophically close to the **"Ensemble Seeding"** and **"Learned Start"** ideas in the blueprint (generate diversity, then refine). | The seeding policy is **learned** (information feedback loop), not explicitly **spatially engineered** ($\text{MST, A-R, Blue-noise}$). |

---

## ⚠️ Gaps / Opportunities (Blueprint's Novel Contribution)

The published research validates the *value* of non-random initialization, but the proposed blueprint adds a new layer of **systematic structural engineering** to the problem:

1.  **Systematic Taxonomy for Constructive Heuristics**: The literature is heavier on seeding for metaheuristics ($\text{GA, ILS}$). The blueprint explicitly focuses on **seeding for single-run constructive/local search pipelines** ($\text{NN, CI, LK, GAO}$), introducing a $\text{taxonomy}$ of seed families ($\text{MST, Blue-noise, Angle-Radius}$) tailored for them.
2.  **Explicit Spatial/Topological Seeding**: Concepts like **Poisson-disk/blue-noise distribution** and **angular stratification ($\text{A-R Strat}$)** are rarely seen in the $\text{TSP}$ seeding context, appearing in fragmented form, if at all. The blueprint makes these structural geometries central.
3.  **Algorithmic Alignment Matrix**: There is no readily available paper that systematically studies the matrix of **"Instance Profiling $\to$ Seeding Policy $\to$ Greedy Heuristic Alignment"** in a rule-based fashion as detailed in Stages $0\cdot\alpha$ through $0\cdot\gamma$.
4.  **Novel $\text{KPI}$ Focus**: Few studies track the specific stability and convergence metrics proposed, such as **"Variance Reduction across seeds,"** **"Warm-Start Advantage,"** or the early-tour **"Geometric Diagnostics"** ($\Delta r \text{ smoothness, angular rhythm}$).

The blueprint shifts the focus from "get a better-than-random seed" to **"engineer the optimal low-entropy starting field for a specific algorithmic architecture on a specific instance geometry."**