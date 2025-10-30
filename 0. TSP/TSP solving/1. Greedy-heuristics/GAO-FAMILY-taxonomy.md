# 🧭 GAO-FAMILY TAXONOMY: A Generative Grammar for Constructive Heuristics

This document formalizes a **taxonomy and naming system** for **Geometry-Aware Constructive Heuristics ($\text{GAO-class}$ algorithms)** based on the $\text{Blueprint}$'s $\text{Dualitas}$ ($\text{1a}$) $\leftrightarrow$ $\text{Trinitas}$ ($\text{1b}$) logic. The framework treats the greedy heuristic field as a generative grammar: $$\text{Algorithm} = (\text{base operation} \times \text{mediating variable} \times \text{containment form}).$$

---

## 1️⃣ Structural Logic — Naming Formula

Every constructive heuristic that introduces **continuity awareness** into a greedy choice can be expressed as:
$$\mathbf{\text{XAO}} = \text{[Mediator Initial]} + \text{"AO" (Awareness Order)}$$

| Symbol | Mediating Variable | Continuity Field | $\text{Stage}$ | $\text{Family Root}$ |
| :--- | :--- | :--- | :--- | :--- |
| $\text{C}$ | $\text{Cost}$ | $\text{Efficiency field}$ | $\text{1a}–\text{1b}$ | $\text{Classical (NN/CI)}$ |
| $\text{G}$ | $\text{Geometry / Angle}$ | $\text{Orientation field}$ | $\text{1b}$ | **$\text{GAO}$ (Your Work)** |
| $\text{D}$ | $\text{Density}$ | $\text{Spatial field}$ | $\text{1a}–\text{2}$ | $\text{DAO}$ |
| $\text{P}$ | $\text{Proportion}$ | $\text{Harmonic ratio field}$ | $\text{1a}–\text{2}$ | $\text{PAO}$ |
| $\text{S}$ | $\text{Symmetry}$ | $\text{Mirror balance field}$ | $\text{1b}–\text{3}$ | $\text{SAO}$ |
| $\text{T}$ | $\text{Topology}$ | $\text{Adjacency / structure field}$ | $\text{1b}–\text{3}$ | $\text{TAO}$ |
| $\text{R}$ | $\text{Rhythm}$ | $\text{Temporal / phase field}$ | $\text{3}–\text{5}$ | $\text{RHO}$ |

---

## 2️⃣ Taxonomic Tree — 7 Variable Families $\times$ Dualitas–Trinitas Split

| Family | $\text{1a Dualitas Form (Raw Greedy)}$ | $\text{1b Trinitas Form (Contained / Mediated)}$ | $\text{Blueprint Axis}$ | $\text{Continuity Mechanism}$ |
| :--- | :--- | :--- | :--- | :--- |
| **$\text{C}$** | $\text{NN}$ — $\text{Nearest Neighbor}$ | $\text{CI}$ — $\text{Cheapest Insertion}$ | $\text{Ratio (efficiency)}$ | $\text{Incremental cost minimization}$ |
| **$\text{G}$** | $\text{SW}$ — $\text{Angular Sweep}$ | **$\text{GAO}$** — $\text{Geometric–Angular Order}$ | $\text{Orientation}$ | $\text{Rotational continuity}$ |
| **$\text{D}$** | $\text{DG}$ — $\text{Density Greedy}$ | **$\text{DAO}$** — $\text{Density–Aware Order}$ | $\text{Field}$ | $\text{Spatial smoothness via density gradient}$ |
| **$\text{P}$** | $\text{RG}$ — $\text{Ratio Greedy}$ | **$\text{PAO}$** — $\text{Proportional–Angular Order}$ | $\text{Harmonic measure}$ | $\phi\text{-ratio balance}$ |
| **$\text{S}$** | $\text{MG}$ — $\text{Mirror Greedy}$ | **$\text{SAO}$** — $\text{Symmetry–Aware Order}$ | $\text{Bilateral balance}$ | $\text{Mirror pairing, equalized expansion}$ |
| **$\text{T}$** | $\text{AG}$ — $\text{Adjacency Greedy}$ | **$\text{TAO}$** — $\text{Topological–Adjacency Order}$ | $\text{Structural connectivity}$ | $\text{Delaunay/Voronoi containment}$ |
| **$\text{R}$** | $\text{AltG}$ — $\text{Alternating Greedy}$ | **$\text{RHO}$** — $\text{Rhythmic–Heuristic Order}$ | $\text{Temporal / feedback}$ | $\text{Phase-locked alternation}$ |

