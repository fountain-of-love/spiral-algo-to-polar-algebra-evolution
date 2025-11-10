# 🚀 GAO Spiral — Quick Start for New Contributors

## 🌱 Purpose
This brief onboarding guide helps new team members quickly understand the GAO Spiral project, its goals, and how to get started working with the current codebase.

---

## 🔍 1. What is the GAO Spiral?
The **GAO Spiral** is a generative optimization algorithm inspired by natural spirals, weaving dynamics, and Fibonacci scaling. It evolves through multiple feedback layers, each adding intelligence, adaptivity, and structure to how points are connected.

You can think of it as moving from a **simple greedy spiral** → to an **adaptive living geometry** → to a **multi-scale self-organizing system.**

---

## 🧭 2. Core Concepts

| Term | Meaning |
|------|----------|
| **Dualitas** | Geometric coherence — how stable the spiral’s shape is. |
| **Adaptatio** | Flow adaptation — how smoothly the spiral adjusts to density. |
| **Textura** | Structural coherence — the internal lattice/fabric. |
| **Ecologia** | Rhythmic feedback — stability of phase and oscillation. |
| **Overall** | Composite coherence score (systemic balance). |
| **Blueprint model** | Framework mapping algorithm evolution to systemic stages (Field → Flow → Expression → Learning → Unity). |

---

## 🧩 3. Versions & Focus

| Version | Focus | Core Mechanism |
|----------|--------|----------------|
| **v1–v2** | Field geometry | Golden-angle placement (static field). |
| **v3** | Flow adaptivity | Density-aware candidate selection. |
| **v4** | Rhythm & phase | Fibonacci lattice and breathing φ control. |
| **v5–v6** | Expression | Adaptive breathing, soft lattice, weaving modes. |
| **v7** | Governance / Hierarchy | Multi-scale clustering and meta-spiral. |
| **v8 (planned)** | Learning / Self-tuning | Meta-optimization based on coherence deltas. |

---

## 🛠️ 4. Environment Setup

### Requirements
- **Python 3.10+**
- **Packages:** `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `notebook`

### Setup
```bash
# clone repo
$ git clone <repo_url>
$ cd gao_spiral

# create environment
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

---

## 🧪 5. How to Run Tests

1. Open `GAO_Spiral.ipynb` in Jupyter.
2. Choose algorithm version (`gao_spiral_v6_adaptive_weave` or `gao_spiral_v7_hierarchical`).
3. Run pre-defined scenario cells:
   ```python
   results_v6 = [run_v6(name, **kw) for name, kw in scenarios_v6]
   display(df_v6.sort_values("Overall", ascending=False))
   ```
4. Compare results across modes: Base, Bias, Elastic, Curvature, Hybrid.

---

## 📈 6. Reading Results

| Metric | Interpretation | Target |
|---------|----------------|---------|
| **Dualitas** | Shape stability | > 0.94 |
| **Adaptatio** | Flow smoothness | > 0.55 |
| **Textura** | Fabric responsiveness | > 0.60 |
| **Ecologia** | Rhythmic balance | 0.22–0.28 |
| **Overall** | Systemic coherence | 0.60–0.70 |

---

## 📋 7. Contributor Workflow

1. **Create a feature branch**: `feature/v8_textura_reweave`.
2. **Document every run** in `/logs/metrics_<date>.csv`.
3. **Push updates** with clear commit messages: `feat: add curvature weave feedback`.
4. **Review checklist:**
   - ✅ Code runs without error
   - ✅ Metrics logged
   - ✅ Scenario results saved in `/outputs/`
   - ✅ Notebook updated with notes

---

## 🧭 8. Learning Path

| Step | Resource |
|------|-----------|
| 1 | Read `GAO_Spiral_Overview_v7.md` (full system context). |
| 2 | Run v6 and v7 scenarios to see behaviour. |
| 3 | Review code for `choose_candidate()` to understand flow logic. |
| 4 | Experiment with weave parameters (`bias_rate`, `k_elast`, `k_curvgrid`). |
| 5 | Contribute to v8 (self-tuning and learning feedback). |

---

## 🌟 9. Quick Orientation Summary
- **Goal:** Build an algorithm that learns to weave itself.
- **Current State:** Stable adaptive spiral (v7) awaiting activation of weave feedbacks.
- **Next Leap:** v8 → self-reweaving, learning spiral.
- **Mindset:** Think like nature — iterative, adaptive, harmonic.

