# ⚔️ Stage 1a – Dualitas / Local Contrast

---

## 🔹 Essence

**Stage 1a** marks the **first act of differentiation**: once a seed exists, the system begins to choose — **this vs that**.

In TSP terms, it’s the moment when the tour logic awakens as **“always pick the closest”** or **“shortest edge wins.”**

It’s **pure polarity**: attraction by distance, untempered by containment or feedback.

---

## 🧩 1. Representative Algorithms

| Family / Algorithm | Core Mechanism | Behavioural Signature |
| :--- | :--- | :--- |
| **Nearest Neighbor (NN)** | From current node, choose unvisited city with minimal distance. | Fast, deterministic given start; **angularly chaotic**, tends to loop inward. |
| **Greedy Edge (GE)** | Sort all edges by length; add shortest non-conflicting edges. | Purely edge-centric; ignores tour continuity until late. |
| **Farthest Neighbor (FN)** | Choose farthest unvisited city (inverse polarity). | Expansive pattern; good for sparse sets, often **over-stretched**. |
| **Double-Ended Greedy (DEG)** | Grow tour from both ends by nearest choice. | Slightly smoother than NN; still 1-D polarity logic. |
| **Randomized NN (R-NN)** | Run NN multiple times with random starts; keep best. | Ensemble average softens bias but remains same stage logic. |

* **Complexity:** typically $O(n^2)$; near-constant factor; trivially parallelizable.
* **Performance:** baseline class — fast, 10–25% longer than optimum on TSPLIB-like data.

---

## ⚖️ 2. Core Dualities (the heart of Stage 1a)

| Axis | Pole A | Pole B | Interpretation |
| :--- | :--- | :--- | :--- |
| **Selection Basis** | Local distance | Global pattern (ignored) | Algorithm focuses entirely on the local pole. |
| **Expansion Direction** | Inward pull | Outward exploration | NN $\to$ inward collapse; FN $\to$ outward spread. |
| **Edge Perspective** | Node-centric (NN) | Edge-centric (GE) | Defines two micro-archetypes within 1a. |
| **Determinism** | Deterministic choice | Randomized restart | Randomization softens polarity but doesn’t create a field. |
| **Metric Bias** | Euclidean distance | Other metric (cost, time) | Shows that polarity can occur in any cost dimension. |

**Dualitas** is thus **tension crystallized**: selection vs rejection, attraction vs repulsion, local vs global.

---

## 🔺 3. Proto-Triads (incipient containments within 1a)

Even in pure polarity, minimal triads appear as **process fragments**:

| Triad | Roles | Meaning / Manifestation |
| :--- | :--- | :--- |
| **(Current, Candidate, Chosen)** | evaluator $\leftrightarrow$ options $\leftrightarrow$ selection | The atomic greedy decision loop. |
| **(Distance, Angle, Order)** | metric $\leftrightarrow$ orientation $\leftrightarrow$ sequence | The geometric skeleton for next-stage containment. |
| **(Attraction, Rejection, Continuation)** | pick $\leftrightarrow$ skip $\leftrightarrow$ move-on | Rhythm of greedy traversal. |
| **(Seed, Nearest, Next)** | origin $\leftrightarrow$ pull $\leftrightarrow$ propagate | Converts the Stage 0 seed into a line of action. |

These triads remain **active but ungoverned** — there’s no stabilizing field yet (that appears in 1b).

---

## 🧠 4. Blueprint Step Mapping

| Blueprint Step | Manifestation in Greedy Logics |
| :--- | :--- |
| **S.01a Dualitas** | Pure local contrast — “shortest wins.” |
| **(latent s.00) Origo** | The inherited seed defines the origin of measurement. |
| **(proto s.01b) Trinitas** | Emerges implicitly through recurrent selection $\to$ path line (not yet full containment). |

### ✅ Stage 1a Summary

**Stage 1a – Dualitas = The Law of Local Contrast**

* **“The point that creates the field.”**
* **Purpose:** establish differentiation (nearest/farthest logic).
* **Representative Algorithms:** NN, GE, FN, DEG.
* **Structure:** binary choice loop — evaluate $\to$ pick $\to$ move.
* **Energetic Pattern:** sharp polarity, no feedback; defines the primal **greedy impulse**.
* **Outcome:** fast, locally coherent, globally erratic tours — raw material for Stage 1b containment.