"""
Assignment 2 - Q6: Exhaustive search for humanitarian airlift (0/1 selection of packages).
Every combination is a bitmask from 0 to 2^n - 1 (bit i = package i is loaded).
Run: python q6_exhaustive_knapsack.py
"""
import random
import time


def exhaustive_knapsack(weights, values, capacity):
    n = len(weights)
    best_val, best_mask, examined, feasible = 0, 0, 0, 0
    for mask in range(1 << n):
        examined += 1
        w = v = 0
        for i in range(n):
            if mask >> i & 1:
                w += weights[i]
                v += values[i]
        if w <= capacity:                 # feasibility check
            feasible += 1
            if v > best_val:              # evaluation + keep best
                best_val, best_mask = v, mask
    chosen = [i for i in range(n) if best_mask >> i & 1]
    return best_val, chosen, examined, feasible


if __name__ == "__main__":
    # Small verifiable instance: capacity 10.
    # Combos by hand: {A,B}=w9 v70 ; {B,C}=w10 v80 (best) ; {A,C}=w11 infeasible ; {D}=w10 v60 ...
    w = [4, 5, 5, 10]
    v = [30, 40, 40, 60]
    best, chosen, ex, fe = exhaustive_knapsack(w, v, 10)
    print(f"Verification instance: best value = {best} (expected 80), packages = {chosen} (expected [1, 2])")
    print(f"  combinations examined = {ex} (2^4 = 16), feasible = {fe}\n")

    random.seed(7)
    LIMIT = 2.0
    print(f"Growth investigation (acceptable response time = {LIMIT} s)")
    print(f"{'n':>4} {'predicted 2^n':>14} {'examined':>10} {'time (s)':>9}")
    for n in (10, 14, 16, 18, 20, 22):
        ws = [random.randint(1, 30) for _ in range(n)]
        vs = [random.randint(1, 100) for _ in range(n)]
        cap = sum(ws) // 2
        t0 = time.perf_counter()
        _, _, ex, _ = exhaustive_knapsack(ws, vs, cap)
        t = time.perf_counter() - t0
        flag = "  <-- exceeds limit" if t > LIMIT else ""
        print(f"{n:>4} {2 ** n:>14} {ex:>10} {t:>9.3f}{flag}")
        if t > 15:
            break
    print("""
EXPLANATION: each extra package doubles the number of combinations (2^(n+1) = 2*2^n), so adding 10
packages multiplies the work by about 1000. Work is exponential in n because every package is either
in or out, and all combinations are examined.
DEPLOYMENT BOUNDARY: choose the largest n whose time is below the response-time limit above
(see table; in this Python prototype that is around n = 20). Beyond that, use a smarter method.""")
