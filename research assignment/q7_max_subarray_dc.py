"""
Assignment 3 - Q7 (Day-4): Design D&C from first principles.  Problem chosen: Maximum Subarray Sum
(best contiguous profit/loss window in a daily sales series).

STAGE 1 (independent proposals - kept as required)
 Student A: split in half; answer = max(best in left, best in right); base case n=1.  (Missing: window that
            crosses the middle - this would be a wrong design.)
 Student B: split in half; answer = max(left, right, best crossing the midpoint); base case n=1;
            each call returns only the best sum.  (Missing: nothing wrong, but returns only one value and the
            crossing step re-scans.)
STAGE 2 comparison: both agree on halving and base case; they differ in the combine step - Student B's
            crossing case is essential. Retain B's idea.
STAGE 3 final design: Decomposition = left/right halves. Base case = single element. Each call returns
            (total, best prefix, best suffix, best subarray). Combine:
              total  = L.total + R.total
              prefix = max(L.prefix, L.total + R.prefix)
              suffix = max(R.suffix, R.total + L.suffix)
              best   = max(L.best, R.best, L.suffix + R.prefix)
STAGE 4 recurrence: T(n) = 2T(n/2) + O(1) -> Theta(n)  (the combine is constant time because each call
            returns the 4 summary values). If the crossing step re-scans (Student B's version), T(n)=2T(n/2)+Theta(n)
            = Theta(n log n). Baseline brute force is Theta(n^2).
Run: python q7_max_subarray_dc.py
"""
import random
import sys
import time

sys.setrecursionlimit(100000)
OPS = {"n": 0}


def brute(a):
    best = a[0]; ops = 0
    for i in range(len(a)):
        s = 0
        for j in range(i, len(a)):
            s += a[j]; ops += 1
            best = max(best, s)
    OPS["n"] = ops
    return best


def dc(a, lo, hi):
    """returns (total, prefix, suffix, best)"""
    OPS["n"] += 1
    if lo == hi:
        x = a[lo]
        return x, x, x, x
    mid = (lo + hi) // 2
    L = dc(a, lo, mid)
    R = dc(a, mid + 1, hi)
    total = L[0] + R[0]
    prefix = max(L[1], L[0] + R[1])
    suffix = max(R[2], R[0] + L[2])
    best = max(L[3], R[3], L[2] + R[1])
    return total, prefix, suffix, best


if __name__ == "__main__":
    random.seed(33)
    tests = [[-2, 1, -3, 4, -1, 2, 1, -5, 4], [-5, -2, -9], [7], [1, 2, 3], [-1, 5, -1, 5, -1]]
    print("Correctness tests (D&C vs brute force):")
    for t in tests:
        b = brute(t); d = dc(t, 0, len(t) - 1)[3]
        print(f"  {t} -> brute {b}, D&C {d}, {'PASS' if b == d else 'FAIL'}")
    for _ in range(500):
        t = [random.randint(-50, 50) for _ in range(random.randint(1, 30))]
        assert brute(t) == dc(t, 0, len(t) - 1)[3]
    print("  500 random tests passed\n")
    print(f"{'n':>7} | {'brute ops':>12} {'time(s)':>8} | {'D&C calls':>10} {'time(s)':>8}")
    for n in (100, 1000, 4000, 8000, 64000):
        a = [random.randint(-100, 100) for _ in range(n)]
        t0 = time.perf_counter(); b = brute(a) if n <= 8000 else None; tb = time.perf_counter() - t0
        bops = OPS["n"] if n <= 8000 else n * (n + 1) // 2
        OPS["n"] = 0
        t0 = time.perf_counter(); d = dc(a, 0, n - 1)[3]; td = time.perf_counter() - t0
        if b is not None:
            assert b == d
        print(f"{n:>7} | {bops:>12}{'' if n <= 8000 else '*'} {tb if n <= 8000 else float('nan'):>8.3f} | {OPS['n']:>10} {td:>8.4f}")
    print("(* = n(n+1)/2 computed, brute force not run)")
    print("""
Why D&C suits it: the answer for a range can be built from small summaries of its two halves.
Work reduced: re-adding overlapping windows (O(n^2) -> O(n)). Extra cost: recursion calls and O(log n) stack.
Not appropriate when subproblems overlap heavily or the combine step costs as much as solving from scratch.
Look for: a way to split into independent subproblems of similar size, a cheap combine, and a simple base case.""")
