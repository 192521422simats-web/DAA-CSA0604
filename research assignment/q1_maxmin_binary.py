"""
Assignment 3 - Q1: Divide-and-Conquer Max/Min and Binary Search.
Part A: Max/Min by divide and conquer (tournament). Base cases: 1 element (0 comps) and 2 elements (1 comp).
        Combine: compare the two maxima and the two minima (2 comparisons).
        T(n) = 2T(n/2) + 2, T(2) = 1   ->   T(n) = 3n/2 - 2 for n a power of 2.
        Independent max and min scanning needs 2(n-1) comparisons.
Part B: Binary search - each comparison eliminates half of the remaining sorted range.
Run: python q1_maxmin_binary.py
"""
import math
import random


def max_min(a, lo, hi, cnt):
    if lo == hi:
        return a[lo], a[lo]
    if hi == lo + 1:
        cnt[0] += 1
        return (a[hi], a[lo]) if a[hi] > a[lo] else (a[lo], a[hi])
    mid = (lo + hi) // 2
    mx1, mn1 = max_min(a, lo, mid, cnt)
    mx2, mn2 = max_min(a, mid + 1, hi, cnt)
    cnt[0] += 2                                   # combine: compare maxima, compare minima
    return max(mx1, mx2), min(mn1, mn2)


def naive_max_min(a):
    mx = mn = a[0]; c = 0
    for x in a[1:]:
        c += 1
        if x > mx: mx = x
        c += 1
        if x < mn: mn = x
    return mx, mn, c


def binary_search(a, key):
    lo, hi, c = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if a[mid] == key:
            return mid, c
        c += 1
        if key < a[mid]:
            hi = mid - 1        # key cannot be in a[mid..hi]: all those are >= a[mid] > key
        else:
            lo = mid + 1        # key cannot be in a[lo..mid]: all those are <= a[mid] < key
    return -1, c


if __name__ == "__main__":
    random.seed(1)
    print("Part A: Max/Min (predicted D&C comparisons = 3n/2 - 2 for n = 2^k)")
    print(f"{'n':>7} {'D&C observed':>13} {'3n/2-2':>8} {'naive 2(n-1)':>13}  correct")
    for n in (2, 8, 64, 1024, 8192, 65536):
        a = [random.randint(-10**6, 10**6) for _ in range(n)]
        cnt = [0]
        mx, mn = max_min(a, 0, n - 1, cnt)
        _, _, nc = naive_max_min(a)
        ok = (mx == max(a) and mn == min(a))
        pred = 3 * n // 2 - 2
        print(f"{n:>7} {cnt[0]:>13} {pred:>8} {nc:>13}  {ok}")
    print("Non power-of-2 sizes: the simple midpoint split gives somewhat more than ceil(3n/2)-2 (the formula is exact\nonly for n = 2^k), but still well below the naive 2(n-1):")
    for n in (5, 7, 100, 1000):
        a = [random.random() for _ in range(n)]
        cnt = [0]
        max_min(a, 0, n - 1, cnt)
        print(f"  n={n:>5}: {cnt[0]} comparisons, ceil(3n/2)-2 = {math.ceil(3 * n / 2) - 2}, naive 2(n-1) = {2 * (n - 1)}")

    print("\nPart B: Binary search (successful and unsuccessful) - comparison counts")
    print(f"{'n':>8} {'found(mid)':>11} {'found(first)':>13} {'found(last)':>12} {'missing':>8} {'log2(n)':>8}")
    for n in (10, 100, 1000, 10000, 100000, 1000000):
        a = list(range(0, 2 * n, 2))              # even numbers, so odd numbers are guaranteed missing
        mid = binary_search(a, a[n // 2])[1]
        first = binary_search(a, a[0])[1]
        last = binary_search(a, a[-1])[1]
        miss = binary_search(a, 2 * n + 1)[1]
        print(f"{n:>8} {mid:>11} {first:>13} {last:>12} {miss:>8} {math.log2(n):>8.1f}")
    print("""
Each step eliminates half the range, so at most floor(log2 n)+1 probes are needed.
(Counts above include both the == and < tests per probe, i.e. about 2x the number of probes.)
Termination: the loop stops when lo > hi (empty range) - the key cannot exist anywhere else.""")
