r"""
Assignment 4B - Task 6: Travelling Salesperson with Dynamic Programming (Held-Karp).
Model: Input = cost matrix between hub (0) and delivery locations; Output = cheapest tour hub -> all -> hub.
State: DP[S][j] = minimum cost of a path that starts at the hub, visits exactly the set S of locations (bitmask)
       and ends at location j (j in S).   The current location alone is not enough: two partial routes at j with
       different visited sets have different futures, so S must be remembered.
Base:  DP[{j}][j] = cost(hub, j).
Recurrence: DP[S][j] = min over k in S\{j} of DP[S\{j}][k] + cost(k, j)
Answer: min over j of DP[all][j] + cost(j, hub).
Run: python task6_tsp_dp.py
"""
import itertools
import random
import time
import tracemalloc

INF = float("inf")


def tsp_dp(cost):
    n = len(cost) - 1                        # delivery locations are 1..n, hub is 0
    full = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    states = 0
    for j in range(n):
        dp[1 << j][j] = cost[0][j + 1]
        states += 1
    for S in range(1, full + 1):
        for j in range(n):
            if not S >> j & 1 or S == 1 << j:
                continue
            prev = S ^ (1 << j)
            for k in range(n):
                if prev >> k & 1 and dp[prev][k] + cost[k + 1][j + 1] < dp[S][j]:
                    dp[S][j] = dp[prev][k] + cost[k + 1][j + 1]
                    parent[S][j] = k
            states += 1
    best, last = INF, -1
    for j in range(n):
        if dp[full][j] + cost[j + 1][0] < best:
            best, last = dp[full][j] + cost[j + 1][0], j
    route, S, j = [], full, last
    while j != -1:                           # reconstruct
        route.append(j + 1)
        pj = parent[S][j]
        S ^= 1 << j
        j = pj
    route.reverse()
    return best, route, states


def tsp_bruteforce(cost):
    n = len(cost) - 1
    best, br = INF, None
    for perm in itertools.permutations(range(1, n + 1)):
        c = cost[0][perm[0]] + sum(cost[perm[i]][perm[i + 1]] for i in range(n - 1)) + cost[perm[-1]][0]
        if c < best:
            best, br = c, perm
    return best, list(br)


def random_cost(n, seed):
    rnd = random.Random(seed)
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            m[i][j] = m[j][i] = rnd.randint(5, 60)
    return m


if __name__ == "__main__":
    names = ["Hub", "A", "B", "C", "D", "E", "F"]
    cost = [[0, 12, 29, 22, 13, 24, 18],
            [12, 0, 19, 3, 25, 6, 14],
            [29, 19, 0, 21, 23, 28, 9],
            [22, 3, 21, 0, 4, 16, 17],
            [13, 25, 23, 4, 0, 15, 7],
            [24, 6, 28, 16, 15, 0, 11],
            [18, 14, 9, 17, 7, 11, 0]]
    print("6.3 - Hub + 6 delivery locations. Cost matrix:")
    print("      " + " ".join(f"{n:>4}" for n in names))
    for i, row in enumerate(cost):
        print(f"  {names[i]:>3} " + " ".join(f"{x:>4}" for x in row))
    best, route, st = tsp_dp(cost)
    print("\nOptimal route:", " -> ".join(["Hub"] + [names[i] for i in route] + ["Hub"]))
    print(f"Minimum Travel Cost = {best}   (DP states evaluated: {st})")

    print("\n6.4 - Validation: hub + 4 locations, DP vs exhaustive enumeration of all 4! = 24 tours")
    small = [row[:5] for row in cost[:5]]
    b1, r1, _ = tsp_dp(small)
    b2, r2 = tsp_bruteforce(small)
    print(f"  DP cost = {b1} (route {r1}), exhaustive cost = {b2} (route {r2}), match = {b1 == b2}")
    for seed in range(20):
        c = random_cost(6, seed)
        assert tsp_dp(c)[0] == tsp_bruteforce(c)[0]
    print("  20 extra random 6-location instances also match. An independent method agreeing on many inputs makes")
    print("  an indexing/recurrence defect in the DP very unlikely.")

    print("\n6.5 - State-space growth")
    print(f"{'locations':>9} {'DP states':>11} {'n*2^n':>10} {'table cells':>12} {'time (s)':>9} {'peak mem (KB)':>14}")
    for n in range(4, 15):
        c = random_cost(n, 100 + n)
        tracemalloc.start()
        t0 = time.perf_counter()
        _, _, st = tsp_dp(c)
        t = time.perf_counter() - t0
        peak = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
        print(f"{n:>9} {st:>11} {n * 2 ** n:>10} {(1 << n) * n:>12} {t:>9.3f} {peak:>14.0f}")
    print("""
Inquiry: DP stores each (subset, last city) answer once instead of recomputing all n! orderings, reducing work
from O(n!) to O(n^2 * 2^n). But the number of subsets is 2^n, so states, time AND memory still double with every
extra location - still exponential.

6.6 - 200 locations: 2^200 subsets (~1.6e60) cannot be stored or computed; the requirement has changed from
'guaranteed optimal' to 'excellent within seconds'. I would investigate heuristics/approximation: nearest-neighbour
construction improved by 2-opt / Or-opt local search, or Christofides-style approximation. Trade-off accepted: no
guarantee of the minimum cost (route may be a few percent longer) in exchange for polynomial running time.

6.7 - Reflection (<=150 words): DP removes repeated work, not the exponential number of distinct subproblems.
My table shows states = n*2^n: 10 -> 14 locations multiplied states by ~20 and memory grew the same way. DP is
only scalable when the number of distinct states is polynomial (e.g. knapsack with small W, assembly lines);
for TSP the state includes a subset of locations, so the state space itself is exponential.""")
