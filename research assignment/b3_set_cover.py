"""
Assignment 5 Part B - B3: Emergency-service Set Cover, exact vs greedy approximation.
Exact: try every combination of centres of size 1, 2, 3, ... until one covers all zones (first success is optimal).
Greedy: repeatedly pick the centre covering the most currently uncovered zones.
Run: python b3_set_cover.py
"""
import itertools
import random
import time


def exact_cover(universe, sets):
    """sets: dict name -> set of zones. Returns (chosen names, combinations examined)."""
    names = list(sets)
    examined = 0
    for size in range(1, len(names) + 1):
        for combo in itertools.combinations(names, size):
            examined += 1
            covered = set().union(*(sets[c] for c in combo))
            if covered >= universe:
                return list(combo), examined
    return None, examined


def greedy_cover(universe, sets, show=False):
    uncovered = set(universe); chosen = []; ops = 0
    while uncovered:
        best, gain = None, 0
        for name, zones in sets.items():
            ops += 1
            g = len(zones & uncovered)
            if g > gain:
                best, gain = name, g
        if best is None:
            return None, ops                         # some zone cannot be covered by any centre
        chosen.append(best)
        uncovered -= sets[best]
        if show:
            print(f"    pick {best} (covers {gain} new zones) -> uncovered now {sorted(uncovered)}")
    return chosen, ops


def random_instance(zones, centres, seed):
    rnd = random.Random(seed)
    universe = set(range(1, zones + 1))
    sets = {f"C{i}": set(rnd.sample(sorted(universe), rnd.randint(2, max(3, zones // 3)))) for i in range(centres)}
    covered = set().union(*sets.values())
    for z in universe - covered:                       # guarantee a cover exists
        sets[f"C{rnd.randrange(centres)}"].add(z)
    return universe, sets


if __name__ == "__main__":
    print("=== B3.1 Three small instances (not chosen to make greedy look good) ===")
    insts = [
        ({1, 2, 3, 4, 5, 6}, {"C1": {1, 2, 3}, "C2": {4, 5, 6}, "C3": {1, 4}, "C4": {2, 5}}),
        ({1, 2, 3, 4, 5, 6, 7, 8}, {"C1": {1, 2, 3, 4}, "C2": {3, 4, 5, 6}, "C3": {5, 6, 7, 8}, "C4": {1, 2, 7, 8}, "C5": {2, 4, 6, 8}}),
        ({1, 2, 3, 4, 5, 6}, {"X": {1, 2, 3, 4}, "Y": {1, 3, 5}, "Z": {2, 4, 6}}),
    ]
    print(f"{'Instance':>9} {'Exact size':>11} {'Greedy size':>12} {'Same?':>6}")
    for i, (u, s) in enumerate(insts, 1):
        e, _ = exact_cover(u, s); g, _ = greedy_cover(u, s)
        print(f"{i:>9} {len(e):>11} {len(g):>12} {str(len(e) == len(g)):>6}")

    print("\n=== B3.2 Counterexample (instance 3 above) ===")
    u, s = insts[2]
    print("Zones 1..6; X={1,2,3,4}, Y={1,3,5}, Z={2,4,6}")
    e, _ = exact_cover(u, s)
    print("  Exact optimum:", e, "->", len(e), "centres")
    print("  Greedy trace:")
    g, _ = greedy_cover(u, s, show=True)
    print("  Greedy result:", g, "->", len(g), "centres")
    print("  Decision that led away from the optimum: choosing X first (largest immediate coverage, 4 zones). It covers")
    print("  only zones that Y and Z would also cover, leaving 5 and 6 which then require TWO more centres.")

    print("\n=== B3.3 Increasing problem size (random instances) ===")
    print(f"{'zones':>5} {'centres':>8} | {'exact combos examined':>22} {'exact time(s)':>14} {'exact size':>11} | "
          f"{'greedy ops':>11} {'greedy size':>12}")
    for zones, centres in ((8, 8), (12, 12), (16, 16), (20, 20), (24, 24), (30, 26)):
        u, s = random_instance(zones, centres, seed=zones)
        t0 = time.perf_counter()
        e, ex = exact_cover(u, s)
        te = time.perf_counter() - t0
        g, gops = greedy_cover(u, s)
        print(f"{zones:>5} {centres:>8} | {ex:>22} {te:>14.3f} {len(e):>11} | {gops:>11} {len(g):>12}")
    print("""
=== B3.4 Engineering trade-off ===
Gain: greedy needs ~ (cover size x number of centres) set operations - almost constant growth in this table - while the
exact search examines a rapidly growing number of combinations (it grows like C(m, k): exponential in the number of centres).
Sacrifice: the greedy cover can be larger than the minimum (counterexample above) and has no optimality guarantee, only a
logarithmic approximation ratio (H(n) ~ ln n) in the worst case; in these random instances it was usually equal or +1.
I would accept greedy in a real emergency-planning system with hundreds of candidate centres where a result is needed in
seconds, an extra centre is affordable, and the plan will be re-run as conditions change.""")
