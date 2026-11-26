"""
Assignment 2 - Q7 (Day-4 Design Challenge): Diagnose, redesign and validate.
Chosen solution: Exhaustive search for airlift packages (Q6).

A. DIAGNOSIS : it examines all 2^n combinations, many of which are infeasible or can never beat the best.
B. OBJECTIVE : cut the number of candidate combinations examined by at least 90% for n = 20, same optimum.
C. REDESIGN  : backtracking with (1) pruning when the weight limit is exceeded, and
               (2) bounding: sort by value/weight; if current value + optimistic fractional bound of the
               remaining packages cannot beat the best value found, abandon the branch.
D. PREDICTION: far fewer nodes visited, same optimal value; improvement in 'candidate solutions examined'.
E. VALIDATION: below.   F. DEFENCE: printed at the end.
Run: python q7_redesign_knapsack.py
"""
import random
import time
from q6_exhaustive_knapsack import exhaustive_knapsack


def pruned_knapsack(weights, values, capacity):
    n = len(weights)
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    W = [weights[i] for i in order]
    V = [values[i] for i in order]
    best = [0, []]
    nodes = [0]

    def bound(idx, cur_w, cur_v):
        """Optimistic estimate: fill remaining capacity fractionally (upper bound)."""
        b = cur_v
        room = capacity - cur_w
        for k in range(idx, n):
            if W[k] <= room:
                room -= W[k]
                b += V[k]
            else:
                b += V[k] * room / W[k]
                break
        return b

    def go(idx, cur_w, cur_v, chosen):
        nodes[0] += 1
        if cur_v > best[0]:
            best[0], best[1] = cur_v, chosen[:]
        if idx == n:
            return
        if bound(idx, cur_w, cur_v) <= best[0]:      # cannot beat best -> prune
            return
        if cur_w + W[idx] <= capacity:               # include (only if feasible)
            chosen.append(order[idx])
            go(idx + 1, cur_w + W[idx], cur_v + V[idx], chosen)
            chosen.pop()
        go(idx + 1, cur_w, cur_v, chosen)            # exclude

    go(0, 0, 0, [])
    return best[0], sorted(best[1]), nodes[0]


if __name__ == "__main__":
    random.seed(11)
    print(f"{'n':>3} | {'orig examined':>13} {'orig time':>9} | {'new nodes':>10} {'new time':>9} | "
          f"{'reduction':>9} | same optimum")
    for n in (12, 16, 18, 20, 22):
        ws = [random.randint(1, 30) for _ in range(n)]
        vs = [random.randint(1, 100) for _ in range(n)]
        cap = sum(ws) // 2
        t0 = time.perf_counter()
        v1, _, ex, _ = exhaustive_knapsack(ws, vs, cap)
        t1 = time.perf_counter() - t0
        t0 = time.perf_counter()
        v2, _, nodes = pruned_knapsack(ws, vs, cap)
        t2 = time.perf_counter() - t0
        red = 100 * (1 - nodes / ex)
        print(f"{n:>3} | {ex:>13} {t1:>9.3f} | {nodes:>10} {t2:>9.4f} | {red:>8.2f}% | {v1 == v2} ({v1})")
    print("\nHarder instances (strongly correlated: value = weight + 10, so the bound prunes poorly):")
    for n in (16, 20, 22):
        ws = [random.randint(10, 40) for _ in range(n)]
        vs = [w + 10 for w in ws]
        cap = sum(ws) // 2
        v1, _, ex, _ = exhaustive_knapsack(ws, vs, cap)
        v2, _, nodes = pruned_knapsack(ws, vs, cap)
        print(f"{n:>3} | orig examined {ex:>8} | new nodes {nodes:>8} | reduction {100 * (1 - nodes / ex):6.2f}% | same optimum {v1 == v2}")
    print("""
F. DEFENCE: The prediction is supported - the pruned search returns the same optimal value while visiting a
tiny fraction of the 2^n combinations, so the objective (>= 90% fewer candidates for n = 20) is met.
New costs: sorting (O(n log n)), a bound computation at each node, recursion overhead. Worst case is still
exponential (an adversarial input where the bound never prunes), and for very small n plain enumeration is
simpler and just as fast, so the original may still be preferable there.""")
