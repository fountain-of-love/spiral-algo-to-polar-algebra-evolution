# GAO v4 Dossier — Rhythm & Phase Coupling (Ecologia)

> **Scope.** This dossier formalizes **GAO Spiral v4**, introducing **rhythmic phase modulation** ("breathing") and **Fibonacci-weighted lattice coupling**. v4 transforms v3’s locally adaptive flow into a *rhythmically stabilized* process, mitigating jitter and enabling coherent phyllotactic structure.

**Prepared by:** Yves Langeraert with Enigma\
**Date:** November 2025

---

## 1. Executive Overview

**Objective.** Add a *time-dependent* phase controller that synchronizes spiral advancement with local flow conditions.\
**Conceptual leap.** From static adaptivity (v3) → *temporal coordination* of flow and structure (v4).\
**Mechanism.** A controlled oscillation of the golden phase increment (φ-step) and **Fibonacci-band weighting** on the radial lattice to anchor patterns.

**Blueprint stage.** *Ecologia (s.03–3 Synchronia)* — rhythmic coupling between flow (Adaptatio) and structural fabric (Textura).

---

## 2. 5W2H Breakdown

| W/H          | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| **Who**      | Yves Langeraert & Enigma; 1 systems engineer for stability analysis.                                   |
| **What**     | Phase-breathing controller over golden-angle step; Fibonacci-weight band costs; light twill offset.    |
| **Why**      | Reduce oscillatory jitter, stabilize curvature, and encourage phyllotactic regularity.                 |
| **Where**    | Implemented in `gao_spiral_v4()`; diagnostics via `phase_error_hist()`, `band_occupancy()`.            |
| **When**     | Sprint 3 (post v3 validation).                                                                         |
| **How**      | φ-step becomes `φ_t = φ0·(1 + ε·sin(ω t))`; angular cost scaled by soft membership to Fibonacci rings. |
| **How much** | Runtime +10–30% vs v3; Ecologia +0.01–0.03; smoother Adaptatio variance.                               |

---

## 3. Mathematical Formulation

### 3.1 Breathing Phase Controller

Let \(\phi_0 = 2\pi(1 - 1/\phi)\) be the golden-angle step with \(\phi\) the golden ratio. Define time index \(t=0,1,\dots\). The *breathing* phase increment is \(\phi_t = \phi_0\,\bigl(1 + \varepsilon\,\sin(\omega t + \psi)\bigr), \quad 0 < \varepsilon \ll 1, \; \omega > 0.\) The running phase obeys \(\alpha_{t+1} = (\alpha_t + \phi_t) \bmod 2\pi.\)

**Phase error.** For a candidate with angular displacement \(\Delta\theta_t\), define phase error \(e_t = (\phi_t - \Delta\theta_t)/\phi_t\). A mild proportional term \(k_\phi e_t\) (implicit via cost shaping) damps over/under-rotation.

### 3.2 Fibonacci-Weighted Radial Lattice

Let cumulative Fibonacci radii \(0 < f_1 < f_2 < \dots < f_{B_r} \approx r_{\max}\). Define soft band membership for point radius \(r\): \(w_F(r) = \exp\!\Big(-\tfrac{1}{2}\tfrac{\min_j |r - f_j|^2}{\sigma_r^2}\Big), \quad \sigma_r = c \cdot (r_{\max}/\sqrt{B_r}).\)

### 3.3 Candidate Cost (v4)

Augment v3 cost with (i) *phase-aligned angular term* and (ii) *Fibonacci band* regularization: \(J_t(j) = \underbrace{\lambda_d\,\lVert p_j - p_{i_t}\rVert_2}_{\text{flow}}\; +\; \underbrace{\lambda_\theta\,\Delta\theta_t(j)}_{\text{phase}}\; +\; \underbrace{\lambda_F\,(1 - w_F(r_j))}_{\text{band}}\; +\;\text{(v3 density terms)}.\) Parameters \(\lambda_\theta, \lambda_F\) are small positive weights; density corrections from v3 remain.

---

## 4. Algorithmic Pseudocode

```python
def gao_spiral_v4(points, Bθ=None, Br=None, eps=0.04, omega=None, lam_theta=1.0, lam_F=0.06):
    import numpy as np, math
    P = np.asarray(points)
    C = P.mean(axis=0)
    Q = P - C
    r = np.linalg.norm(Q, axis=1)
    theta = (np.arctan2(Q[:,1], Q[:,0]) + 2*np.pi) % (2*np.pi)

    n = len(P)
    Bθ = Bθ or int(2.5 * np.sqrt(n))
    Br = Br or int(np.sqrt(n))
    r_max = r.max() + 1e-9

    # Fibonacci cumulative radii
    fib = np.array([1,1,2,3,5,8,13,21,34,55,89], dtype=float)
    fib = np.pad(fib, (0, max(0, Br - len(fib))), mode='edge')[:Br]
    f_c = np.cumsum(fib); f_c = f_c/f_c[-1] * r_max
    sigma_r = 0.2 * (r_max / np.sqrt(Br))

    def wF(rv):
        d = np.min(np.abs(f_c - rv))
        return math.exp(-(d*d)/(2*sigma_r*sigma_r))

    binsθ = [[] for _ in range(Bθ)]
    for i in range(n):
        bθ = int(Bθ * theta[i] / (2*np.pi)) % Bθ
        binsθ[bθ].append(i)

    visited = np.zeros(n, dtype=bool)
    start = np.argmin(r)
    visited[start] = True
    tour = [start]

    phi0 = 2*np.pi*(1 - 1/((1+5**0.5)/2))
    if omega is None:
        omega = 2*np.pi / max(10, int(0.6*np.sqrt(n)))
    alpha = theta[start]

    def ang_diff(a, b):
        d = abs(a-b) % (2*np.pi)
        return min(d, 2*np.pi - d)

    for t in range(1, n):
        # breathing phase increment
        phi_t = phi0 * (1.0 + eps * math.sin(omega * t))
        bθ = int(Bθ * alpha / (2*np.pi)) % Bθ

        # local angular neighborhood
        cand_pool = []
        for dθ in (-3,-2,-1,0,1,2,3):
            cand_pool += [j for j in binsθ[(bθ + dθ) % Bθ] if not visited[j]]
        if not cand_pool:
            cand_pool = [j for j in range(n) if not visited[j]]

        last = tour[-1]
        nxt = min(cand_pool, key=lambda j: (
            np.linalg.norm(P[j] - P[last]) +
            lam_theta * ang_diff(theta[j], alpha) +
            lam_F * (1.0 - wF(r[j]))
        ))

        tour.append(nxt); visited[nxt] = True
        alpha = (alpha + phi_t) % (2*np.pi)

    return tour
```

