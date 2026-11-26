# Assignment 4 Part II - Implement, Test, Debug and Optimise
| File | Task |
|---|---|
| `task1_word_wrap.py` | Task 1 Word wrap DP: lines, unused spaces, penalties, DP states, 3 widths, boundary tests |
| `task2_greedy_vs_dp.py` | Task 2 Fractional greedy vs 0/1 DP knapsack, counterexample, work/memory comparison |
| `task3_routing.py` | Task 3 Dijkstra, negative edge, Bellman-Ford, negative-cycle detection, Floyd, Warshall |
| `task4_assembly_line.py` | Task 4 Assembly-line DP with trace, route, prediction and disruption experiments |
| `task5_mst.py` | Task 5 Kruskal, Prim and Boruvka traces, tie / multiple-MST experiment |
| `task6_tsp_dp.py` | Task 6 TSP Held-Karp DP, validation against brute force, state-space growth |
The word-wrap penalty formula was missing in the document text; `PENALTY_POWER = 2` (penalty = unused^2) is at the top of
`task1_word_wrap.py` - change it if your question paper uses a different formula.
Sample outputs: `task*_output.txt`.
