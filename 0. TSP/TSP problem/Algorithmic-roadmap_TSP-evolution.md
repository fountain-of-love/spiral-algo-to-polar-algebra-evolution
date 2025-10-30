# 🗺️ Algorithmic Roadmap: TSP Evolution (Stage 0 $\to$ 13)

This roadmap charts the evolutionary journey of $\text{TSP}$ algorithms across the $\text{FIBO}$ (Form-In-Balance-Optimization) stages, mapping structural, computational, and energetic growth. The progression reflects increasing algorithmic intelligence, moving from random search to self-tuning systems.

---

## 0 — $\text{Origo}$ (Seed / Possibility ignition) 💡

| Field | Content |
| :--- | :--- |
| **Role** | Initialize the search’s entropy & geometry. |
| **Potential reached** | $35\%$ |
| **Primary bottlenecks** | Random or ad-hoc seeding; little instance-aware biasing. |
| **Near-term upgrades** | **Smart seeding** via $\text{k-means/medoids}$; Poisson-disk $\text{blue-noise}$ starts; multi-seed ensembles with diversity constraints; seed scoring by tour lower bounds. |
| **Speciation zones** | **Directed Seeding Intelligence** (learned seed policies); **Entropy-shaped bootstraps** (maximize future $\text{k-opt}$ gains); **Geometry-aware seeds** (field lines from vector flow). |
| **Milestones** | $\ge 1-2\%$ tour quality gain from seeds alone on $\text{TSPLIB}$-like sets; variance $\downarrow 50\%$; ensemble seed portfolio auto-select. |
| **KPIs** | Best-of-10 seed gap vs random; time-to-first-good-tour; improvement headroom captured by $\text{k-opt}$ after seeding. |
| **Risks/Mitigations** | Overfitting to structure $\to$ use cross-domain eval & diversity regularizers. |

---

## 1a — $\text{Dualitas}$ (Local choice / Greedy emergence) ⚖️

| Field | Content |
| :--- | :--- |
| **Role** | Fast local progress along a single gradient ($\text{angle} \leftrightarrow \text{radius}$, distance, etc.). |
| **Potential reached** | $60\%$ |
| **Primary bottlenecks** | Myopia; brittleness to noise; single-criterion selection. |
| **Near-term upgrades** | **Contextual greed** (multi-feature scoring: $\Delta\theta, \Delta r, \text{density}, \text{curvature}$); bounded candidate sets (angular/radial windows); tie-break by future ruin probability; incremental lower-bound checks. |
| **Speciation zones** | **Greedy-with-lookahead** (tiny rollouts); **Risk-aware greed** (ruin avoidance); **Field-sensing greed** (local density/anisotropy). |
| **Milestones** | Beat vanilla $\text{NN/Sweep}$ by $\ge 2-3\%$ at similar runtime; $\lt 5\%$ crossing inflation vs $\text{GAO}$-style order. |
| **KPIs** | Tour length vs $\text{NN}$; crossings per $1\text{k}$ nodes; runtime overhead vs $\text{NN}$. |
| **Risks/Mitigations** | Feature bloat $\to$ $\text{L1}$-sparse scoring & ablation. |

---

## 1b — $\text{Trinitas}$ (Containment / Early pruning) 🛡️

| Field | Content |
| :--- | :--- |
| **Role** | Add guardrails (bins, zones, bounds) to stabilize greedy flow. |
| **Potential reached** | $45\%$ |
| **Primary bottlenecks** | Static bins/thresholds; poor adaptive containment. |
| **Near-term upgrades** | Adaptive bin widths by local variance; soft exclusion rings; crossing-avoid masks; incremental $\text{MST/1-tree}$ bounds to veto bad hops. |
| **Speciation zones** | **Self-bounding fields** (containment evolves with flow); **Micro-cut reasoning** (cheap cuts during construction); **Local-global blend** ($\text{MST/1-tree}$ hints guiding stepwise building). |
| **Milestones** | $20-30\%$ crossing reduction at $\le 20\%$ time cost; veto layer blocks $\ge 60\%$ of later $\text{k-opt}$ repairs. |
| **KPIs** | Veto precision/recall; post-repair delta length; average bin entropy. |
| **Risks/Mitigations** | Over-pruning $\to$ fallback to exploration quota. |

---

## 2 — $\text{Adaptatio}$ (Sustained consistency) 🔄

| Field | Content |
| :--- | :--- |
| **Role** | Maintain smoothness & feasibility as structure accrues. |
| **Potential reached** | $50\%$ |
| **Primary bottlenecks** | Jerkiness in $\Delta r/\Delta\theta$; local traps. |
| **Near-term upgrades** | **Curvature-budgeting**; smoothness penalties; micro-relinks during construction; temperature-like noise for de-trapping. |
| **Speciation zones** | **Physically-plausible planners** (bounded curvature); **On-line micro-repairers**; **Consistency controllers** ($\text{PID}$-style signals on smoothness). |
| **Milestones** | Smoothness $\uparrow 30\%$ with $\le 1\%$ length cost; fewer $2\text{-opt}$ necessities. |
| **KPIs** | Path curvature stats; $2\text{-opt}$ gain needed; stall duration. |
| **Risks/Mitigations** | Oversmooth $\to$ keep a small “sharp turn” allowance. |