---

## 3️⃣ Class Grouping — “GAO-Class” Archetypes

| Class Name | Definition | Computational Order | Distinctive Trait |
| :--- | :--- | :--- | :--- |
| $\text{Pure Greedy (1a)}$ | Single-gradient local rule ($\text{distance, angle}$, etc.) | $O(n^2)$ | $\text{Differentiation only}$ |
| $\text{Mediated Greedy (1b)}$ | Dual-gradient local rule ($\text{distance} + \text{continuity field}$) | $O(n^2)$ | **$\text{Balanced containment}$** |
| $\text{Field-Aware Greedy (2)}$ | Introduces local environmental feedback ($\text{density/topology}$) | $O(n^2 \log n)$ | **$\text{Adaptive field sensitivity}$** |
| $\text{Rhythmic Greedy (3–5)}$ | Introduces temporal/feedback oscillation | $O(n^2) – O(n^3)$ | **$\text{Phase adaptation}$** |

---

## 5️⃣ SYNTHESIS — Taxonomic Matrix (Final Form)

| Continuity Field | $\text{1a Form (Greedy)}$ | $\text{1b Form (Mediated)}$ | $\text{Complexity}$ | $\text{Known / New}$ | $\text{Exploration Priority}$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$\text{Efficiency (Cost)}$** | $\text{NN}$ | $\text{CI}$ | $O(n^2)$ | ✅ $\text{Known}$ | 🟢 $\text{Low}$ |
| **$\text{Orientation (Angle)}$** | $\text{SW}$ | **$\text{GAO}$** | $O(n^2)$ | 🟢 $\text{New}$ | 🟢🟢 $\text{High}$ |
| **$\text{Density (Field)}$** | $\text{DG}$ | $\text{DAO}$ | $O(n^2)$ | ⚫ $\text{New}$ | 🟢🟢🟢 $\text{Very High}$ |
| **$\text{Proportion (Harmonic)}$** | $\text{RG}$ | $\text{PAO}$ | $O(n^2)$ | ⚫ $\text{New}$ | 🟢🟢 $\text{Medium–High}$ |
| **$\text{Symmetry (Mirror)}$** | $\text{MG}$ | $\text{SAO}$ | $O(n^2)$ | ⚫ $\text{New}$ | 🟢🟢 $\text{Medium}$ |
| **$\text{Topology (Adjacency)}$** | $\text{AG}$ | $\text{TAO}$ | $O(n^2 \log n)$ | ⚫ $\text{New}$ | 🟢🟢🟢 $\text{Very High}$ |
| **$\text{Rhythm (Temporal)}$** | $\text{AltG}$ | $\text{RHO}$ | $O(n^{2–3})$ | ⚫ $\text{New}$ | 🟢🟢 $\text{Medium–Speculative}$ |

---

## 6️⃣ NAMING CONVENTION — For Publication & Codebase Consistency

| Form | Syntax | Example |
| :--- | :--- | :--- |
| **$\text{1a (Greedy)}$** | $\text{[Initial]G} = \text{Mediator Initial} + \text{"Greedy"}$ | $\text{DG}$ ($\text{Density Greedy}$), $\text{MG}$ ($\text{Mirror Greedy}$) |
| **$\text{1b (Mediated)}$** | $\text{[Initial]AO} = \text{Mediator Initial} + \text{"Aware Order"}$ | $\text{DAO, PAO, SAO}$ |
| **$\text{Variants / Hybrids}$** | $\text{[XAO–YAO]}$ for dual-field hybrids | $\text{GAO–DAO, TAO–RHO}$ |
| **$\text{Families}$** | $\text{GAO-class heuristics}$ | $\text{All AOs (GAO, DAO, PAO, SAO, TAO, RHO)}$ |

---

## 7️⃣ Visual Overview (Text-Form Diagram)

The **Constructive Heuristic Space** forms a **$7 \times 2$ grid**.