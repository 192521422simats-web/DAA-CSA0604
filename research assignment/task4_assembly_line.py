"""
Assignment 4B - Task 4: Assembly-line scheduling with Dynamic Programming.
f1[j] = fastest time to finish station j on line 1, f2[j] likewise for line 2.
    f1[0] = e1 + a1[0]          f2[0] = e2 + a2[0]
    f1[j] = min(f1[j-1] + a1[j],  f2[j-1] + t2[j-1] + a1[j])      (stay / transfer from line 2)
    f2[j] = min(f2[j-1] + a2[j],  f1[j-1] + t1[j-1] + a2[j])      (stay / transfer from line 1)
    answer = min(f1[n-1] + x1, f2[n-1] + x2)
t1[j] = time to transfer from line 1 (after station j) to line 2; t2[j] the reverse.
Run: python task4_assembly_line.py
"""


def assembly(a1, a2, t1, t2, e1, e2, x1, x2, trace=True):
    n = len(a1)
    f1, f2 = [0] * n, [0] * n
    from1, from2 = [0] * n, [0] * n           # which line the product came from before this station
    f1[0], f2[0] = e1 + a1[0], e2 + a2[0]
    from1[0], from2[0] = 1, 2
    rows = []
    for j in range(1, n):
        s1, c1 = f1[j - 1] + a1[j], f2[j - 1] + t2[j - 1] + a1[j]
        s2, c2 = f2[j - 1] + a2[j], f1[j - 1] + t1[j - 1] + a2[j]
        f1[j], from1[j] = (s1, 1) if s1 <= c1 else (c1, 2)
        f2[j], from2[j] = (s2, 2) if s2 <= c2 else (c2, 1)
        rows.append((j + 1, s1, c1, "Stay" if s1 <= c1 else "Transfer", s2, c2, "Stay" if s2 <= c2 else "Transfer"))
    end1, end2 = f1[-1] + x1, f2[-1] + x2
    best, last = (end1, 1) if end1 <= end2 else (end2, 2)
    route, line = [], last
    for j in range(n - 1, -1, -1):             # reconstruct
        route.append((line, j + 1))
        line = from1[j] if line == 1 else from2[j]
    route.reverse()
    if trace:
        print(f"{'Station':>7} | {'L1 stay':>8} {'L1 transfer':>12} {'Selected':>9} | {'L2 stay':>8} {'L2 transfer':>12} {'Selected':>9}")
        print(f"{1:>7} | {'-':>8} {'-':>12} {'(entry)':>9} | {'-':>8} {'-':>12} {'(entry)':>9}   f1={f1[0]}, f2={f2[0]}")
        for r in rows:
            print(f"{r[0]:>7} | {r[1]:>8} {r[2]:>12} {r[3]:>9} | {r[4]:>8} {r[5]:>12} {r[6]:>9}")
    return best, route


def print_route(best, route):
    print("Entry")
    prev = None
    for line, st in route:
        tag = " Transfer" if prev is not None and prev != line else ""
        print(f"  ↓{tag}")
        print(f"Line {line} - Station {st}")
        prev = line
    print("  ↓\nExit")
    print(f"\nMinimum Production Time = {best}")
    print("Transfer points:", [(route[i - 1][1], f"L{route[i - 1][0]}->L{route[i][0]}")
                               for i in range(1, len(route)) if route[i][0] != route[i - 1][0]] or "none")


if __name__ == "__main__":
    a1 = [7, 9, 3, 4, 8, 4]
    a2 = [8, 5, 6, 4, 5, 7]
    t1 = [2, 3, 1, 3, 4]          # transfer line1 -> line2 after station j
    t2 = [2, 1, 2, 2, 1]          # transfer line2 -> line1 after station j
    e1, e2, x1, x2 = 2, 4, 3, 2
    print("=== 4.1 / 4.2 Base case ===")
    best, route = assembly(a1, a2, t1, t2, e1, e2, x1, x2)
    print_route(best, route)

    print("\n=== 4.3 Increase transfer times ===")
    print("PREDICTION (written before running): with every transfer cost raised from ~2 to 20, switching lines is no")
    print("longer worth it; the route should stay on ONE line, the transfer decision (the one the base plan used) is the")
    print("one affected, and the total time must not decrease.")
    t1b, t2b = [20] * 5, [20] * 5
    best2, route2 = assembly(a1, a2, t1b, t2b, e1, e2, x1, x2)
    print_route(best2, route2)
    print(f"Observed: total {best} -> {best2} ({'increased' if best2 > best else 'unchanged'}).")

    print("\n=== 4.4 Production disruption: station 3 on the line used at station 3 becomes slow (3 -> 30) ===")
    line_at_3 = route[2][0]
    a_dis = [a1[:], a2[:]]
    a_dis[line_at_3 - 1][2] = 30
    best3, route3 = assembly(a_dis[0], a_dis[1], t1, t2, e1, e2, x1, x2)
    print_route(best3, route3)
    print(f"Observed: route changes from {[r for r in route]} to {[r for r in route3]}; time {best} -> {best3}.")
    print("Explanation: Line 1 station 3 now costs 30, so entering it (even via a cheap transfer) is no longer optimal. The")
    print("DP keeps production on the other line through station 3, which also removes the two transfers around it, and the")
    print("minimum time rises only slightly because the DP re-optimises all later decisions from that point.")

    print("""
=== 4.5 Extension to three lines (not implemented) ===
State: f[i][j] stays the same idea, but i now ranges over 3 lines (a 3 x n table instead of 2 x n).
Transition: f[i][j] = a[i][j] + min( f[i][j-1],  min over k != i of ( f[k][j-1] + t[k][i][j-1] ) ) - a min over the
other TWO lines, with a transfer-time table t[k][i] for every ordered pair of lines (6 pairs) instead of 2 numbers.
Reconstruction: store for every (i, j) the line k that gave the minimum (predecessor pointer), then trace back from
the best of the 3 exit totals. Complexity grows from O(n) to O(n * m^2) for m lines; optimal substructure is unchanged.""")
