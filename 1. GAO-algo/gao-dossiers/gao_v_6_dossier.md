# GAO v6 Dossier — Weaving Mechanics: Bias, Elastic, Curvature (Expressio → Governance)

> **Scope.** This dossier formalizes **GAO Spiral v6**, which introduces **active Textura** via three weaving mechanisms—**Bias‑weave** (lattice rotation), **Elastic‑weave** (density‑responsive angular resolution), and **Curvature‑weave** (curvature‑driven lattice bending). v6 sits on top of v5’s adaptive breathing φ(t) and soft Fibonacci band fabric to create a **flexible, responsive geometry**.

**Prepared by:** Yves Langeraert with Enigma\
**Date:** November 2025

---

## 1. Executive Overview

**Objective.** Move from a responsive but largely static lattice (v5) to a **fabric that repositions itself** locally in response to flow, density and curvature.

**Conceptual leap.** From *adaptive motion within a fixed frame* → **co‑evolution of motion and frame** (the lattice becomes a participant).

**Blueprint stage.** *Expression → Governance (s.05–1/2 → s.05–3)* — adding structural degrees of freedom that regulate and coordinate flow.

---

## 2. 5W2H Breakdown

| W/H          | Description                                                                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Who**      | Yves Langeraert & Enigma; 1–2 contributors for mode ablations and perf profiling.                                                            |
| **What**     | Three weaving modes controlling the **Textura lattice**: Bias (rotation), Elastic (bin elasticity), Curvature (curvature‑driven re‑meshing). |
| **Why**      | Reduce crossings, increase fabric responsiveness, and improve Adaptatio/Textura balance across heterogeneous fields.                         |
| **Where**    | Implemented in `gao_spiral_v6_adaptive_weave()`; parameters extended in `GAOParams`.                                                         |
| **When**     | Sprint 5–6 (post v5 stabilization).                                                                                                          |
| **How**      | Modify binning / neighborhood selection before candidate scoring; keep v5 control signals and soft bands intact.                             |
| **How much** | Runtime +10–25% vs v5 (per mode); overall +15–35% when multiple modes combined.                                                              |

---

## 3. Mathematical Formulation

Let \(B_\theta\) be the baseline angular bin count (v5). At step t with running phase \(\alpha_t\):

### 3.1 Bias‑Weave (Lattice Rotation)

Apply a slow rotation to the angular lattice by phase drift \(\delta_t\): \(\delta_t = \rho_b\, t, \quad 0<\rho_b\ll 1.\) The effective bin index for a point with angle \(\theta\) becomes \(b_\theta^{\text{bias}}(\theta, t) = \Big\lfloor B_\theta \cdot \frac{(\theta + \delta_t)\bmod 2\pi}{2\pi} \Big\rfloor.\) **Intuition:** introduces a gentle shear that discourages persistent alignment artefacts, promoting diagonal weaving.

### 3.2 Elastic‑Weave (Density‑Responsive Angular Resolution)

Let \(d_t\) be the local normalized density (v3). Define an **effective** angular resolution \(B_\theta^{\text{eff}} = \operatorname{clip}\Big( B_\theta\,\big(1 - k_e (d_t - 1)\big),\; B_{\min}, B_{\max} \Big).\) Then \(b_\theta^{\text{elas}}(\theta, t) = \Big\lfloor B_\theta^{\text{eff}} \cdot \frac{\theta}{2\pi} \Big\rfloor.\) **Intuition:** crowding → fewer, wider bins (easier lateral movement); sparse regions → finer bins (more regular alignment).

### 3.3 Curvature‑Weave (Curvature‑Driven Band Shift)

Let \(\widehat{\Delta\theta}_t\) be the EW angular increment (v5). Define a curvature surrogate \(\kappa_t = \frac{|\widehat{\Delta\theta}_t - \phi_0|}{\phi_0}.\) Shift Fibonacci cumulative radii \(f_j\) by a small factor proportional to \(\kappa_t\): \(f_j^{\text{curv}} = f_j\,(1 + k_c\,\kappa_t).\) Band membership functions \(w_F\) and ring indices use \(f_j^{\text{curv}}\) instead of \(f_j\). **Intuition:** when curvature deviates from golden rotation, the radial fabric dilates/relaxes to follow the flow.