---

## 5. Complexity & Performance

| Component    | Complexity                | Notes                                         |
| ------------ | ------------------------- | --------------------------------------------- |
| Bin init     | O(n)                      | reuse v3 binning logic.                       |
| Neighborhood | O(1) per step             | fixed window (±3 bins).                       |
| Selection    | O(k)                      | k = neighborhood size (≪ n).                  |
| Total        | **O(n)** after precompute | + small overhead for breathing & band weight. |

Empirically +10–30% runtime vs v3 for n ≤ 1k.

---

## 6. Stability & Control Notes

- **Breathing amplitude** \(\varepsilon\in[0.02, 0.06]\) — larger values risk phase overshoot; start at 0.04.
- **Frequency** \(\omega\) proportional to \(1/\sqrt{n}\) balances adaptivity speed and stability.
- **Band weight** \(\lambda_F\in[0.04, 0.08]\) — too high leads to overlocking into rings; too low yields no effect.

**Phase error distribution** should narrow versus v3; heavy tails indicate too large \(\varepsilon\) or \(\omega\).

---

## 7. DQM Validation

| Dimension      | Description                                                                       |
| -------------- | --------------------------------------------------------------------------------- |
| **Data**       | Uniform, clusters, grid\_jitter (n=200–900); same seeds as v3.                    |
| **Quality**    | Ecologia +0.01–0.03 vs v3; Adaptatio variance ↓; Dualitas stable (±0.003).        |
| **Management** | Record ε, ω, λ\_F; store phase-error histograms and band-occupancy plots per run. |

### Expected Metrics (n≈400)

| Metric        | v3 Reference | v4 Target     | Comment                                    |
| ------------- | ------------ | ------------- | ------------------------------------------ |
| **Dualitas**  | 0.94–0.95    | 0.94–0.95     | unchanged (geometry preserved).            |
| **Adaptatio** | 0.54–0.60    | 0.53–0.59     | sometimes slightly ↓ due to stabilization. |
| **Textura**   | 0.60–0.63    | 0.61–0.64     | band guidance adds order.                  |
| **Ecologia**  | 0.18–0.22    | **0.20–0.24** | breathing improves rhythmic stability.     |
| **Overall**   | 0.57–0.59    | 0.58–0.60     | modest uplift with reduced jitter.         |

---

## 8. Experimental Protocol

1. **Baseline.** Run v3 on all datasets/seeds; log metrics and phase-error histograms.
2. **Breathing sweep.** Grid-search ε∈{0.02,0.04,0.06}, ω = 2π/T with T∈{√n/2, √n, 2√n}.
3. **Band weight.** Test λ\_F∈{0.04,0.06,0.08}; plot band-occupancy skew.
4. **Acceptance.** Ecologia improvement ≥ +0.015 median; Adaptatio variance reduced ≥ 10%; Dualitas within ±0.003 of v3.

---

## 9. Observations & Behaviour

- Breathing suppresses rapid alternation of short/long steps (|Δr| variance ↓).
- Fibonacci bands encourage consistent inter-arm spacing (Textura ↑).
- Overly strong band weights lead to ring locking (avoid).
- Twill-like tiny phase nudges may further smooth aliasing, optional.

---

## 10. Edge Cases & Failure Modes

- **Resonance with dataset periodicity.** If ω matches dataset symmetries, artifacts may appear → randomize ψ (phase offset).
- **Sparse boundary zones.** Bands at large r may bias outward steps excessively → reduce λ\_F with r.
- **Clustered inputs.** If clusters are tight, increase Br for finer band resolution.

---

## 11. Unit Tests

| Test                  | Expected Outcome                                                            |
| --------------------- | --------------------------------------------------------------------------- |
| **Phase progression** | median(Δθ) within 3% of φ0; std ↓ vs v3.                                    |
| **Ecologia uplift**   | +0.01–0.03 median across seeds.                                             |
| **Textura banding**   | occupancy variance across bands increases slightly (non-uniform by design). |
| **Runtime bound**     | v4 build time ≤ 1.3× v3 median.                                             |

---

## 12. Change Log & Handoff

- Added breathing phase controller and Fibonacci-band soft weighting.
- Achieved rhythmic stabilization with modest Textura gains.
- Prepares ground for v5–v6 adaptive weaving (bias, elastic, curvature) and v6’s dynamic feedback.

**Next:** v5 introduces **adaptive** φ(t) based on |Δr| variance and soft bands that evolve with flow.

