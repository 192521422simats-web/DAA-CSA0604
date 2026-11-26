"""
Assignment 5 Part B - B4: Bin packing (workloads -> servers) with First Fit Decreasing (FFD).
Placement rule: sort workloads by demand in decreasing order; put each workload into the FIRST server that
still has enough remaining capacity; if none, open a new server.
Run: python b4_bin_packing.py
"""
import random
import time


def first_fit_decreasing(items, cap):
    servers = []                      # each server: [remaining_capacity, [workloads]]
    for x in sorted(items, reverse=True):
        for s in servers:
            if s[0] >= x:
                s[0] -= x; s[1].append(x)
                break
        else:
            servers.append([cap - x, [x]])
    return servers


def exact_bins(items, cap):
    """Exact optimum by backtracking (small inputs only)."""
    items = sorted(items, reverse=True); n = len(items)
    for k in range(-(-sum(items) // cap), n + 1):
        loads = [0] * k

        def go(i):
            if i == n:
                return True
            seen = set()
            for b in range(k):
                if loads[b] + items[i] <= cap and loads[b] not in seen:
                    seen.add(loads[b]); loads[b] += items[i]
                    if go(i + 1):
                        return True
                    loads[b] -= items[i]
            return False
        if go(0):
            return k


def show(servers):
    print(f"  Servers used: {len(servers)}")
    for i, (rem, w) in enumerate(servers, 1):
        print(f"   Server {i}: workloads {w}  used {sum(w)}  remaining capacity {rem}")


if __name__ == "__main__":
    print("=== B4.1 Practical strategy: First Fit Decreasing ===")
    cap = 100
    work = [42, 69, 29, 31, 56, 12, 8, 77, 20, 55, 33, 18, 40, 25, 9]
    srv = first_fit_decreasing(work, cap)
    print(f"Capacity {cap}, workloads {work}")
    show(srv)
    assert all(s[0] >= 0 for s in srv) and sorted(sum((s[1] for s in srv), [])) == sorted(work)
    print(f"  Lower bound (total demand / capacity, rounded up) = {-(-sum(work) // cap)}")

    print("\n=== B4.2 Challenge the strategy (input where FFD is NOT optimal) ===")
    cap2 = 18
    bad = [15, 10, 10, 8, 7, 6, 5, 4, 4]
    srv2 = first_fit_decreasing(bad, cap2)
    print(f"Capacity {cap2}, workloads {bad}")
    show(srv2)
    print(f"  Exact optimum (small exhaustive check) = {exact_bins(bad, cap2)} servers  <- FFD used one more.")
    print("  Optimal packing: {15}, {10,8}, {10,4,4}, {7,6,5} - three bins filled exactly to 18 plus {15} (total waste 3).")
    print("  Reason FFD fails: it puts the second 10 with 7 (the first bin where it fits, 17/18) and later has to open a")
    print("  5th bin for the leftover 4. The optimum needs 10 paired with 4+4 and 7 paired with 6+5; greedy commitments")
    print("  made early cannot be undone.")
    print("\n=== Scale check: thousands of workloads ===")
    random.seed(1)
    print(f"{'workloads':>10} {'servers (FFD)':>14} {'lower bound':>12} {'time (s)':>9}")
    for n in (1000, 3000, 6000):
        items = [random.randint(1, 60) for _ in range(n)]
        t0 = time.perf_counter()
        s = first_fit_decreasing(items, 100)
        t = time.perf_counter() - t0
        print(f"{n:>10} {len(s):>14} {-(-sum(items) // 100):>12} {t:>9.3f}")

    print("""
=== B4.3 Algorithm Engineering Decision Note ===
Why exhaustive search is unattractive: assigning n workloads to servers has up to n^n (Bell-number scale) arrangements;
even the pruned exact search above becomes impractical beyond a few dozen workloads, while production receives thousands.
Guarantee of FFD: never worse than (11/9)*OPT + 6/9 servers - a proven bound, not optimality (see B4.2 counterexample).
Computational advantage: sorting O(n log n) plus a scan for the first fit (O(n * servers) here; O(n log n) with a
tree structure); the scale table shows thousands of workloads placed in well under a second, and in practice the
servers used are within ~1 of the theoretical lower bound.
When an exact approach is appropriate: small batches, or when each server is very expensive (e.g. dedicated
hardware or licences) and a one-off planning job can run for minutes or hours; also to benchmark the heuristic offline.
Evidence to monitor before deployment: servers used vs the lower bound ceil(sum/capacity), utilisation per server,
placement latency at peak load, behaviour on adversarial/skewed demand distributions, and how often rebalancing is needed.""")
