# Fibonacci Heap – Python Implementation

This project implements a **Fibonacci Heap (priority queue)** in Python for efficient priority queue operations.  
*(Note: this is the **data structure**, not the Fibonacci number sequence.)*

📍 Developed as part of the **Analysis and Algorithms** class at **University of the Fraser Valley (UFV)**.  

---

## 📂 Documentation
- [`docs/analysis.md`](./docs/analysis.md) → Complexity analysis, design trade-offs  
- [`docs/decision.md`](./docs/decision.md) → Design decisions, algorithmic choices  

---

## 👩‍💻 Our team
- **Meriem** — insert, minimum, merge + tests + demo; decrease_key, _cut, _cascading_cut, delete (+ tests)  
- **Barend** — extract_min + consolidate, heap_link (+ tests)  

---
### Install dependencies
pip install pytest
pip install networkx matplotlib


### how to run 
python -m scripts.demo_game
  
## Bonus: Live Visualization
We added an optional live visualization using `matplotlib` + `networkx`.

## References 

GeeksforGeeks. (2023, July 15). *Fibonacci Heap – Insert, Union and Minimum operations*. GeeksforGeeks. https://www.geeksforgeeks.org/fibonacci-heap-insert-union-and-minimum-operations/

Fredman, M. L., & Tarjan, R. E. (1987). Fibonacci heaps and their uses in improved network optimization algorithms. *Journal of the ACM, 34*(3), 596–615. https://doi.org/10.1145/28869.28874

MIT OpenCourseWare. (2018, June 20). *Fibonacci Heaps or How to invent an extremely clever data structure* [Video]. YouTube. https://www.youtube.com/watch?v=6JxvKfSV9Ns

OpenAI. (2025). ChatGPT (September 2025 version) [Large language model]. https://chat.openai.com
We used ChatGPT (OpenAI, 2025) to draft explanations, generate code scaffolding, and clarify analysis steps.
