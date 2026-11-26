"""
Assignment 3 - Q6: (A) Median of Medians vs QuickSelect, (B) Meet-in-the-Middle subset sum.
Run: python q6_selection_and_meet_in_middle.py
"""
import bisect
import itertools
import random
import sys

sys.setrecursionlimit(100000)

# ---------------- Part A: k-th smallest ----------------
def quickselect(a, k, pivot_rule, st):
    """k is 0-based. pivot_rule: 'first' (deterministic) or 'random'."""
    if len(a) == 1:
        return a[0]
    p = a[0] if pivot_rule == "first" else random.choice(a)
    st["comps"] += len(a)
    lo = [x for x in a if x < p]
    eq = [x for x in a if x == p]
    hi = [x for x in a if x > p]
    if k < len(lo):
        return quickselect(lo, k, pivot_rule, st)
    if k < len(lo) + len(eq):
        return p
    return quickselect(hi, k - len(lo) - len(eq), pivot_rule, st)


def mom_select(a, k, st):
    """Median of Medians (groups of 5) - worst-case O(n)."""
    if len(a) <= 5:
        st["comps"] += len(a) * 2
        return sorted(a)[k]
    groups = [sorted(a[i:i + 5]) for i in range(0, len(a), 5)]
    st["comps"] += len(a) * 2                              # sorting small groups
    medians = [g[len(g) // 2] for g in groups]
    pivot = mom_select(medians, len(medians) // 2, st)    # median of the medians
    st["comps"] += len(a)
    lo = [x for x in a if x < pivot]
    eq = [x for x in a if x == pivot]
    hi = [x for x in a if x > pivot]
    if k < len(lo):
        return mom_select(lo, k, st)
    if k < len(lo) + len(eq):
        return pivot
    return mom_select(hi, k - len(lo) - len(eq), st)


# ---------------- Part B: subset sum ----------------
def subset_sum_bruteforce(nums, target):
    checks = 0
    for mask in range(1 << len(nums)):
        checks += 1
        s = sum(nums[i] for i in range(len(nums)) if mask >> i & 1)
        if s == target:
            return True, checks
    return False, checks


def all_sums(nums):
    sums = [0]
    for x in nums:
        sums += [s + x for s in sums]
    return sums


def meet_in_middle(nums, target):
    h = len(nums) // 2
    left, right = all_sums(nums[:h]), all_sums(nums[h:])
    right.sort()                                           # extra memory: 2^(n/2) sums per half
    work = len(left) + len(right)
    for s in left:
        work += 1
        i = bisect.bisect_left(right, target - s)
        if i < len(right) and right[i] == target - s:
            return True, work, len(left) + len(right)
    return False, work, len(left) + len(right)


if __name__ == "__main__":
    random.seed(21)
    print("PART A - k-th smallest (median) selection; comparisons counted")
    print(f"{'n':>6} {'input':<14} {'QuickSelect(first)':>19} {'QuickSelect(random)':>20} {'MedianOfMedians':>16}")
    for n in (1000, 5000):
        for name, data in (("random", random.sample(range(10 * n), n)), ("sorted", list(range(n)))):
            k = n // 2
            res = []
            for rule in ("first", "random"):
                st = {"comps": 0}
                r = quickselect(data, k, rule, st); res.append(st["comps"])
                assert r == sorted(data)[k]
            st = {"comps": 0}
            r = mom_select(data, k, st)
            assert r == sorted(data)[k]
            print(f"{n:>6} {name:<14} {res[0]:>19} {res[1]:>20} {st['comps']:>16}")
    print("""
Note: on random data Median of Medians does MORE work than QuickSelect (larger constant factor) but its\nworst case never degrades; QuickSelect(first) explodes on sorted input.\nGrouping: split into groups of 5, take each group's median, recursively find the median of those medians
and use it as pivot. This pivot is guaranteed to have at least ~30% of the elements on each side, so each
partition discards a constant fraction -> T(n) <= T(n/5) + T(7n/10) + O(n) = O(n) worst case.
The deterministic 'first element' pivot on sorted input gives n^2/2-type work. Random pivots make that
unlikely but cannot rule it out (a bad sequence of random picks is still possible).
Student B verification: pivot quality decides how much of the data each step discards; poor pivots discard
almost nothing, so the work becomes quadratic.""")

    print("\nPART B - Meet-in-the-Middle subset sum (target chosen so that NO subset matches: worst case)")
    print(f"{'n':>3} {'2^n enumeration':>16} {'MITM work':>10} {'MITM memory(sums)':>18}")
    for n in (10, 16, 20, 22):
        nums = [2 * random.randint(1, 500) for _ in range(n)]         # all even
        target = sum(nums) // 2 | 1                                    # odd target: impossible
        ok1, c1 = subset_sum_bruteforce(nums, target) if n <= 20 else (False, 2 ** n)
        ok2, w, mem = meet_in_middle(nums, target)
        assert ok1 == ok2 == False
        print(f"{n:>3} {c1:>16} {w:>10} {mem:>18}")
    nums = [3, 34, 4, 12, 5, 2]
    print("\nCorrectness: nums =", nums, " target 9 ->", meet_in_middle(nums, 9)[0], " target 30 ->", meet_in_middle(nums, 30)[0])
    print("""
Split the n numbers into two halves; each half has 2^(n/2) subset sums. Sort one list and, for each sum s of
the other, binary-search for target - s. Time ~ O(2^(n/2) * n) instead of 2^n, using O(2^(n/2)) extra memory
(the time-memory trade-off). Student A verification: extra storage lets us replace one huge enumeration of
2^n combinations by two small enumerations plus fast lookups, so the total work shrinks dramatically.""")
