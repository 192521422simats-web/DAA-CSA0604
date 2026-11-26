"""
Assignment 2 - Q4: Brute-force closest pair of drones.
Unique pairs for n drones: n(n-1)/2  (pair (i,j) with i<j, so (j,i) is never repeated).
Run: python q4_closest_pair.py
"""
import math
import random
import time


def closest_pair_brute(points):
    best = float("inf"); pair = None
    pairs = dist_calcs = 0
    n = len(points)
    for i in range(n - 1):
        for j in range(i + 1, n):          # j > i avoids duplicate pairs
            pairs += 1
            dist_calcs += 1
            # squared distance: same ordering as real distance, avoids sqrt in the loop
            d = (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2
            if d < best:
                best = d; pair = (points[i], points[j])
    return math.sqrt(best), pair, pairs, dist_calcs


if __name__ == "__main__":
    random.seed(5)
    # small correctness check
    pts = [(0, 0), (10, 10), (3, 4), (3, 5), (20, 1)]
    d, p, pr, _ = closest_pair_brute(pts)
    print(f"Check: closest pair = {p}, distance = {d} (expected (3,4)-(3,5), 1.0)\n")

    LIMIT = 1.0   # acceptable response time in this experiment: 1 second
    print(f"Acceptable response time defined as <= {LIMIT} s")
    print(f"{'n':>6} {'pairs examined':>15} {'n(n-1)/2':>12} {'dist calcs':>11} {'time (s)':>9}")
    for n in (100, 500, 1000, 2000, 4000, 6000):
        pts = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
        t0 = time.perf_counter()
        _, _, pairs, dc = closest_pair_brute(pts)
        t = time.perf_counter() - t0
        flag = "  <-- exceeds limit" if t > LIMIT else ""
        print(f"{n:>6} {pairs:>15} {n * (n - 1) // 2:>12} {dc:>11} {t:>9.3f}{flag}")
    print("""
ANALYSIS: pairs examined equal n(n-1)/2 exactly, so doubling n multiplies work by ~4 (Theta(n^2)).
The inefficiency comes from comparing every drone with every other drone even though most pairs are far
apart and cannot be the closest. A redesign must avoid examining far-apart pairs, e.g. by sorting by x
and dividing the plane, or by using a grid, so each point is only compared with nearby points.""")