---

## 4. Integrated Candidate Selection (v6)

We retain v5’s cost structure and control signals but compute candidate neighborhoods and ring weights with the **mode‑adjusted lattice**: \(J_t(j) = \lambda_d\,\lVert p_j - p_{i_t}\rVert_2 + \lambda_\theta\,\Delta\theta_t(j)\,\Big(\tfrac{r_{i_t}}{r_{\max}}\Big)^{\eta} + \lambda_F\,(1 - w_F^{\text{mode}}(r_j))\,W_{b_r^{\text{mode}}(j)} + \lambda_C\,\Pi_t(j).\) Here \(w_F^{\text{mode}}, b_r^{\text{mode}}\) denote the **curvature‑shifted** band functions when curvature mode is active; the angular neighborhood uses **bias**/**elastic** indices when those modes are active.

---

## 5. Reference Pseudocode (mode hooks)

```python
def gao_spiral_v6_adaptive_weave(points, params):
    # assumes v5’s breathing, soft bands, and control already in place
    # here we show only the weaving hooks
    import numpy as np, math
    P = np.asarray(points); n = len(P)
    # ... compute C, r, theta, bins, fib cumulative f_c, etc. (as in v5)

    def local_density(bθ):
        # ±2 angular neighbors, unvisited counts normalized by mean
        ...

    def bias_bin(alpha, t):
        if params.weave_mode != 'bias':
            return int(Bθ * alpha / (2*np.pi)) % Bθ
        theta_shift = params.bias_rate * t
        return int((Bθ * ((alpha + theta_shift) % (2*np.pi)) / (2*np.pi))) % Bθ

    def elastic_bin(alpha, d_norm):
        if params.weave_mode != 'elastic':
            return int(Bθ * alpha / (2*np.pi)) % Bθ
        Bθ_eff = int(Bθ * (1 - params.k_elast * (d_norm - 1)))
        Bθ_eff = max(6, min(3*int(np.sqrt(n)), Bθ_eff))
        return int(Bθ_eff * alpha / (2*np.pi)) % Bθ_eff

    def curvature_shifted_fib(f_c, kappa):
        if params.weave_mode != 'curvature':
            return f_c
        return f_c * (1 + params.k_curvgrid * kappa)

    # main loop
    for t in range(1, n):
        # density & phase trackers (from v5)
        d_norm = local_density(...)
        kappa = abs(ew_dtheta - phi0) / phi0

        # choose angular bin according to mode
        if params.weave_mode == 'bias':
            bθ = bias_bin(alpha, t)
        elif params.weave_mode == 'elastic':
            bθ = elastic_bin(alpha, d_norm)
        else:
            bθ = int(Bθ * alpha / (2*np.pi)) % Bθ

        # candidate pool from neighborhood of bθ
        pool = ...

        # curvature-driven band shift for ring lookup
        f_c_mode = curvature_shifted_fib(f_c, kappa)
        def ring_idx(rv):
            return int(np.searchsorted(f_c_mode, rv, side='right'))

        # score candidates (as in v5) using ring_idx and wF with f_c_mode
        nxt = min(pool, key=lambda j: distance + ang_term + band_term + curvature_penalty)
        # update trackers (v5), update alpha by φ(t)
        ...
```

---

## 6. Complexity & Performance

| Mode          | Incremental cost vs v5 | Notes                                     |
| ------------- | ---------------------- | ----------------------------------------- |
| **Bias**      | \~+5–10%               | constant‑time extra angle shift.          |
| **Elastic**   | \~+10–15%              | effective bin recompute + bounds.         |
| **Curvature** | \~+10–20%              | per‑step shifted f\_c and ring search.    |
| **Hybrid**    | \~+20–35%              | combination; still O(n) after precompute. |

Overall still linear after precompute; constant factors increase modestly.

---

## 7. Stability & Control Notes

- **Bias rate (ρ\_b).** Choose ρ\_b ≈ φ0/(n·6) for gentle shear; too large causes drifting phase alignment.
- **Elastic gain (k\_e).** Keep in [0.15, 0.35]; large values create aliasing from rapid bin changes.
- **Curvature gain (k\_c).** Keep in [0.10, 0.20]; excessive dilation contracts/expands rings too aggressively.

**Interference control.** When combining modes, halve the individual gains to avoid over‑steering (superposition can amplify effects).

---

## 8. DQM Validation

| Dimension      | Description                                                                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data**       | Uniform, clusters, grid\_jitter (n=200–900). Prefer structured sets to expose mode benefits.                                                              |
| **Quality**    | Distinct metric signatures per mode; crossings ↓ (bias/curvature); Adaptatio ↑ (bias); Textura ↑ (elastic); Overall ↑ 0.02–0.05 vs v5 on structured sets. |
| **Management** | Run ablations per mode and hybrid; log build\_time\_ms; save candidate distribution & band occupancy deltas.                                              |

### Expected Metrics (n≈400, structured sets)

| Mode          | Dualitas | Adaptatio      | Textura        | Ecologia       | Overall        |
| ------------- | -------- | -------------- | -------------- | -------------- | -------------- |
| **Bias**      | ≈ v5     | **+0.03–0.06** | +0.01–0.02     | ±0.00          | **+0.02–0.04** |
| **Elastic**   | ≈ v5     | +0.01–0.02     | **+0.04–0.06** | ±0.00          | **+0.02–0.04** |
| **Curvature** | ≈ v5     | +0.00–0.02     | +0.02–0.03     | **+0.02–0.03** | **+0.02–0.04** |
| **Hybrid**    | ≈ v5     | +0.03–0.05     | +0.04–0.06     | +0.01–0.02     | **+0.04–0.08** |

---

## 9. Experimental Protocol

1. **Baselines.** Reproduce v5 metrics all datasets/seeds.
2. **Mode ablation.** Run v6 with each mode isolated; then `hybrid` with halved gains.
3. **Cluster sensitivity.** Use structured datasets to demonstrate improvements.
4. **Diagnostics.** Plot crossings, |Δr| variance, band occupancy changes, and angular neighborhood size.
5. **Acceptance.** Distinct metric shifts per mode; hybrid shows best Overall in ≥70% structured runs.

---

## 10. Observations & Behaviour

- **Bias** reduces persistent alignment artefacts; promotes diagonal interleaving of arms; often reduces crossings.
- **Elastic** adapts angular granularity to local density, improving Textura and preventing over‑tight turns.
- **Curvature** allows the fabric to follow flow—ring dilation smooths phase mismatches, modest Ecologia gains.
- On purely random uniform sets, improvements are smaller; on clustered or ring‑like structures, gains are marked.

---

## 11. Edge Cases & Failure Modes

- **Over‑steering (hybrid).** Combined gains too high → unstable oscillations; halve gains or stagger activations.
- **Micro‑clusters.** Elastic mode may compress bins excessively; cap Bθ\_eff ≥ 6.
- **Boundary dilation.** Curvature shift at large r may push candidates outward; taper k\_c with r/r\_max.

---

## 12. Unit Tests

| Test                 | Expected Outcome                                                           |
| -------------------- | -------------------------------------------------------------------------- |
| **Mode isolation**   | Bias/Elastic/Curvature runs differ from Base in tour order (hash/ID diff). |
| **Signature checks** | Bias: Adaptatio↑; Elastic: Textura↑; Curvature: Ecologia↑.                 |
| **Runtime bounds**   | v6 build\_time ≤ 1.35× v5 median for single mode.                          |
| **No regressions**   | Dualitas within ±0.005 of v5 median.                                       |

---

## 13. Change Log & Handoff

- Introduced **Bias**, **Elastic**, **Curvature** weaving mechanisms with parameterized gains.
- Integrated with v5’s adaptive φ(t) and soft band fabric.
- Established ablation protocol and diagnostic expectations.

**Next:** v7 composes multiple v6 spirals hierarchically (micro‑weaves + meta‑weave) and addresses parameter propagation across clusters.

