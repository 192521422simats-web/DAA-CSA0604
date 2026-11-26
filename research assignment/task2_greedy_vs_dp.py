"""
Assignment 4B - Task 2: Fractional Knapsack (Greedy) vs 0/1 Knapsack (Dynamic Programming).
Run: python task2_greedy_vs_dp.py
"""


def fractional_greedy(items, cap, show=True):
    """items: list of (id, weight, value). Take by highest value/weight, last item may be fractional."""
    order = sorted(items, key=lambda it: it[2] / it[1], reverse=True)
    total, room, chosen, ops = 0.0, cap, [], len(items)       # ops: sort comparisons approx n log n, plus scan
    for iid, w, v in order:
        ops += 1
        if room <= 0:
            break
        if w <= room:
            chosen.append((iid, 1.0)); total += v; room -= w
            if show: print(f"  take whole {iid} (ratio {v / w:.2f}) -> value {total:.2f}, room {room}")
        else:
            frac = room / w
            chosen.append((iid, round(frac, 3))); total += v * frac
            if show: print(f"  take {frac:.3f} of {iid} (ratio {v / w:.2f}) -> value {total:.2f}, room 0")
            room = 0
    return total, chosen, ops


def greedy_01(items, cap, show=True):
    """Same ratio intuition but items cannot be split: skip an item that does not fit."""
    order = sorted(items, key=lambda it: it[2] / it[1], reverse=True)
    total, room, chosen = 0, cap, []
    for iid, w, v in order:
        if w <= room:
            chosen.append(iid); total += v; room -= w
            if show: print(f"  commit {iid} (w={w}, v={v}, ratio {v / w:.2f}) -> value {total}, room {room}")
        elif show:
            print(f"  skip {iid} (w={w} does not fit in room {room})")
    return total, chosen


def dp_01(items, cap):
    n = len(items)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    ops = 0
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        for c in range(cap + 1):
            ops += 1
            dp[i][c] = dp[i - 1][c]
            if w <= c and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v
    chosen, c = [], cap
    for i in range(n, 0, -1):                     # reconstruct selected items
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(items[i - 1][0]); c -= items[i - 1][1]
    return dp[n][cap], chosen[::-1], ops, (n + 1) * (cap + 1)


if __name__ == "__main__":
    print("2.1 NORMAL CASE - classic instance, capacity 50 (fractional knapsack: greedy is optimal)")
    items = [("A", 10, 60), ("B", 20, 100), ("C", 30, 120)]
    v, ch, ops = fractional_greedy(items, 50)
    print(f"Solution A (fractional greedy): value = {v:.2f}, selected = {ch}")
    v2, ch2, ops2, cells = dp_01(items, 50)
    print(f"Solution B (0/1 DP)           : value = {v2}, selected items = {ch2}   (0/1 cannot split, so it is lower)\n")

    print("2.2 BREAK THE GREEDY INTUITION (0/1 problem), capacity 10")
    bad = [("X", 1, 2), ("Y", 10, 15)]
    print("Ratio greedy applied to 0/1:")
    gv, gch = greedy_01(bad, 10)
    dv, dch, _, _ = dp_01(bad, 10)
    print(f"  greedy value = {gv}, items = {gch}")
    print(f"  DP optimum   = {dv}, items = {dch}")
    print("  First greedy commitment preventing the optimum: taking X (ratio 2.0) first leaves room 9, so Y (w=10) can")
    print("  never fit; the best choice was Y alone (15 > 2).")
    bad2 = [("P", 5, 30), ("Q", 4, 24), ("R", 6, 31), ("S", 3, 16)]
    print("\nSecond counterexample, capacity 10:")
    gv, gch = greedy_01(bad2, 10)
    dv, dch, _, _ = dp_01(bad2, 10)
    print(f"  greedy value = {gv} items {gch};  DP optimum = {dv} items {dch}")

    print("\n2.3 ENGINEERING COMPARISON (work, memory, quality, guarantee)")
    import random
    random.seed(5)
    print(f"{'n':>5} {'cap':>7} | {'greedy ops':>10} {'greedy value':>12} | {'DP ops':>10} {'DP cells':>10} {'DP value':>9} | gap")
    for n, cap in ((10, 100), (100, 1000), (500, 5000), (1000, 20000)):
        its = [(f"I{i}", random.randint(1, 60), random.randint(1, 200)) for i in range(n)]
        _, _, gops = fractional_greedy(its, cap, show=False)
        gval01, _ = greedy_01(its, cap, show=False)
        dval, _, dops, cells = dp_01(its, cap)
        print(f"{n:>5} {cap:>7} | {gops:>10} {gval01:>12} | {dops:>10} {cells:>10} {dval:>9} | {100 * (dval - gval01) / dval:5.2f}%")
    print("""
Greedy: ~n log n work, O(n) memory, optimal ONLY for the fractional version; for 0/1 it carries no guarantee.
DP: O(nW) work and O(nW) memory (table cells), always optimal for 0/1, but cost grows with capacity W.

2.4 CHANGED REQUIREMENT ("return extremely quickly; near-optimal acceptable")
The table shows that the 0/1 ratio-greedy answer is within a small percentage of the DP optimum on random
data while using orders of magnitude less work and memory, so I would choose the greedy strategy (optionally
improved by also comparing with the best single item). I would keep DP when the loss in value on adversarial
instances like the counterexample above is unacceptable and W is small enough for the table to fit.""")
