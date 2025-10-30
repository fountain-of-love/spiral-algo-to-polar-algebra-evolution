# 📖 Bibliography: Key Papers on TSP Initialization (Seeding)

This one-page bib sheet summarizes seminal and recent works related to initialization/seeding strategies in the $\text{Travelling Salesman Problem}$ ($\text{TSP}$) domain, highlighting their focus and relevance to structured seeding.

| \# | Citation | Seeding / Initialization Focus | Notes & Key Quotes |
| :--- | :--- | :--- | :--- |
| 1 | **Platzman \& Bartholdi (1989)**: "Spacefilling curves and the planar travelling salesman." | **Space-Filling Curve ($\text{SFC}$) Ordering** used as a constructive heuristic start for planar $\text{TSP}$. | "To construct a short tour … the points are sequenced as they appear along a space-filling curve." Also provides worst-case analysis: $O(\log n)$ factor. |
| 2 | **Huang (2017)**: "Investigating $\text{TSP}$ Heuristics for Location‑Based Services." | Uses **Hilbert/Strip curves** to define the initial tour ordering for Euclidean $\text{TSP}$ in a practical context. | "The space filling curve … keeps the locality information … visiting query nodes in the order of their appearance … reduces the total route length." |
| 3 | **Agostinelli (2017)**: "Density‑Based Clustering Heuristics for the Traveling Salesman Problem." | Uses **Clustering ($\text{DBSCAN}$)** to partition and seed heuristic tours in $\text{TSP}$. | "Novel design combining classic heuristics with density-based clustering … for the Traveling Salesman Problem." Supports the **"Clustering-driven seeding"** family. |
| 4 | **Alkafaween (2024)**: "An Efficiency Boost for Genetic Algorithms: Initializing the Population with a Greedy Approach." | Initialization (seeding) of the **population in Genetic Algorithms ($\text{GA}$)** for $\text{TSP}$; compares greedy seeding vs. random. | "The proposed method … starts by adding four extreme cities … then adding each city via a greedy strategy … The experimental results demonstrate … better than other $\text{GAs}$ that use conventional seeding strategies." |
| 5 | **Ahmed et al. (2014)**: "The Ordered Clustered Travelling Salesman Problem." | Focuses on **clustered instances ($\text{CTSP}$)** and heuristics, demonstrating how explicit cluster handling impacts tour structure. | Provides heuristic algorithms for $\text{CTSP}$ and discusses impact of clustering on tour structure. Relevant for defining **cluster-aware seeding strategies.** |
| 6 | **Rosenkrantz et al. (1977)**: "An Analysis of Several Heuristics for the Traveling Salesman Problem." | Early analysis of constructive heuristics like $\text{Nearest Neighbor}$ ($\text{NN}$); sets a **baseline for naive/random starting conditions**. | Useful for understanding the baseline "random / naive ordering" vs. more structured starts and motivating the need for better seeding. |

---

## 🛑 Key Gaps \& Opportunities for New Contribution

These papers confirm the value of non-random starts but reveal specific omissions addressed by a systematic seeding blueprint:

1.  **Missing Systematic Comparison**: None of these papers systematically compare the performance of **different seeding families** (e.g., $\text{SFC}$ vs $\text{Clustering}$ vs $\text{MST}$) when aligned with **different greedy heuristics** ($\text{NN, CI, Sweep, GAO}$) in a unified experimental framework.
2.  **Under-Explored Geometries**: The **angle–radius, blue-noise, or Poisson-disk** seeding idea, crucial for $\text{GAO/Sweep}$ alignment, appears **absent or severely under-explored** in the $\text{TSP}$ literature.
3.  **No Adaptive Pipeline**: There is little evidence of a production-ready **instance-profiling ($\text{geometry features}$) $\to$ seeding strategy selection pipeline**. Most current seeding work is for **metaheuristics** ($\text{GA, EA}$) rather than pure **greedy + local search** pipelines.