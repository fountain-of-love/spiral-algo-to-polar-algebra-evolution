# 🧭 Mixed-Domain CPU Architecture  
*(Confidential internal concept summary — 2025 draft)*  

---

## Overview
Shows what fits in one core (**no ISA change**) and what needs **ISA extensions** or **SoC/IP blocks**.  
Includes dependencies, synergy, and a pragmatic filing / implementation roadmap.  

---

## A) Execution / Issue / Rename  

**✅ Combine in one core (no ISA change)**  
DLX — Dynamic Linear-Flow Execution (linear)  
DCX — Dynamic Coordinate-Domain Scheduler (polar)  
VRRB — Vector-Reuse Rotation Buffer (linear)  
ARS — Arithmetic Reuse Scheduler (linear)  
RLSB — Register-Level Stream Buffer (linear)  
> DLX ↔ DCX complement linear chains vs rotational bursts; VRRB cuts rename churn for GEMM and polar sweeps.  

**🔧 Requires ISA / visible extension** – none  

---

## B) FPU / SFU (Compute Datapaths)  

**✅ Combine in one core (no ISA change)**  
MARU — Micro-Adaptive Rotation Unit (polar)  
PAAA — Precision-Adaptive Angle Arithmetic (polar)  
DPF — Dynamic Precision Fusion (FP16→FP32 dot) (linear)  

**🔧 Requires ISA / visible extension**  
CFMA — Complex Fused Multiply-Add (polar)  
ANORM — Branchless Angle Normalization µ-op (polar / soft-ISA)  
QTU — Quaternion 2×2–3×3 Micro-Unit (polar / 3D)  
SAVM — Shared-Accumulator Vector Mode (linear)  
> CFMA + QTU are headline opcodes; MARU / PAAA / DPF stay below ISA via compiler intrinsics.  

---

## C) SIMD / Vector Unit  

**✅ Combine in one core (no ISA change)** – none  

**🔧 Requires ISA / visible extension**  
ARGMIN.ANGLE — Angle-aware argmin + index (polar)  
HPVE — Hierarchical Polar Vector Extension (polar)  
SAVM — Shared-Accumulator Vector Mode (linear, see B)  
> Expose wrapped-angle compares, mixed (x,y)/(r,θ) lanes, and scalar reductions without horizontal steps.  

---

## D) Cache / Prefetch / Memory System  

**✅ Combine in one core (no ISA change)**  
ATPC — Adaptive Tile Prefetch (linear)  
AGPCM — Angle-Gradient Prefetch (polar)  
MBCM — Micro-Block Cache Mapper (linear)  
DTCM — Dual-Topology Cache Mapping (polar)  
MPAC — Micro-Tiled Polar Accumulator Cache (polar)  
ICRE — In-Cache Reduction (linear)  
ORLQ — Operand-Recycling Load Queue (linear)  
ATCB — Angle-Temporal Coherence Buffer (polar)  
> ATPC (2-D tiling) + AGPCM (spiral prefetch) span linear and polar flows; DTCM/MPAC/MBCM cut conflict misses; ICRE halves reduction bandwidth.  

**🔧 Requires ISA / visible extension** – none  

---

## E) Compiler / Runtime / OS  

**✅ Combine in one core (no ISA change)**  
CGLF — Compiler-Guided Linear Fusion (linear)  
Polar Auto-Vectorizer (polar)  
Hybrid Polar–Linear Backend (polar)  
RDGS — Rotational Dependency Graph Scheduler (polar)  
DD-JIT — Dynamic Domain JIT (both)  
RTA — Rotation-Aware Thread Affinity (polar)  
PLVC — Phase-Linked Vector Clock (polar)  
PISF / DSPI — Simulation & Profiling Interface (all)  

**🔧 Requires ISA / visible extension** – none (but can use new intrinsics when present)  

---

## F) Power / Thermal / Telemetry  

