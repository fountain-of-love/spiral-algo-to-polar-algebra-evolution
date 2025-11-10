# 🧩 GAO Spiral — Troubleshooting & FAQ

## ⚙️ Common Setup Issues

### 1. Environment or Import Errors
**Symptom:** `ModuleNotFoundError: No module named 'numpy'` or similar.

**Fix:**
```bash
pip install -r requirements.txt
```
If the problem persists, ensure your virtual environment is active:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

---

### 2. Notebook Fails to Load GAO Functions
**Symptom:** `NameError: name 'gao_spiral_v6_adaptive_weave' is not defined`

**Fix:** Make sure you’ve run the import cell or file:
```python
from gao_spiral import *
```
If using modular scripts, restart the kernel after editing code.

---

### 3. Version Conflicts (v5, v6, v7)
**Symptom:** Older notebooks reference outdated signatures.

**Fix:**
- Use the newest function definitions: `gao_spiral_v6_adaptive_weave()` or `gao_spiral_v7_hierarchical()`.
- Check argument names: new versions accept `weave_mode`, `bias_rate`, `k_elast`, `k_curvgrid`, `**kwargs`.

---

### 4. Scenarios Returning Identical Scores
**Symptom:** All scenarios show the same metrics despite different parameters.

**Cause:** Weave modes not activated; hierarchical sub‑spirals reuse the same parameter reference.

**Fix:** In `gao_spiral_v7_hierarchical()`:
```python
local_params = GAOParams(**vars(params))  # clone params per cluster
```
Then verify different sub‑spirals produce unique paths.

---

### 5. Runtime Extremely Slow
**Symptoms:** Large `build_time_ms` (hundreds of ms or seconds).

**Causes:**
- High `k_clusters` → many local spirals.
- Frequent re‑grid interval (`k_regrid` too small).
- Large dataset (n>900) without caching.

**Fixes:**
- Reduce `k_clusters` to 3–5.
- Increase `k_regrid` to 20–30.
- Enable coarse density caching or run smaller n for diagnostics.

---

## 🧠 Coherence Metric Questions

### Why is Textura always 0.594?
Because the lattice remains static or unresponsive. To change it, enable **elastic** or **bias** weave modes and ensure dataset has spatial variance (not purely random uniform points).

### Why does Overall plateau around 0.58?
That’s the equilibrium of a non‑learning adaptive spiral on random fields. To exceed it, use structured data (clusters, rings) or enable hierarchical v7 with distinct weave modes.

---

## 🔬 Development & Debug Tips

| Tip | Command / Action |
|-----|------------------|
| View first tour indices per cluster | `print(tour[:10])` inside v7 main loop |
| Check parameter propagation | `print(vars(params))` before sub‑spiral call |
| Visualize coherence | Plot Adaptatio vs Textura scatter to see flow balance |
| Profile runtime | `%%timeit` in Jupyter or Python `time` module |
| Log metrics | `df.to_csv('metrics_log.csv', index=False)` |

---

## 🧭 When to Ask for Help
- **Algorithmic behaviour unclear?** → Ping Enigma/Yves with dataset + seed.
- **Code bug or crash?** → Create issue on repo with traceback.
- **Performance regression >2× baseline?** → File a “perf” issue and include timing table.

---

## ✅ Quick Diagnostic Checklist
1. [ ] Environment clean, correct Python version.
2. [ ] Latest GAO functions loaded.
3. [ ] Scenarios defined with unique parameters.
4. [ ] Weave modes activated and reflected in logs.
5. [ ] Metrics table saved to `/outputs/`.
6. [ ] Results reviewed and interpreted via coherence matrix.

---

**End of FAQ** — Keep this sheet pinned in your onboarding folder for quick debugging.

