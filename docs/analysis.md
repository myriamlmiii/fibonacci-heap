# Analysis (Amortized) 
Potential: Phi(H) = (# of trees in root list) + 2*(# of marked nodes).
Target amortized costs: insert/merge/min/decrease_key = O(1); extract_min/delete = O(log n).


# Fibonacci Heap — Analysis Framework (Amortized)

This document applies the standard amortized analysis for Fibonacci Heaps using a potential function.  
We follow the textbook (CLRS) and the Fredman–Tarjan paper ideas.

---

**Amortized complexities:**
- `insert`, `minimum`, `merge`, `decrease_key` → O(1)
- `extract_min`, `delete` → O(log n)

**Sketch:**  
- `insert` adds a 1-node tree, increasing \(T\) by 1 (constant actual + potential change).  
- `merge` concatenates two root lists with O(1) pointer splicing; \(T\) adds, no linking yet.  
- `decrease_key` cuts nodes that violate the heap order; marking ensures at most one unmarked violation per parent, so the potential drop pays for cascading cuts.  
- `extract_min` moves min’s children to root list and consolidates by tree degree; degrees are bounded by O(log n) due to Fibonacci growth of subtree sizes, hence O(log n) links.


## Model & Notation
- A heap is a set of **root trees** (each is a heap-ordered tree).
- Each **node** stores a `mark` bit. A **marked** node has lost a child since it became a child of its current parent.
- Let:
  - `T(H)` = number of trees (roots) in the root list
  - `M(H)` = number of marked nodes

### Potential Function
We use the standard potential:
\[
\Phi(H) \;=\; T(H) \;+\; 2\,M(H).
\]

Intuition:
- Adding a root increases potential by 1 (we “bank” credit to pay for future work).
- Marks track whether a second child loss triggers cascading cuts; unmarking during cuts releases potential to pay for them.

---

## Amortized Costs (Results)

| Operation        | Amortized Time |
|------------------|----------------|
| `insert`         | O(1)           |
| `minimum`        | O(1)           |
| `merge` (meld)   | O(1)           |
| `decrease_key`   | O(1)           |
| `extract_min`    | O(log n)       |
| `delete`         | O(log n)       |

---

## Sketches of the Analysis

### `insert(key)` — **O(1)**
- Actual: splice a 1-node tree into the root list; update `min` → O(1).
- Potential: `T` increases by 1 (ΔΦ = +1).
- Amortized = Actual + ΔΦ = O(1).

### `minimum()` — **O(1)**
- Actual: return `min.key` → O(1).
- Potential unchanged → amortized O(1).

### `merge(other)` (meld) — **O(1)**
- Actual: concatenate two circular root lists; update `min` → O(1).
- Potential: `T` becomes `T(H1)+T(H2)`; no linking yet → ΔΦ = O(1).
- Amortized O(1).

### `decrease_key(x, new_key)` — **O(1)**
- If heap order is violated, **cut** `x` to the root list (O(1)); if parent was unmarked, mark it; if already marked, cascade (cut parent, and so on).
- Each **cascading cut** removes a mark (potential −2) and adds a new root (potential +1), net ΔΦ ≤ −1 per cascaded step.
- This released potential pays for the O(1) per cut, yielding amortized O(1).

### `extract_min()` — **O(log n)**
1. Remove the min root; add all its children to the root list (pointer fixes are O(degree(min))).
2. **Consolidate**: repeatedly link roots of the same degree so at most one tree of each degree remains.
- The number of distinct degrees that can appear is O(log n) (see **Degree Bound** below).
- Thus at most O(log n) links; amortized O(log n).

### `delete(x)` — **O(log n)**
- Standard trick: `decrease_key(x, -∞)`, then `extract_min()`.
- Amortized = O(1) + O(log n) = O(log n).

---

## Degree Bound (Why O(log n))
Let `D(n)` be the maximum degree of any node in an `n`-node Fibonacci Heap.
- When a node attains degree `k`, it has acquired children over time; due to marking and cuts, each child it keeps has size at least the size of the **(k−2)**-th Fibonacci number.
- Therefore, the size of a tree of degree `k` is at least `F_{k+2}` (grows exponentially in `k`).
- Hence `k = O(log n)`, and the consolidation’s number of possible degrees is `O(log n)`.

---

## What Each Teammate’s Part Contributes to the Analysis
- **Meriem**: `insert`, `minimum`, `merge` → O(1) operations that manipulate the root list and maintain `min`.
- **Barend**: `extract_min` + **consolidation** → where the O(log n) work occurs; uses the degree bound above.
- **Harishman**: `decrease_key`, `_cut`, `_cascading_cut`, `delete` → O(1) amortized for `decrease_key` (via marks + potential), O(log n) for `delete`.

---

## Takeaways
- Fibonacci Heaps achieve **constant amortized time** for `insert`, `merge`, `minimum`, and `decrease_key`, which is why they’re attractive for algorithms like **Dijkstra** (when many decrease-key operations occur).
- The logarithmic work is isolated in `extract_min` (and `delete`), controlled via consolidation and the **O(log n)** degree bound.