**✅ Combine in one core (no ISA change)**  
PDG — Power-Aware Dot-Product Governor (linear)  
EGEG — Energy-Gradient Execution Governor (polar)  
TPBC — Thermal-Phase Balancing Controller (polar)  
RWSU — Rotational Workload Signature Unit (polar)  

**🔧 Requires ISA / visible extension** – none (firmware + counters suffice)  

---

## G) SoC / Interconnect / I-O  

**✅ Combine in one chip (no ISA change)**  
GDMA — Geometric DMA Engine (polar)  
PNIP — Polar-Native Interconnect Protocol (polar)  
RPC-x — Rotational Precision Coherence for xPU (polar)  

**🔧 Requires ISA / visible extension** – bus / protocol specs only (MMIO / CSR interfaces)  

---

## H) Security / Entropy  

**✅ Combine in one core (no ISA change)**  
ADEG — Angle-Domain Entropy Generator (polar)  

**🔧 Requires ISA / visible extension**  
RHFU — Rotational Hash Function Unit (polar, new instruction or coprocessor call)  

---

## Dependency & Synergy Map  

**Foundational (no-ISA backbone)** — drop-in core:  
DLX, DCX, MARU, PAAA, DPF, ATPC, AGPCM, MBCM, DTCM, MPAC, ICRE, ORLQ, ATCB, CGLF, Hybrid Backend, RDGS, DD-JIT, PDG, EGEG, TPBC, RWSU, GDMA, PNIP, RPC-x, ADEG, PISF/DSPI.  
> Deliver substantial speed / power gains and ship without ISA review.  

**ISA “value multipliers” (optional but high-impact)** — CFMA, ARGMIN.ANGLE, HPVE, SAVM, ANORM (soft-ISA), QTU, RHFU.  
> Expose major software wins with graceful fallbacks.  

**Cross-reinforcements**  
• DLX + CGLF → linear-chain fusion  
• DCX + Hybrid Backend + DD-JIT → auto linear↔polar switch  
• ATPC / AGPCM + DTCM / MBCM / MPAC → memory locality  
• MARU + CFMA / HPVE → rotation-heavy kernels  
• ICRE + SAVM → dot-reduction efficiency  
• EGEG / PDG + RWSU → telemetry-driven power governance  

---

## Filing & Implementation Roadmap  

| Phase | Focus | Scope / Components | Value |  
|:--|:--|:--|:--|  
| 0 – Software / Compiler | Fast to file & ship | Polar Auto-Vectorizer, Hybrid Backend, CGLF, RDGS, DD-JIT, PISF/DSPI, RTA, PLVC | 1.2–2× uplift in geometry-heavy apps; lays HW groundwork |  
| 1 – µArch / Firmware | No ISA; single-core integration | DLX, DCX, MARU, PAAA, DPF, ATPC, AGPCM, MBCM, DTCM, MPAC, ICRE, ORLQ, ATCB, PDG, EGEG, TPBC, RWSU | +20–40 % throughput, −10–20 % power |  
| 2 – SoC / I-O | Fabric / coherence | GDMA, PNIP, RPC-x | CPU↔GPU synchronization; fewer cache storms |  
| 3 – ISA Enhancements | Selective high-ROI extensions | CFMA, ARGMIN.ANGLE, HPVE, SAVM, ANORM (soft), QTU, RHFU | Step-function inner-loop speedups; strong patent claims |  

---

## Integration Summary  

**✅ Fits in single core revision (no ISA)** – Everything in Phases 0–2 (software + µarch + SoC FW).  
> Safest path for near-term gain and defensible IP.  

**🔧 Truly needs ISA** – CFMA, ARGMIN.ANGLE, HPVE, SAVM, QTU, RHFU (+ optional ANORM).  
> Strategic extensions turn the design into a first-class Linear + Polar engine; each independently valuable, collectively defining a coherent mixed-domain CPU.  

---

*End of document — Internal Master Taxonomy (Linear + Polar Unified CPU Architecture, 2025).*
