"""
Assignment 3 - Q5: Divide-and-conquer closest pair vs brute force.
1. Sort points by x (once). 2. Split at the median x line into left/right halves.
3. Recursively find d_left and d_right, d = min(d_left, d_right).
4. Combine: keep points within distance d of the dividing line (the strip), sorted by y.
   Each strip point only needs comparing with the next <= 7 points in y-order, because at most a constant
   number of points (with mutual distance >= d) fit in a d x 2d box. So the strip step is O(n), not O(n^2).
T(n) = 2T(n/2) + O(n)  ->  O(n log n).
Run: python q5_closest_pair_dc.py
"""
import math
import random
import time

CALLS = {"dist": 0}


def dist(p, q):
    CALLS["dist"] += 1
    return math.hypot(p[0] - q[0], p[1] - q[1])


def brute(pts):
    best = float("inf"); pair = None
    for i in range(len(pts) - 1):
        for j in range(i + 1, len(pts)):
            d = dist(pts[i], pts[j])
            if d < best:
                best, pair = d, (pts[i], pts[j])
    return best, pair


def closest_rec(px):
    n = len(px)
    if n <= 3:
        return brute(px)
    mid = n // 2
    midx = px[mid][0]
    dl, pl = closest_rec(px[:mid])
    dr, pr = closest_rec(px[mid:])
    d, pair = (dl, pl) if dl <= dr else (dr, pr)
    strip = sorted((p for p in px if abs(p[0] - midx) < d), key=lambda p: p[1])
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):       # at most 7 neighbours
            if strip[j][1] - strip[i][1] >= d:
                break
            dd = dist(strip[i], strip[j])
            if dd < d:
                d, pair = dd, (strip[i], strip[j])
    return d, pair


def closest_dc(points):
    return closest_rec(sorted(points))


if __name__ == "__main__":
    random.seed(12)
    print("Correctness: D&C result must equal brute-force result on 200 random sets (including a pair straddling the divider)")
    for t in range(200):
        pts = list({(random.randint(0, 60), random.randint(0, 60)) for _ in range(random.randint(2, 40))})
        if len(pts) < 2:
            continue
        assert abs(closest_dc(pts)[0] - brute(pts)[0]) < 1e-9
    print("  all tests passed\n")
    print(f"{'n':>6} | {'brute dist calcs':>16} {'time(s)':>8} | {'D&C dist calcs':>14} {'time(s)':>8} | ratio")
    for n in (50, 100, 500, 1000, 2000, 4000, 8000):
        pts = list({(random.uniform(0, 10000), random.uniform(0, 10000)) for _ in range(n)})
        CALLS["dist"] = 0; t0 = time.perf_counter(); d1, _ = brute(pts); tb = time.perf_counter() - t0; cb = CALLS["dist"]
        CALLS["dist"] = 0; t0 = time.perf_counter(); d2, _ = closest_dc(pts); td = time.perf_counter() - t0; cd = CALLS["dist"]
        assert abs(d1 - d2) < 1e-9
        print(f"{n:>6} | {cb:>16} {tb:>8.3f} | {cd:>14} {td:>8.3f} | {cb / cd:>6.1f}x")
    print("""
D&C pays for sorting and strip building but its distance calculations grow ~ n log n instead of n^2/2, so
it becomes advantageous once n is in the low hundreds (see table). The strip step does not compare every
point with every other: only points within d of the dividing line matter, and in y-order only the next few
neighbours can be closer than d, giving linear work per level.""")