---

## 3 — $\text{Ecologia}$ (Constraint ecology fully active) 🌐

| Field | Content |
| :--- | :--- |
| **Role** | Integrate interdependencies; avoid global traps early. |
| **Potential reached** | $40\%$ |
| **Primary bottlenecks** | Static priorities; expensive exact signals. |
| **Near-term upgrades** | Learned edge-worth predictors; active-set candidate pools; “do-not-enter” region predictors; **hybrid neuro-symbolic vetoes**. |
| **Speciation zones** | **Adaptive pruning intelligence**; **Neuro-symbolic ecology** ($\text{GNN}$ scoring + symbolic checks); **Spatial risk maps** (forbidden funnels). |
| **Milestones** | $10-15\%$ search reduction for same quality in exact/$2\text{-opt}$ pipelines; fewer deep trap events. |
| **KPIs** | Branch factor; invalid/ruined edges taken; exact-solver node cuts saved. |
| **Risks/Mitigations** | Miscalibrated predictors $\to$ conformal calibration & abstain option. |

---

## 5 — $\text{Expressio}$ (Optimization frontier) ✨

| Field | Content |
| :--- | :--- |
| **Role** | Scale local $\leftrightarrow$ global coherence ($\text{k-opt}, \text{LK}, \text{Christofides}, \text{GAO}$). |
| **Potential reached** | $70\%$ |
| **Primary bottlenecks** | Manual tuning; static metrics; expensive neighborhoods. |
| **Near-term upgrades** | Adaptive $\text{k}$ selection; **energy–information balancing** (angle, distance, density); neighborhood caching & reuse; parallel multi-neighborhood racing. |
| **Speciation zones** | **Energy–information resonance** (self-tuning coherence weights); **Field-coupled optimization** (multi-criteria controllers); **Surrogate neighborhoods** (learned proxies for $\text{LK}$ moves). |
| **Milestones** | Match $\text{LK}$ quality at $\le 70\%$ time on medium instances; robust gains on anisotropic datasets. |
| **KPIs** | Quality–time Pareto; improvement per evaluation; cache hit-rate. |
| **Risks/Mitigations** | Overfit configs $\to$ auto-tuning via bandits. |

---

## 8 — $\text{Governance}$ (Metaheuristic regulation) 🏛️

| Field | Content |
| :--- | :--- |
| **Role** | Orchestrate strategies; balance explore/exploit across time. |
| **Potential reached** | $55\%$ |
| **Primary bottlenecks** | Fixed schedules; brittle hyperparameters; poor transfer. |
| **Near-term upgrades** | **Hyper-heuristics** with contextual state; bandit-style operator selection; curriculum schedules by instance signature; anytime checkpoints & restarts. |
| **Speciation zones** | **Meta-regulatory synthesis** (controllers that learn $\text{WHEN}$ to switch); **Policy distillation** (compress winning combos); **Self-diagnostics** (entropy & diversity monitors). |
| **Milestones** | $\ge 10\%$ wall-clock reduction for same quality across $10+$ corpora; graceful anytime behavior. |
| **KPIs** | Area-under-Pareto; operator utility curves; transfer gap across domains. |
| **Risks/Mitigations** | Controller thrash $\to$ smoothing & hysteresis; cap switch frequency. |

---

## 13 — $\text{Unio}$ (Reflexive/coherent meta-systems) 💫

| Field | Content |
| :--- | :--- |
| **Role** | Self-tuning solvers that reconfigure their own search. |
| **Potential reached** | $25\%$ |
| **Primary bottlenecks** | Sample inefficiency; stability; hardware coupling (quantum/analog). |
| **Near-term upgrades** | $\text{RL}$-guided neighborhood selection; **differentiable $\text{k-opt}$ layers** for gradient hints; solver architecture search ($\text{NAS}$) with cost-aware objective; quantum/analog co-design pilots. |
| **Speciation zones** | **Reflexive self-tuning systems**; **Neural-symbolic-quantum hybrids**; **Free-energy controllers** (minimize expected search regret). |
| **Milestones** | End-to-end policies beating tuned metaheuristics by $\ge 3-5\%$ quality at equal time; stable $\gt 1\text{e}6\text{-node}$ scaling via modularization. |
| **KPIs** | Improvement per wall-second; policy generalization to unseen geometries; reconfiguration events vs gains. |
| **Risks/Mitigations** | Collapse to trivial policies $\to$ entropy bonuses, population-based training; safety rails (symbolic veto). |

---

## 📊 Roll-up (Where the Headroom Is)

| Category | $\text{FIBO}$ Stages | Key Focus Area |
| :--- | :--- | :--- |
| **Largest untapped headroom** | **Stages 13** ($\text{Reflexive}$) and **3** ($\text{Adaptive pruning ecology}$). | Pushing $\text{AI}$ to self-reconfigure and deeply integrating constraint logic. |
| **Most immediate $\text{ROI}$** | **Stages 0, 1a/1b, 5.** | Smart initialization, highly contextual greedy construction, and self-tuning optimization ($\text{LK/GAO}$). |
| **Stability & scale enablers** | **Stage 8 governance.** | Necessary to orchestrate the complex, multi-component solvers developed in Stages 5 and 13. |