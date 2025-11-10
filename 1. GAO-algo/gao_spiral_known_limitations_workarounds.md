# ⚠️ GAO Spiral — Known Limitations & Workarounds

This document lists the **current constraints** and **practical workarounds** in the GAO Spiral development as of **version 7 (Hierarchical Adaptive Spiral)**. It helps contributors and testers understand what behaviors are expected, which ones are open issues, and how to mitigate them in the short term.

---

## 🧩 1. Weave Modes Not Affecting Results
**Issue:** In v7 runs, Bias/Elastic/Curvature/Hybrid weave modes often yield identical scores.

**Cause:** The hierarchical controller reuses the same parameter reference across clusters, so sub‑spirals share identical logic and outcome.

**Workaround:**
```python
local_params = GAOParams(**vars(params))  # clone per cluster
```
Then ensure `k_clusters` ≤ 5 so each cluster is large enough for mode differentiation.

**Status:** Fix scheduled in v7.1 (parameter propagation patch).

---

## ⚙️ 2. Runtime Scaling in v6–v7
**Issue:** Build time grows super‑linearly with n (especially >400) due to frequent density re‑grid and per‑cluster loops.

**Workarounds:**
- Increase `k_regrid` interval to 20–30.
- Cache density and reuse between steps.
- Reduce cluster count (3–5 typical sweet spot).

**Status:** Optimization planned for v8 (density caching layer).

---

## 🌀 3. Textura Plateau at 0.594
**Issue:** Structural coherence (Textura) remains constant across runs.

**Cause:** Lattice grid static or weave feedback inactive.

**Workarounds:**
- Use **Elastic** or **Bias** modes.
- Ensure dataset has variance (clustered or ringed structure). Pure random uniform sets show little difference.

**Status:** Active Textura reweaving (v8) will resolve this.

---

## 🧠 4. Identical Tours Across Seeds
**Issue:** Same output tour even when seed changes.

**Cause:** Deterministic cluster ordering and consistent random seed propagation.

**Workaround:**
- Introduce randomness per cluster (e.g., `np.random.seed(seed + c)`).
- Randomize cluster order before concatenation.

**Status:** To be added in v7.2 for more varied spiral geometries.

---

## 📏 5. Crossings Not Reduced by Weaving
**Issue:** Crossings count sometimes increases with adaptive feedback.

**Cause:** Weave mechanics introduce longer angular jumps without self‑untangling logic.

**Workarounds:**
- Enable curvature mode only after bias or elastic confirmed stable.
- Consider adding lightweight 2‑opt post‑pass guided by coherence delta.

**Status:** Post‑processing step planned for v8 to rebalance crossings.

---

## 🧩 6. Cluster Edge Artifacts (v7)
**Issue:** Visible discontinuities at cluster boundaries.

**Cause:** Local spirals built independently, without smoothing continuity between last point of one cluster and first of next.

**Workarounds:**
- Introduce small overlap region when partitioning clusters.
- Add smoothing pass that connects cluster boundaries with mid‑points.

**Status:** Fix under design; will be integrated in v8’s multi‑level merge logic.

---

## 🧮 7. Coherence Metrics May Hide Structural Change
**Issue:** Identical metric values can occur even if geometry differs slightly.

**Cause:** Current scoring resolution too coarse for subtle topological variation.

**Workarounds:**
- Visualize tours or add alternative metrics (crossings per unit length, curvature variance).
- Compare `df.describe()` of r‑θ differences instead of single overall score.

**Status:** Diagnostic enrichment task open; expected in analytics v2 module.

---

## 📈 Summary Table

| Limitation | Impact | Temporary Fix | Target Version |
|-------------|---------|----------------|----------------|
| Weave modes inert | Medium | Clone params per cluster | v7.1 |
| Runtime scaling | High | Increase k_regrid / cache density | v8 |
| Textura plateau | Medium | Structured data + weave mode | v8 |
| Identical tours | Low | Randomize per cluster | v7.2 |
| Crossings | Medium | Add 2‑opt correction | v8 |
| Cluster edges | Medium | Overlap smoothing | v8 |
| Metric resolution | Low | Add visual + alt metrics | analytics v2 |

---

**Note:** These limitations are normal in the transition from *adaptive* to *learning* GAO phases. Each workaround provides a short‑term path until self‑reweaving (v8) stabilizes the full feedback architecture.

