# 🌿 Stage 2-1 – Adaptatio / Sustaining Flows

---

## 🔹 Essence

**Adaptatio** introduces **responsiveness**.

Where Stage 1b built a static frame (“sweep through a fixed order”), Adaptatio begins to **listen** — adjusting the construction as new information arrives.

In TSP heuristics, this means every insertion or extension of the tour is decided by **how it affects total balance** (length, smoothness, continuity).

Adaptatio = **“keep the flow alive.”** It transforms rigid order into **dynamic maintenance**.

---

## 🧩 1. Representative Algorithms

| Family / Algorithm | Core Mechanism | Behavioural Signature |
| :--- | :--- | :--- |
| **Cheapest Insertion (CI)** | Add the point that yields the smallest increase in total tour length. | Smooth incremental growth; globally aware; **slower but steady**. |
| **Nearest Insertion (NI)** | Choose point closest to tour, insert where cost increase is minimal. | More local; preserves shape; efficient compromise. |
| **Farthest Insertion (FI)** | Insert the farthest unvisited point at cheapest position. | Expands perimeter evenly; good for distributed data. |
| **Distance & Least Insertion (DLI)** | Hybrid: select nearest point, then least-cost insertion. | Balanced local + global awareness; fast. |
| **Regret-2 / Regret-k Heuristics** | Insert point whose delay would hurt most (regret = second-best − best). | **Anticipatory adaptation**; handles nonuniformity well. |

* **Complexity:** $O(n^2 – n^3)$ (depends on update policy).
* **Performance:** among the strongest classical constructive heuristics; 3–10% above optimum for many TSPLIB sets.

---

## ⚖️ 2. Core Dualities of Adaptatio

| Axis | Pole A | Pole B | Interpretation |
| :--- | :--- | :--- | :--- |
| **Local vs Global** | choose nearest insertion | minimize total added cost | constant negotiation between micro-fit and macro-flow |
| **Growth vs Maintenance** | expand tour | preserve shape continuity | balancing extension and smoothness |
| **Inclusion vs Exclusion** | insert new node | protect integrity of existing path | care-based filtering logic |
| **Deterministic vs Probabilistic** | fixed rule | adaptive weighting (e.g., regret) | early seeds of learning behaviour |
| **Temporal vs Spatial** | order of addition | geometry of route | synchronizing two dimensions of change |

Adaptatio thus converts pure selection into **relational maintenance** — a feedback process that values **continuity**.

---

## 🔺 3. Triads Active in Adaptatio

| Triad | Roles | Meaning / Manifestation |
| :--- | :--- | :--- |
| **(Existing tour, Candidate point, Insertion position)** | context $\leftrightarrow$ input $\leftrightarrow$ action | canonical Adaptatio decision loop. |
| **(Length, Smoothness, Cost)** | quantitative $\leftrightarrow$ qualitative $\leftrightarrow$ energetic measure | evaluates balance of effort. |
| **(Add, Assess, Adjust)** | growth $\leftrightarrow$ feedback $\leftrightarrow$ correction | minimal control cycle. |
| **(Local, Regional, Global)** | micro $\leftrightarrow$ meso $\leftrightarrow$ macro adaptation scales | beginning of ecological layering. |

These triads embody the **self-stabilizing heartbeat** of constructive systems.

---

## 🧠 4. Blueprint Step Mapping

| Blueprint Step | Manifestation in Algorithmic Logics |
| :--- | :--- |
| **S.02-1 Adaptatio** | introduces feedback loops to preserve flow; each insertion cares for global shape. |
| **(inherited S.01b) Trinitas** | frame still provides reference (order, angle). |
| **(proto S.02-2) Textura** | repeated insertions begin forming texture (scaffolding). |

### ✅ Stage 2-1 Summary

**Stage 2-1 – Adaptatio = The Law of Sustaining Flows**

* **“Containment becomes care.”**
* **Purpose:** preserve coherence while expanding.
* **Representative Algorithms:** CI, NI, FI, DLI, Regret-k.
* **Structure:** feedback insertion loop; evaluates cost + continuity.
* **Energetic Pattern:** responsive, nurturing, smoothing.
* **Outcome:** tours with graceful curvature and reduced crossings; slower but far more stable.
* **Transition Vector:** toward **Textura (S.02-2)** when structure ceases to be reactive and becomes **supportive** — a fabric.