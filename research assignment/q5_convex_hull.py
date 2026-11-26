"""
Assignment 2 - Q5: Brute-force convex hull.
Geometric rule: segment (Pi,Pj) is a hull edge if ALL other points lie on the same side of the line
through Pi and Pj. Side of point P relative to the line is the sign of the cross product
    cross = (xj-xi)*(yP-yi) - (yj-yi)*(xP-xi)
(>0 left, <0 right, 0 collinear). Collinear points are accepted only if they lie within the segment,
otherwise the segment is not the extreme edge.
Run: python q5_convex_hull.py   (saves hull_test1.png, hull_test2.png if matplotlib is installed)
"""
import math
import random


def cross(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def between(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def brute_force_hull(points):
    pts = list(dict.fromkeys(points))            # remove duplicate points
    n = len(pts)
    edges = []
    tests = 0
    for i in range(n):
        for j in range(i + 1, n):
            pos = neg = 0
            ok = True
            for k in range(n):
                if k == i or k == j:
                    continue
                tests += 1
                c = cross(pts[i], pts[j], pts[k])
                if c > 0:
                    pos += 1
                elif c < 0:
                    neg += 1
                elif not between(pts[i], pts[j], pts[k]):   # collinear but outside the segment
                    ok = False
                    break
                if pos and neg:
                    ok = False
                    break
            if ok:
                edges.append((pts[i], pts[j]))
    return edges, tests


def order_hull(edges):
    """Chain the accepted edges into a polygon (list of vertices)."""
    if not edges:
        return []
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = min(adj)
    poly = [start]
    prev, cur = None, start
    while True:
        nxt = [v for v in adj[cur] if v != prev]
        if not nxt:
            break
        nxt = nxt[0]
        if nxt == start:
            break
        poly.append(nxt)
        prev, cur = cur, nxt
    return poly


def plot(points, hull, name):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    plt.figure(figsize=(5, 5))
    plt.scatter(*zip(*points), c="blue", s=15)
    h = hull + [hull[0]]
    plt.plot(*zip(*h), "r-")
    plt.title(name)
    plt.savefig(name + ".png", dpi=100)
    plt.close()


if __name__ == "__main__":
    # Test 1: boundary + interior points
    t1 = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5), (3, 4), (7, 2), (6, 8), (2, 7)]
    edges, tests = brute_force_hull(t1)
    hull = order_hull(edges)
    print("Test 1 (square + interior points)")
    print("  hull vertices:", hull, " side-tests:", tests)
    plot(t1, hull, "hull_test1")

    # Test 2 (designed to challenge): collinear points on the boundary, duplicates, a point inside
    t2 = [(0, 0), (5, 0), (10, 0), (10, 5), (10, 10), (5, 10), (0, 10), (0, 5), (5, 5), (5, 5), (2, 2)]
    edges, tests = brute_force_hull(t2)
    hull = order_hull(edges)
    print("Test 2 (collinear boundary points, duplicate point, interior points)")
    print("  hull vertices:", hull, " side-tests:", tests)
    plot(t2, hull, "hull_test2")

    print("\nGrowth of work: number of orientation tests vs n  (expected ~ n^2 pairs x n points = n^3)")
    random.seed(2)
    print(f"{'n':>5} {'orientation tests':>18} {'n^3':>12}")
    for n in (10, 20, 40, 80):
        pts = [(random.randint(0, 500), random.randint(0, 500)) for _ in range(n)]
        _, tests = brute_force_hull(pts)
        print(f"{n:>5} {tests:>18} {n ** 3:>12}")
    print("""
CORRECTNESS ARGUMENT: the hull is the smallest convex polygon containing all points. If every other point
lies on one side of line PiPj, then the line is a supporting line of the point set that touches it at Pi and
Pj, so the segment lies on the boundary of the convex hull. If points were on both sides, some point would
lie beyond the segment, so the segment would cut through the interior and cannot be a hull edge.""")
