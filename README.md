# xAO — Future-Aware Optimization

> **From greedy decisions to decisions that preserve future value.**

This repository explores a simple question:

> **Can an optimization algorithm make better local decisions by accounting for what those decisions enable next?**

Many constructive optimization algorithms are deliberately greedy: at each step, they choose the move that looks best **right now**. That is fast and often useful. But in problems such as the **Travelling Salesman Problem (TSP)**, a locally attractive move can reduce the quality of the choices that remain. A move can be cheap now and expensive later.

The work in this repository explores an alternative:

> **Evaluate the next move not only by its immediate value, but by the value it creates, preserves, or unlocks for the moves that follow.**

This is the central idea behind **xAO — a framework for Future-Aware Optimization.**

## How the work fits together

The repository can be understood as four connected layers:

```text
                         xAO
                          │
             ┌────────────┼────────────┐
             │            │            │
            TSP          GAO        xAO family
         proving       concrete     generalized
          ground       algorithm     framework
           │             │             │
           └─────────────┼─────────────┘
                         │
                       PAPER
              Unified Future-Aware
                   Optimization
```

### TSP - the proving ground

The **Travelling Salesman Problem** provides the concrete environment in which the core hypothesis is explored. TSP makes the weakness of purely greedy decisions easy to see:

> The cheapest next move is not necessarily the move that leads to the best complete tour.

The TSP work explores how decisions can become increasingly aware of the structure they create.

### GAO - the concrete algorithm

**GAO (Geometry-Aware Optimization)** is one of the first concrete implementations of the idea. It introduces geometric information into the decision process, asking not only which next edge is attractive, but how that edge fits into the route that is being constructed. GAO is therefore an important bridge between the TSP experiments and the broader xAO framework.

### xAO family - the generalized framework

The **xAO family** generalizes the underlying principle beyond geometry. Different xAO variants explore different forms of structural information:

- **GAO** — Geometry-Aware Optimization
- **DAO** — Density-Aware Optimization
- **PAO** — Proportion-Aware Optimization
- **SAO** — Symmetry-Aware Optimization
- **TAO** — Topology-Aware Optimization
- **RHO** — Rhythm-Aware Optimization

The intention is not to create a collection of unrelated heuristics. The common question is:

> **What information about the current state tells us which decision will create better future possibilities?**

### The paper - the unified framework

The paper brings these ideas together: **xAO: A Unified Framework for Future-Aware Optimization** It provides the conceptual and mathematical framework connecting the TSP work, GAO and the wider xAO family.

## The TSP hypothesis

A conventional greedy strategy asks:

```text
What is the cheapest next move?
```

xAO asks:

```text
What next move creates the most value
for the moves that follow?
```

Consider two candidate moves:

```text
Candidate A
    ↓
shorter immediately
    ↓
but constrains the remaining route


Candidate B
    ↓
slightly longer immediately
    ↓
but preserves better subsequent connections
```

A purely greedy algorithm chooses **A**. A future-aware algorithm may choose **B**. The hypothesis is that **the value of a decision cannot always be understood from the decision alone; it also depends on the structure it leaves behind.**

## From greedy optimization to future-aware optimization

The conceptual progression is:

```text
Immediate value
      ↓
Context
      ↓
Structural consequences
      ↓
Future opportunity
      ↓
Better solution
```

In simplified form: Decision Value=Immediate Value+Future Structural Value The second term is the central research challenge. How can future value be estimated from the current state of an evolving solution?

## The xAO family

xAO generalizes this principle by allowing different structural properties to influence the value of a decision.
- GAO - Geometry: How does the move affect the geometric trajectory?
- DAO - Density: How does it affect spatial distribution and coverage?
- PAO - Proportion: How does it affect relationships between scales and distances?
- SAO - Symmetry: Does it preserve useful structural balance?
- TAO - Topology: How does it affect connectivity and graph structure?
- RHO - Rhythm: How does it affect temporal or periodic structure?

The specific signal changes. The underlying question does not:

> **What does this decision enable next?**

### The xAO hypothesis

The framework can be expressed conceptually as: J(m∣St)=f(m∣St)+λΦ(m,St) where:

- St is the current state of the evolving solution,
- m is a candidate move,
- f represents immediate objective value,
- Φ represents structural or future-aware value,
- λ controls the influence of that additional information.

This provides a common language for different forms of future-aware decision making. The research question is not whether every structural signal improves every problem. It is:

> **Can the right representation of future structural value consistently improve constructive optimization?**

### Why TSP matters

TSP provides a particularly clear test because every decision affects the remaining search space. A locally optimal choice can:

- consume a useful connection,
- create an awkward remaining cluster,
- force a long closing edge,
- introduce geometric discontinuity,
- or leave a poor set of remaining options.

This creates a natural laboratory for testing whether **future-aware local decisions** can outperform purely greedy ones. The key comparison is therefore not simply:

> “Which algorithm finds the shortest tour?”

but also:

> **“Can we identify decisions where the locally cheaper choice produces a worse future, and can xAO detect that before the damage is done?”**

### The computational opportunity

There is an important potential advantage. Full look-ahead can become expensive. A simple greedy algorithm is computationally attractive precisely because it does not explore many possible futures. xAO explores the possibility of capturing **some of the information that deep look-ahead would provide through a compact representation of the current structural state.**

Conceptually:

```text
Greedy
  │
  │ fast, but myopic
  ▼
xAO
  │
  │ context-aware
  │ future-sensitive
  ▼
Deep look-ahead
  │
  │ potentially stronger,
  │ potentially more expensive
  ▼
Global optimization
```

The research opportunity is the middle ground:

> **Can we obtain some of the benefits of future awareness without paying the full computational cost of explicit search?**


## What we want to discover

The most important question is empirical:

> **Does future-aware decision making produce better solutions than conventional greedy decision making at comparable computational cost?**

For TSP, this means comparing approaches such as:

- nearest-neighbour / greedy construction,
- GAO,
- xAO variants,
- combinations with established local-search methods,
- and stronger benchmark algorithms.

But the deeper objective is understanding **why** a future-aware decision works. For example:

```text
Greedy:
A is cheaper than B
        ↓
Choose A
        ↓
Future options deteriorate


xAO:
B has greater downstream value
        ↓
Choose B
        ↓
Future options remain stronger
        ↓
Better complete solution
```

If this pattern can be demonstrated consistently, it provides evidence for the central xAO hypothesis.
