# 🌱 Stage 0 – Origo / Seed

---

## 🔹 Essence

**Origo** is the **ignition point**: the origin or reference from which spatial relationships are defined.

At this stage there is **no structure yet**—only the **potential** for structure.

In constructive TSP heuristics, this corresponds to **choosing the first city** or **defining the coordinate frame** (centroid, pole, or seed set).

Even though it seems trivial, the **seed deeply influences the geometry that follows** (especially in 1a–1b stages).

---

## 🧩 1. Common Seed Initialization Options

| Type | Description | Typical Use / Motivation |
| :--- | :--- | :--- |
| **Random Start (uniform)** | Pick any city at random as start. | Baseline; ensures variability across runs (Monte Carlo, ensemble averaging). |
| **Nearest-to-Centroid** | Choose city closest to geometric center (mean of coordinates). | Symmetric entry point; minimizes bias for convex, evenly distributed sets. |
| **Farthest-from-Centroid** | Start at periphery; spiral inward. | Useful when the heuristic tends to collapse inward (e.g. GAO inward spiral). |
| **Leftmost / Lowest-Y** | Deterministic reference on convex hull. | Classical choice for planar sweeps (Sweep, Convex-Hull insertion). |
| **Random Cluster Seed** | Pick a random point within each cluster, then merge. | Multi-seed variant for cluster-first methods. |
| **Central-Density Seed** | Start in area of highest local density (via k-NN or kernel estimate). | Useful when data are non-uniform; promotes even expansion. |
| **K-Means Center Seed** | Use a pre-computed centroid of k-means clusters as pivot. | Semi-deterministic; supports hierarchical initializations. |
| **Deterministic Anchor (known hub)** | Start from a fixed, meaningful node (e.g. depot in VRP). | Problem-specific; preserves interpretability. |

So even “random start” has a whole design space — from **random**, to **centroid-anchored**, to **density-weighted** seeds.

---

## ⚖️ 2. Dualitas / Trinitas patterns inside Stage 0

Although Stage 0 itself precedes **Dualitas** (1a), every seed contains **proto-polarities** and **proto-fields**.

Here’s how they appear:

| Heuristic Aspect | Dualitas (latent polarity) | Trinitas (proto-containment / field) |
| :--- | :--- | :--- |
| **Choice principle** | Random $\leftrightarrow$ Deterministic | Blending both defines statistical vs geometric order. |
| **Spatial orientation** | Center $\leftrightarrow$ Periphery | Generates outward/inward growth bias. |
| **Frame of reference** | Point $\leftrightarrow$ Field | The seed city defines a point; the centroid defines a containing field. |
| **Multiplicity** | Single $\leftrightarrow$ Multi-Seed | One origin vs distributed origins (proto-ecology). |
| **Information basis** | Local $\leftrightarrow$ Global | Random = no context; centroid = global context. |

These dualities already “tune” the field into which Stage 1a (greedy contrast) will act.

---

## 🔺 3. Proto-Triads (emerging Trinitas fields)

Even at Origo, triads begin to coalesce as **potential containments**:

| Triad | Roles | Meaning / Use |
| :--- | :--- | :--- |
| **(Centroid, Point, Periphery)** | Global mean $\leftrightarrow$ chosen seed $\leftrightarrow$ outer boundary | Defines an implicit **polar field** for subsequent angular/radial measures. |
| **(Random, Deterministic, Weighted)** | pure random $\leftrightarrow$ fixed rule $\leftrightarrow$ probabilistic bias | Determines the statistical “temperature” of generation. |
| **(Seed, Frame, Density)** | discrete point $\leftrightarrow$ coordinate system $\leftrightarrow$ data texture | Sets up the canvas for geometry. |

So Stage 0 already encodes the **gestational geometry**—the womb out of which Dualitas will start pulling edges.

---

## 🧠 4. Summary (Blueprint lens)

| Blueprint Step | Manifestation in Seed Logics |
| :--- | :--- |
| **S.00 Origo** | Ignition of choice: pick an anchor or reference. |
| **(latent s.01a) Dualitas** | Local vs global; random vs deterministic tension. |
| **(latent s.01b) Trinitas** | Field emerges: centroid + orientation + boundary. |

### ✅ Positioning Summary

**Stage 0 – Origo: Seed / Start**

* "The point that creates the field."
* In algorithmic terms, this is the **origin definition step**—choosing a starting node or reference frame.
* **Design space:** Random $\leftrightarrow$ Deterministic $\leftrightarrow$ Weighted
* **Structural output:** A point and a potential field (centroid, orientation, density).
* **Energetic pattern:** Latent Dualitas (choice tension), emerging Trinitas (field coherence).