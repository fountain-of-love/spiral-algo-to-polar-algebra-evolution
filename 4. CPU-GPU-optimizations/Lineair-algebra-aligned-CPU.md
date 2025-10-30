# 🧮 Linear Algebra on CPUs — Where to Push Further, Where ROI Falls Off  
*(2025 internal performance guidance draft)*  

---

## 1️⃣ Works Great Today (No ISA Changes)

**Use the right libraries and layouts**
- **Dense:** BLAS / BLIS / oneMKL / OpenBLAS  
- **Sparse:** SuiteSparse, Intel MKL Sparse  
- **Microkernel–blocked GEMM (BLIS-style):** tune `mc/nc/kc` for your cache (L1/L2/L3), use packed panels for reuse.  
- **SIMD:** compile with AVX2 / AVX-512 / SVE; enable FMA; add prefetch pragmas.  
- **Layouts:** SoA for vector ops; AoS→SoA around hot loops; align to 64 B; use huge pages for large data.  
- **Threading:** TBB / OpenMP with static partitioning for regular kernels; tasks for irregular. Avoid false sharing by cache-line padding.  
- **NUMA:** first-touch, thread pinning, interleaving for read-mostly tensors.  

**Payoff:**  
~90–100 % of vendor BLAS on key shapes; can beat it on **tall-skinny** and **small-batch** GEMMs using shape-specialized kernels.

---

## 2️⃣ Optimize Hard (Compiler / IR + Autotuning)

**Microkernel DSL / IR**
- Use MLIR Linalg or a tiny custom IR to declare tile sizes, vector widths, pack strategy.  

**Autotune per shape**
- Tune: `tile(M,N,K)`, pack(A|B), vector_width, threads/socket, prefetch distance, nontemporal stores.  

**Specialize by regime**
- **Small GEMM (8–128):** fully unrolled kernels, all data in L1.  
- **Tall-skinny:** panel-major packing, thread across skinny dimension.  
- **Batched tiny:** fuse batches into SIMD groups; use GEMM-STRIDED or custom SoA packing.  

**Sparse tricks**
- Pick format by density: CSR → general, BCSR → medium blocks, ELL/SELL-C-σ → quasi-regular.  
- Inspector–executor: reorder rows/cols for block density & SIMD-ability (RCM, graph partitioning), cache the plan.  

**Reduction & scan**
- Prefer tree reductions + vector horizontals; software-pipeline to hide L1 latency; use branchless masks for tails.  

**Payoff:**  
1.2–3× over stock libs on non-ideal shapes; 1.1–1.5× on core cases via better cache fit and fewer copies.

---

## 3️⃣ “Soft” ISA Extensions (Intrinsics / Compiler Patterns, No Silicon Change)

- **Complex FMA intrinsic (`z = a·b + c`)** on packed float2 → removes 4–6 µops per complex multiply-add.  
- **Horizontal argmin/argmax-with-index** → single-pass (val, idx) for top-k, pivoting, block selection.  
- **Block histogram / prefix-sum intrinsics** with cache-conflict avoidance → faster sparse pattern builds, radix binning.  
- **Vectorized transcendental bundles** — v{sincos}, vatan2 standardized as inlinable intrinsics; better fusion.  
- **Masked nontemporal store hints** — mark “one-shot” writes so hardware bypasses caches reliably.  
- **Load + permute idioms** — recognize AoS→SoA shuffles; map to `vpermt2` / `tbl` efficiently.  

**Payoff:**  
5–30 % typical uplift on mixed LA + geometry; major gains in **complex-valued** and **reduction-heavy** paths.

---

## 4️⃣ Hardware Wishlist (Small ISA / µArch Additions)

- **Native Complex FMA** → cmadd/cmacc treating registers as complex lanes.  
- **Small-matrix MMA in CPU** → 4×4 / 8×8 FP32/FP16 tiles for micro-GEMM, block-sparse kernels (not just INT8/AI).  
- **Scatter/gather with coalescing** → merge nearby lanes, lower TLB & bandwidth pressure.  
- **Vector prefix-sum / scan / indexed reduction** (min + arg) → faster pivoting, graph & sparse ops.  
- **Improved prefetch control** → user-space settable descriptors (stride, distance) per stream.  
- **L1 stream buffers** → keep 2 read + 1 write stream hot for panel-packed GEMM.  

**Payoff:**  
Moves CPU kernels toward GPU-class throughput while retaining branching agility — especially for block-sparse LA and batched tiny GEMMs.

---

## 5️⃣ Is It Worth It?

**Absolutely, when…**
- Working on **small / medium problem sizes**, mixed shapes, or latency-sensitive loops (ML pre/post, control, HFT, robotics).  
- Using **complex-valued** LA (signal, FFT, 2-D/3-D transforms).  
- Running **sparse or block-sparse** workloads where memory dominates and GPUs under-utilize.  
- Requiring **portability / low-dependency** deployment (CPUs everywhere).  

**Diminishing returns, when…**
- Massive dense GEMMs easily offloaded to GPU tensor cores; beyond that, CPU gains are marginal without AMX/SME or shape-special tuning.  

---

## 6️⃣ Compact Roadmap

### Exploit Today
- Switch to BLIS/oneMKL + shape-specialized paths.  
- Verify vector width usage & cache blocking.  
- Add packing + microkernels for hot shapes.  
- Enable NUMA pinning + huge pages.  

### IR + Autotune
- Express kernels in MLIR Linalg or TE.  
- Autotune tile/pack/prefetch per shape.  
- Generate intrinsic microkernels for small/batched cases.  

### Soft-Intrinsic Layer
- Wrap SVML/VML vector math.  
- Add intrinsics: complex FMA, argmin+idx, hist/scan.  
- Pattern-match AoS↔SoA shuffles.  

### Stretch
- If fleet allows, target **AMX (x86)** or **SME/SVE2 (ARM)** for micro-MMAs.  
- Adopt block-sparse layouts aligned to these tiles.  

### Quick-Win Checklist
- ✅ FMA + widest SIMD (AVX-512 / SVE) enabled — check perf counters.  
- ✅ Use BLIS tuned mc/nc/kc; add small-GEMM kernels.  
- ✅ AoS→SoA around hot loops; align + pad 64 B; avoid false sharing.  
- ✅ Add nontemporal stores for write-once outputs; prefetch panels (distance 2–3).  
- ✅ For sparse: reorder → BCSR / SELL-C-σ; inspector–executor schedule; batched SpMV + gather fusion.  

---

## 🧭 Bottom Line
Further **CPU-side linear-algebra optimization is absolutely worthwhile** for everything short of giant dense GEMMs.  
With **smart packing**, **shape-specialization**, and a **thin intrinsic layer**, expect **1.2–3×** gains over stock libraries in real pipelines — all while keeping the **latency and deployment simplicity** GPUs can’t match.
