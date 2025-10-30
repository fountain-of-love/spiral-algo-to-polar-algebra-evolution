# 🧭 Expanding the Greedy Heuristic Landscape: Dualities and Triadic Mediators

The **Geometry-Aware Order (GAO)** heuristic, introduced in the previous context, represents a successful application of **Stage 1a – Dualitas** logic: finding a mediating term to resolve the tension between the poles of **cost minimization** and **spatial coherence** in constructive algorithms. By resolving this duality, GAO moves toward **Stage 1b – Trinitas** (coherent field formation).

This section explores the broader landscape of greedy constructive heuristics by identifying other inherent dualities and proposing "sibling" algorithms that act as **Triadic mediators**.

---

## 🧩 1. The Dualities Inside Greedy Heuristics

Traditional greedy heuristics (like Nearest Neighbor) exist within a set of unresolved tensions. The $\text{GAO}$ successfully addressed the first one ($\text{Distance cost} \leftrightarrow \text{Angular continuity}$).

| Pole A | Pole B | Tension / Field | Mediating Third Term ($\text{Trinitas}$) |
| :--- | :--- | :--- | :--- |
| $\text{Distance cost}$ | $\text{Angular continuity}$ | **Rotation Field** | $\text{GAO}$ ($\text{cost} \times \text{angle}$) |
| $\text{Nearest}$ | $\text{Farthest / Opposite}$ | $\text{Contrast-aware}$ | $\text{Contrast-Aware}$ greedy |
| $\text{Local greedy}$ | $\text{Global bias / centroid}$ | $\text{Context-aware}$ | $\text{Centroid-Biased}$ greedy |
| $\text{Deterministic}$ | $\text{Stochastic}$ | $\text{Probabilistic continuity}$ | $\text{Probabilistic Coherence}$ greedy |
| $\text{Euclidean metric}$ | $\text{Topological / density metric}$ | $\text{Structure-aware}$ | $\text{Topological-Adjacency}$ greedy ($\text{TAO}$) |

Each duality provides an opportunity to spawn a new constructive heuristic by inserting a **mediating third term**—the **Trinitas** of Stage 1b.

---

## ⚙️ 2. Triadic Expansions — Possible New Greedy Spatial Heuristics

These prototypes remain **constructive** and **greedy** but mediate a different pair of tensions than $\text{GAO}$.

| Heuristic Prototype | Duality It Mediates | Core Local Rule | Relation to GAO |
| :--- | :--- | :--- | :--- |
| **GAO** (Geometric–Angular Order) | $\text{cost} \leftrightarrow \text{angle}$ | pick nearest neighbor within minimal angular deviation | **Baseline mediator** (distance + rotation) |
| **DAO** (Density–Aware Order) | $\text{cost} \leftrightarrow \text{spatial density}$ | pick next city minimizing $\text{distance} / \text{local density gradient}$ | continuity by **crowding gradient**; favors smooth density transitions. |
| **RAO** (Radial–Angular Order) | $\text{center} \leftrightarrow \text{edge}$ | pick next by nearest radius \& smooth angular increment | continuity in **radius–angle plane**; mitigates polar "ring collapse." |
| **PAO** (Proportional–Angular Order) | $\text{distance} \leftrightarrow \text{proportion ratio}$ | maintain segment ratios near $\text{golden } \phi$ while minimizing cost | continuity through **harmonic proportionality**. |
| **SAO** (Symmetry–Aware Order) | $\text{forward} \leftrightarrow \text{mirror direction}$ | pair symmetric counterparts while extending path | continuity by **bilateral reflection**; ideal for symmetric sets. |
| **TAO** (Topological–Adjacency Order) | $\text{geometric} \leftrightarrow \text{connectivity}$ | $\text{next} = \text{nearest in Delaunay/Voronoi adjacency, not just distance}$ | continuity by **topological field**, avoids crossings. |
| **RHO** (Rhythmic–Heuristic Order) | $\text{greedy} \leftrightarrow \text{oscillatory feedback}$ | alternate between $\text{NN}$ and angular rule every $k$ steps | continuity through **temporal rhythm** (phase-locked alternation). |

