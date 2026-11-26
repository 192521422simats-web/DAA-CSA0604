"""
Assignment 2 - Q1: Selection, Bubble and Insertion Sort under different data conditions.
Records comparisons and swaps/movements. Predictions are printed BEFORE the results.
Run: python q1_sorting.py
"""
import random


def selection_sort(a):
    a = a[:]; comps = moves = 0
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]; moves += 1
    return a, comps, moves


def bubble_sort(a):
    """Plain bubble sort WITH early-exit flag (stops when a pass makes no swap)."""
    a = a[:]; comps = moves = 0
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; moves += 1; swapped = True
        if not swapped:
            break
    return a, comps, moves


def insertion_sort(a):
    a = a[:]; comps = moves = 0
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]; moves += 1; j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps, moves


def datasets(n=1000):
    random.seed(1)
    rnd = random.sample(range(1, 10 * n), n)
    srt = sorted(rnd)
    rev = srt[::-1]
    # 95% already in order, 5% new orders appended at the end (the fulfilment-centre scenario)
    k = n // 20
    nearly = srt[:n - k] + random.sample(range(1, 10 * n), k)
    return {
        "Random": rnd,
        "Already sorted": srt,
        "Reverse sorted": rev,
        "95% sorted (appended 5% new)": nearly,
        "Edge: all equal priority": [7] * n,
    }


PREDICTIONS = """
PREDICTIONS (made before running)
- Selection sort: always ~n(n-1)/2 comparisons whatever the order (it always scans the rest), but
  at most n-1 swaps. So it should look the same on every dataset in comparisons.
- Bubble sort (with early exit): sorted input needs one pass (n-1 comparisons, 0 swaps).
  Reverse needs ~n^2/2 comparisons AND ~n^2/2 swaps (worst case).
- Insertion sort: sorted input -> n-1 comparisons, 0 moves (best). Reverse -> ~n^2/2 comparisons
  and moves. Nearly sorted -> close to linear, because each element only moves a short distance.
- All-equal: insertion sort and bubble sort behave like sorted input because the test is strict (>).
"""

if __name__ == "__main__":
    print(PREDICTIONS)
    n = 1000
    print(f"{'Dataset':<32}{'Algorithm':<12}{'Comparisons':>12}{'Swaps/Moves':>13}")
    print("-" * 69)
    for name, data in datasets(n).items():
        expected = sorted(data)
        for algo_name, algo in (("Selection", selection_sort), ("Bubble", bubble_sort),
                                ("Insertion", insertion_sort)):
            out, c, m = algo(data)
            assert out == expected, f"{algo_name} failed on {name}"
            print(f"{name:<32}{algo_name:<12}{c:>12}{m:>13}")
        print()
    print("""RECOMMENDATION: with ~95% of orders already in priority order, use INSERTION SORT.
On that dataset it needs far fewer comparisons than Selection/Bubble sort (close to O(n) because
every element is already near its final place), and only the few new orders cause movement.
Selection sort always pays n(n-1)/2 comparisons; bubble sort pays extra passes for out-of-place items.""")
