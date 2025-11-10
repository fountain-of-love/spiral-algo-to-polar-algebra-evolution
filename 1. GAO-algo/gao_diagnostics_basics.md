# GAO Diagnostics — Fundamentals & Quality Metrics

> **Purpose.** This document explains the diagnostic philosophy and basic evaluation framework used throughout the GAO Spiral algorithm family (v1–v8). It focuses on *quality-based* rather than *cost-based* diagnostics — emphasizing coherence, flow, and systemic behaviour rather than path length alone.

**Prepared by:** Yves Langeraert with Enigma  
**Date:** November 2025

---

## 1. Diagnostic Philosophy

Traditional algorithms (e.g., TSP solvers) measure **distance**, **cost**, or **time efficiency**. GAO introduces a **qualitative diagnostic paradigm** based on coherence metrics that assess *how well the algorithm expresses systemic intelligence* — not merely how short the path is.

These diagnostics act as **mirrors of system quality** rather than mere performance counters.

### Key Principles
- **Quality over cost:** Evaluate structural coherence, not minimal length.
- **Flow before speed:** Stable, rhythmic evolution is prioritized over greedy optimization.
- **Dimensional metrics:** Every version (v1–v8) expresses improvement along four main quality axes.
- **Comparative continuity:** Diagnostics ensure evolutionary consistency between versions.

---

## 2. Core Coherence Metrics

GAO diagnostics use a **four-axis coherence model** that evolved with the Blueprint framework:

| Metric | Description | Intuitive Analogy |
|---------|-------------|------------------|
| **Dualitas** | *Geometric consistency*: how well the spiral preserves proportional angular progression and global symmetry. | Field geometry / stability. |
| **Adaptatio** | *Flow quality*: smoothness of radial transitions and adaptability to spatial density. | Breath / rhythm of motion. |
| **Textura** | *Fabric coherence*: regularity of structural spacing and inter-arm relationships. | Weave pattern consistency. |
| **Ecologia** | *Rhythmic balance*: synchronization between flow and structure, phase stability over time. | Ecosystemic resonance. |
| **Overall** | Composite quality score derived from weighted sum or PCA of the above. | Global coherence index. |

Each metric maps to Blueprint triads:  
**Dualitas** → Structure, **Adaptatio** → Flow, **Textura** → Fabric, **Ecologia** → Rhythm.

---

## 3. Diagnostic Layers

Diagnostics are divided into **three layers**:

### 3.1 Local Diagnostics
- **Δr Variance:** Measures stability of radial step sizes.
- **Δθ Regularity:** Checks angular phase distribution around the golden angle.
- **Local Density Field:** Quantifies bin occupancy and uniformity.
- **Instantaneous Flow Feedbacks:** Monitors u_t (phase control signal), m_r, and v_r traces.

### 3.2 Structural Diagnostics
- **Crossings Count:** Detects self-intersections or pattern discontinuities.
- **Band Occupancy Distribution:** Evaluates how evenly the Fibonacci rings are populated.
- **Curvature Smoothness:** Evaluates the continuity of directional curvature.
- **Adaptive Weave Metrics (v6+):** Monitors how well bias, elasticity, or curvature mechanisms regulate flow.

### 3.3 Systemic Diagnostics
- **Coherence Evolution Curves:** Track Dualitas, Adaptatio, Textura, Ecologia over time.
- **Phase Error Histograms:** Evaluate rhythmic stability (v4+).
- **Meta-Coherence Maps:** (v7+) Visualize inter-cluster coordination and global phase locking.
- **Learning Trajectories:** (v8+) Plot coherence deltas across epochs.

---

## 4. Measurement Process

1. **Run GAO variant (vX)** with fixed dataset, seed, and parameter set.  
2. **Collect raw traces:** positions, r(t), θ(t), control signals, timing.  
3. **Compute derived quantities:** Δr, Δθ, flow variance, phase error, etc.  
4. **Aggregate into metrics:** compute 4 coherence scores (0–1 scale).  
5. **Store & visualize:** export as CSV, plot time-based traces, radar plots, and phase histograms.

Each diagnostic notebook (e.g., `diagnostics_gao.ipynb`, `diagnostics_GAO_Adaptatio.ipynb`) provides modular routines for these steps.

---

## 5. Interpretation Framework

| Metric Shift | Interpretation |
|---------------|----------------|
| **Dualitas ↓, Adaptatio ↑** | Algorithm becomes more fluid but less geometrically constrained (good for dense or clustered sets). |
| **Textura ↑, Ecologia ↑** | Strong structural rhythm emerging — coherence improving. |
| **Adaptatio variance ↓** | Flow stabilizing; successful adaptive control. |
| **Crossings ↓, Overall ↑** | Major systemic improvement. |
| **All flat (≈constant)** | Indicates architecture saturation — time for structural change (next GAO version). |

---

## 6. Practical Outputs for Collaborators

### Key Plots
- **Phase error histogram:** Evaluate rhythmic coherence (v4+).
- **Band occupancy heatmap:** Check distribution uniformity (v4+). 
- **Flow variance trace:** Verify stability of adaptive control (v5+).
- **Cluster coherence map:** Inspect global-local alignment (v7+).
- **Learning convergence curve:** Observe coherence delta stabilization (v8+).

### Key Files
| File | Purpose |
|------|----------|
| `compare_GAO_v2.ipynb` | Baseline comparison of cost and coherence metrics (v1–v2). |
| `diagnostics_gao.ipynb` | Core diagnostic suite — geometry, flow, structure. |
| `diagnostics_GAO_Adaptatio.ipynb` | Specialized Adaptatio diagnostics and flow-trace analysis. |

---

## 7. Diagnostic Mindset

- Diagnostics are **not scores of success** but **expressions of balance**.  
- Focus on *interrelations*: how one metric rises as another stabilizes.  
- Treat anomalies as **signals of new behaviour**, not errors.  
- Diagnostics should **invite curiosity**, not only validation.

---

## 8. Next Steps — Toward a Benchmark Suite

In future releases, diagnostics will evolve into a **benchmark folder** integrating:
- Parametric sweeps (ε, λ_F, weave gains, φ amplitude).  
- Multi-seed statistical analyses.  
- Visual coherence dashboards.  
- Automated DQM validation hooks for each GAO version.

---

**Summary:**  
Diagnostics in GAO are qualitative mirrors — they measure *coherence, balance, and emergent order* across algorithmic evolution. They help collaborators see *how* an algorithm learns, not just *what* it achieves.