---

## 🔺 3. Structural Triads Emerging

These new heuristics align with the $\text{Blueprint}$'s energetic structure, falling into specific "spatial-continuity triads":

| Triad | Poles | Mediating Principle | Example Heuristics |
| :--- | :--- | :--- | :--- |
| **$\text{Field Triad}$** ($\text{0}–\text{1b}$) | $\text{Distance} \leftrightarrow \text{Angle}$ | **Containment/field continuity** | $\text{GAO, RAO}$ |
| **$\text{Flow Triad}$** ($\text{2}–\text{3}$) | $\text{Distance} \leftrightarrow \text{Density/Topology}$ | **Ecological/topological continuity** | $\text{DAO, TAO}$ |
| **$\text{Resonance Triad}$** ($\text{5}–\text{8}$) | $\text{Determinism} \leftrightarrow \text{Oscillation}$ | **Temporal continuity** | $\text{RHO}$ |

$\text{GAO}$ is the angular mediator of the $\text{Field Triad}$. Its siblings explore density, proportion, or rhythmic feedback as alternative continuity mediators, all while remaining $\text{greedy}$ and $\text{constructive}$.

---

## 🧭 4. Summary Table — Potential Greedy Spatial Heuristic Lineage

| Code | Name | Mediating Variable | Continuity Type | Blueprint Domain |
| :--- | :--- | :--- | :--- | :--- |
| **NN** | $\text{Nearest Neighbor}$ | $\text{cost}$ | none | $\text{1a Dualitas}$ |
| **CI** | $\text{Cheapest Insertion}$ | $\text{incremental cost}$ | structural | $\text{1b Trinitas}$ |
| **Sweep** | $\text{Angular Sort}$ | $\text{angle (global)}$ | planar ordering | $\text{1b Trinitas}$ |
| **GAO** | $\text{Geometric–Angular Order}$ | $\text{cost} \times \text{angle}$ | rotational continuity | $\text{1a} \leftrightarrow \text{3}$ |
| **DAO** | $\text{Density–Aware Order}$ | $\text{cost} \times \text{density gradient}$ | field continuity | $\text{1a} \leftrightarrow \text{2}$ |
| **RAO** | $\text{Radial–Angular Order}$ | $\text{radius} \times \text{angle smoothness}$ | polar continuity | $\text{1a} \leftrightarrow \text{1b}$ |
| **PAO** | $\text{Proportional–Angular Order}$ | $\phi\text{-ratio} \times \text{cost}$ | harmonic continuity | $\text{1b} \leftrightarrow \text{2}$ |
| **SAO** | $\text{Symmetry–Aware Order}$ | $\text{mirror balance}$ | bilateral continuity | $\text{1b} \leftrightarrow \text{3}$ |
| **TAO** | $\text{Topological Adjacency Order}$ | $\text{Delaunay connectivity}$ | topological continuity | $\text{1b} \leftrightarrow \text{3}$ |
| **RHO** | $\text{Rhythmic–Heuristic Order}$ | $\text{phase feedback}$ | temporal continuity | $\text{3} \leftrightarrow \text{5}$ |

### $\text{Interpretation}$

Reading this through $\text{Blueprint}$ logic reveals the lineage:

* **$\text{GAO}$** is the $\text{first leap toward Trinitas}$, successfully mediating $\text{cost} \leftrightarrow \text{coherence}$.
* **$\text{DAO, RAO, PAO}$** are its **parallel siblings**—same stage family, different mediators.
* **$\text{TAO}$** and **$\text{RHO}$** start to **nudge toward Stage 2–3 and beyond** by integrating higher-order patterns like topology ($\text{TAO}$) or temporal feedback ($\text{RHO}$).

This provides a structured framework for exploring and classifying new geometry-aware constructive heuristics.