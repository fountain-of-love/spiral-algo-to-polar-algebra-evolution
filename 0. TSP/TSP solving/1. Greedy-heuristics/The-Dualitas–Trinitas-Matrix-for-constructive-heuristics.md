# 🧭 The Dualitas–Trinitas Matrix for Constructive Heuristics

The construction of greedy heuristics can be formalized by mapping the **Blueprint**'s **$\text{Dualitas}$** ($\text{Stage 1a}$) and **$\text{Trinitas}$** ($\text{Stage 1b}$) logic onto algorithmic design. Each mediating variable (cost, angle, density, etc.) must possess both a raw **greedy expression ($\text{1a}$)** and a **contained or incremental expression ($\text{1b}$)**.

---

## 1. Underlying Logic — Dualitas $\leftrightarrow$ Trinitas in Constructive Heuristics

This framework defines two structural functions within constructive heuristics:

| Stage | Essence | Algorithmic Signature | Structural Function |
| :--- | :--- | :--- | :--- |
| **$\text{1a – Dualitas}$** | Pure greedy choice along one dimension (single polarity). | Pick next city minimizing a single criterion ($\text{cost, angle, density}$, etc.). | Differentiates a single **gradient** — no containment. |
| **$\text{1b – Trinitas}$** | Mediated or incremental rule that stabilizes a duality. | Uses an additional structural or sequential logic ($\text{insertion, angular containment, partial grouping}$). | **Contains** or **balances** the greedy field. |

Thus, for every **greedy variable**, we expect a **$\text{1a}$ form** (raw direct greedy expression) and a **$\text{1b}$ form** (a **containment / insertion / sequence-building** form).

---

## 2. Mediating Variables Across Greedy Spatial Heuristics

These variables determine the type of continuity or efficiency prioritized by the algorithm.

| Mediating Variable | Meaning / Field | Archetypal Source Pattern |
| :--- | :--- | :--- |
| **Cost (distance)** | Pure efficiency gradient | $\text{Proportional / Ratio}$ |
| **Angle (direction)** | Orientation continuity | $\text{Rotational / Symmetry}$ |
| **Density (local crowding)** | Spatial field smoothness | $\text{Containment / Field}$ |
| **Proportion (ratio of segment lengths)** | Harmonic moderation | $\text{Proportional / Ratio}$ |
| **Symmetry (mirror pairing)** | Bilateral balance | $\text{Rotational / Symmetry}$ |
| **Topology (connectivity)** | Adjacency and structure | $\text{Containment / Field}$ |
| **Rhythm (temporal phase / sequence pattern)** | Alternation, pacing | $\text{Resonant / Rhythmic}$ |

---

## 3. The Dualitas–Trinitas Matrix for Constructive Heuristics

This matrix formalizes the pairs, highlighting existing and latent opportunities:

| Mediating Variable | $\text{1a – Dualitas}$ (Direct Greedy) | $\text{1b – Trinitas}$ (Containment / Incremental) | Status |
| :--- | :--- | :--- | :--- |
| **Cost** | $\text{Nearest Neighbor (NN)}$: pick $\min$ distance | $\text{Cheapest Insertion (CI)}$: minimize incremental cost of containment | ✅ **Existing pair** ($\text{NN} \leftrightarrow \text{CI}$) |
| **Angle** | $\text{Angular Sweep}$: order by polar angle from a center | **$\text{GAO}$**: greedy cost selection + rotational continuity | ✅ **Existing pair** ($\text{Sweep} \leftrightarrow \text{GAO}$) |
| **Density** | $\text{Density Gradient Greedy (new)}$: choose next toward lower crowding | **$\text{DAO}$**: minimize $\text{cost} \times \text{density gradient}$ (field continuity) | 🆕 **Proposed pair** |
| **Proportion** | $\text{Ratio Greedy (new)}$: maintain constant step length ratio ($\text{e.g., golden } \phi$) | **$\text{PAO}$**: maintain harmonic proportionality while minimizing cost | 🆕 **Proposed pair** |
| **Symmetry** | $\text{Mirror Greedy (new)}$: expand tour symmetrically from seed point | **$\text{SAO}$**: pair symmetric nodes incrementally (mirror insertion) | 🆕 **Proposed pair** |
| **Topology** | $\text{Adjacency Greedy (new)}$: choose next among direct $\text{Delaunay}$ neighbors | **$\text{TAO}$**: incremental $\text{Delaunay}$ insertion / local planar containment | 🆕 **Proposed pair** |
| **Rhythm** | $\text{Alternating Greedy (new)}$: fixed periodic alternation (distance $\leftrightarrow$ angle) | **$\text{RHO}$**: adaptive phase-locked alternation tuned to tour curvature | 🆕 **Proposed pair** |

---

## 4. Interpretive Summary — Completion of the Greedy Field

The $\text{Dualitas–Trinitas}$ matrix essentially **completes the constructive heuristic grid**. Only two pairs (Cost and Angle) have established classical algorithmic equivalents; the remaining five variables constitute a **latent design space** for future geometry-aware heuristics.

| Variable Family | $\text{1a Form}$ | $\text{1b Form}$ | Observed in Literature? | Potential |
| :--- | :--- | :--- | :--- | :--- |
| **Cost** | $\text{NN}$ | $\text{CI}$ | ✅ $\text{Yes}$ | $\text{Saturated}$ |
| **Angle** | $\text{Sweep}$ | $\text{GAO}$ | ✅ $\text{Emerging}$ | $\text{High}$ |
| **Density** | $\text{Density Greedy}$ | $\text{DAO}$ | ❌ $\text{No}$ | $\text{Medium–High}$ |
| **Proportion** | $\text{Ratio Greedy}$ | $\text{PAO}$ | ❌ $\text{No}$ | $\text{Medium}$ |
| **Symmetry** | $\text{Mirror Greedy}$ | $\text{SAO}$ | ❌ $\text{No}$ | $\text{Medium}$ |
| **Topology** | $\text{Adjacency Greedy}$ | $\text{TAO}$ | ❌ $\text{No}$ | $\text{High (links to Delaunay/Voronoi)}$ |
| **Rhythm** | $\text{Alternating Greedy}$ | $\text{RHO}$ | ❌ $\text{No}$ | $\text{Speculative but elegant}$ |

### $\text{Insight: Triad Families}$

Each variable corresponds to a **Triad Family** within the $\text{Blueprint}$ logic:

* **$\text{Cost Triad}$** ($\text{NN} \leftrightarrow \text{CI}$)
* **$\text{Angle Triad}$** ($\text{Sweep} \leftrightarrow \text{GAO}$)
* **$\text{Density/Topology Triads}$** ($\text{DAO, TAO}$)
* **$\text{Proportion/Symmetry Triads}$** ($\text{PAO, SAO}$)

$\text{GAO}$ sits as the **$\text{Trinitas mediator}$** in the $\text{Angle Triad}$, demonstrating the method for expanding the constructive field across other essential spatial properties.