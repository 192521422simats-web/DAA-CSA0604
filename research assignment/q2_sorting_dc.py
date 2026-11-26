"""
Assignment 3 - Q2: Merge Sort vs Quick Sort.
Quick Sort pivot strategy (clearly stated): FIRST element of the sub-array is the pivot.
Balanced input  : constructed so the first element is the median at every level.
Unbalanced input: already sorted array (pivot is always the minimum -> partitions of size 0 and n-1).
Records: partition sizes, max recursion depth and comparisons.
Run: python q2_sorting_dc.py
"""
import random
import sys

sys.setrecursionlimit(100000)


def merge_sort(a, stats, depth=1):
    stats["depth"] = max(stats["depth"], depth)
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], stats, depth + 1)
    right = merge_sort(a[mid:], stats, depth + 1)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        stats["comps"] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def quick_sort(a, stats, depth=1):
    stats["depth"] = max(stats["depth"], depth)
    if len(a) <= 1:
        return a
    p = a[0]
    left, right = [], []
    for x in a[1:]:
        stats["comps"] += 1
        (left if x < p else right).append(x)
    if len(stats["splits"]) < 7:
        stats["splits"].append((len(left), len(right)))
    return quick_sort(left, stats, depth + 1) + [p] + quick_sort(right, stats, depth + 1)


def balanced_input(vals):
    if not vals:
        return []
    m = len(vals) // 2
    return [vals[m]] + balanced_input(vals[:m]) + balanced_input(vals[m + 1:])


if __name__ == "__main__":
    n = 1023
    random.seed(4)
    inputs = {
        "Quick-balanced (constructed)": balanced_input(list(range(n))),
        "Quick-unbalanced (sorted)": list(range(n)),
        "Random": random.sample(range(n), n),
    }
    print(f"n = {n}; log2(n) ~ {n.bit_length()}; n^2/2 ~ {n * n // 2}")
    print(f"{'Input':<30}{'Algorithm':<12}{'comparisons':>12}{'max depth':>10}   first partition sizes (left,right)")
    for name, data in inputs.items():
        for algo, fn in (("QuickSort", quick_sort), ("MergeSort", merge_sort)):
            st = {"comps": 0, "depth": 0, "splits": []}
            out = fn(data, st)
            assert out == sorted(data)
            sp = st["splits"][:4] if algo == "QuickSort" else "-"
            print(f"{name:<30}{algo:<12}{st['comps']:>12}{st['depth']:>10}   {sp}")
    print("""
ANALYSIS
- Merge Sort always splits exactly in half -> recursion depth ~log2(n), comparisons ~ n log n for ANY input.
- Quick Sort's split quality depends on pivot value. Balanced pivot -> depth ~log n, ~n log n comparisons.
  With the first element as pivot on sorted data the splits are (0, n-1): depth n and ~n^2/2 comparisons.
  Recurrence: T(n) = T(n-1) + n  ->  O(n^2).  A 90:10 split gives T(n)=T(0.9n)+T(0.1n)+n = O(n log n) but
  with a bigger constant (depth ~ log_{10/9} n).
JOINT DESIGN QUESTION - information I would want before choosing: how much is already sorted / how
adversarial the order can be, input size, whether stability is required, memory limits (Merge Sort needs
O(n) extra), whether data is in memory or on disk, and the cost of comparing items. If nothing is known,
Merge Sort (predictable) or Quick Sort with random / median-of-three pivot are the safe choices.""")
