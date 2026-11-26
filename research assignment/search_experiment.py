"""
DAA Assignment 1 - Student Record Search (Tasks 8, 9, 12)

Three different strategies for finding a registration number:
  1. Linear (sequential) search   - iterative, no preprocessing
  2. Binary search                - recursive, needs sorted data (preprocessing = sort)
  3. Hash table with chaining     - needs a build step (preprocessing = hashing all records)

Basic operation counted: key comparisons
(for the hash table: comparisons made inside one bucket).

Run:  python search_experiment.py
"""
import math
import random
import sys
import time

sys.setrecursionlimit(10000)


# ---------- Approach 1: Linear search (iterative) ----------
def linear_search(arr, key):
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == key:
            return i, comparisons
    return -1, comparisons


# ---------- Approach 2: Binary search (recursive) ----------
def binary_search(arr, key, low=0, high=None, counter=None):
    if counter is None:
        counter = [0]
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1, counter[0]
    mid = (low + high) // 2
    counter[0] += 1                      # comparison arr[mid] == key
    if arr[mid] == key:
        return mid, counter[0]
    counter[0] += 1                      # comparison key < arr[mid]
    if key < arr[mid]:
        return binary_search(arr, key, low, mid - 1, counter)
    return binary_search(arr, key, mid + 1, high, counter)


# ---------- Approach 3: Hash table with separate chaining ----------
class HashTable:
    def __init__(self, size):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key):
        self.buckets[self._hash(key)].append(key)

    def search(self, key):
        comparisons = 0
        for item in self.buckets[self._hash(key)]:
            comparisons += 1
            if item == key:
                return True, comparisons
        return False, comparisons


def make_data(n):
    """n unique registration numbers in random order (as stored in the database)."""
    return random.sample(range(10_000_000, 99_999_999), n)


def run_experiment(sizes=(1000, 10000, 100000, 1000000), queries=200):
    random.seed(42)
    results = []
    print(f"{'n':>9} | {'algo':<8} | {'preproc(s)':>10} | {'avg cmp found':>13} | "
          f"{'avg cmp missing':>15} | {'time/search(us)':>15}")
    print("-" * 85)
    for n in sizes:
        data = make_data(n)
        present = random.sample(data, queries)
        absent = [random.randint(100_000_000, 200_000_000) for _ in range(queries)]

        # Linear: no preprocessing (fewer queries for very large n, still representative)
        q = queries if n <= 100000 else 50
        t0 = time.perf_counter()
        found = [linear_search(data, k)[1] for k in present[:q]]
        miss = [linear_search(data, k)[1] for k in absent[:q]]
        t = (time.perf_counter() - t0) / (2 * q) * 1e6
        results.append((n, "Linear", 0.0, sum(found) / q, sum(miss) / q, t))

        # Binary: preprocessing = sort
        t0 = time.perf_counter()
        sdata = sorted(data)
        pre = time.perf_counter() - t0
        t0 = time.perf_counter()
        found = [binary_search(sdata, k)[1] for k in present]
        miss = [binary_search(sdata, k)[1] for k in absent]
        t = (time.perf_counter() - t0) / (2 * queries) * 1e6
        results.append((n, "Binary", pre, sum(found) / queries, sum(miss) / queries, t))

        # Hash: preprocessing = build table (size ~ n, load factor ~ 1)
        t0 = time.perf_counter()
        ht = HashTable(n)
        for k in data:
            ht.insert(k)
        pre = time.perf_counter() - t0
        t0 = time.perf_counter()
        found = [ht.search(k)[1] for k in present]
        miss = [ht.search(k)[1] for k in absent]
        t = (time.perf_counter() - t0) / (2 * queries) * 1e6
        results.append((n, "Hash", pre, sum(found) / queries, sum(miss) / queries, t))

    for r in results:
        print(f"{r[0]:>9} | {r[1]:<8} | {r[2]:>10.4f} | {r[3]:>13.1f} | {r[4]:>15.1f} | {r[5]:>15.2f}")
    return results


def correctness_tests():
    print("=== Correctness tests ===")
    arr = [5, 12, 18, 25, 31, 40, 77]
    ht = HashTable(7)
    for x in arr:
        ht.insert(x)
    for key, expect in [(5, True), (77, True), (25, True), (6, False), (100, False)]:
        a = linear_search(arr, key)[0] != -1
        b = binary_search(arr, key)[0] != -1
        c = ht.search(key)[0]
        status = "PASS" if a == b == c == expect else "FAIL"
        print(f"key={key:<4} expected={expect!s:<5} linear={a!s:<5} binary={b!s:<5} hash={c!s:<5} {status}")
    print("Boundary: empty list      ->", linear_search([], 1)[0], binary_search([], 1)[0])
    print("Boundary: single element  ->", linear_search([9], 9)[0], binary_search([9], 9)[0])


def day4_design_challenge(n=1_000_000, per_hour=50_000):
    """Task 12: 50,000 searches/hour on 1,000,000 records; new records only once per day."""
    print("\n=== Day-4 Design Challenge: cost of one day (24 h) ===")
    searches = per_hour * 24
    linear = searches * (n / 2)                                   # average successful search
    binary = n * math.log2(n) + searches * math.log2(n)           # sort once + searches
    hashing = n + searches * 1                                    # build once + O(1) average
    print(f"Searches per day                         : {searches:,}")
    print(f"Linear total comparisons                 : {linear:,.0f}")
    print(f"Binary total comparisons (sort + search) : {binary:,.0f}")
    print(f"Hash total operations (build + search)   : {hashing:,.0f}")
    print("Records change only once a day, so the preprocessing cost is paid once and shared by")
    print("1,200,000 searches. Binary/Hash clearly beat Linear; Hash is best if only exact-match")
    print("lookups are needed, Binary is better if range queries / sorted output are also needed.")


if __name__ == "__main__":
    correctness_tests()
    print("\n=== Performance experiment ===")
    res = run_experiment()
    day4_design_challenge()
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        for algo in ("Linear", "Binary", "Hash"):
            xs = [r[0] for r in res if r[1] == algo]
            ys = [r[3] for r in res if r[1] == algo]
            plt.plot(xs, ys, marker="o", label=algo)
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("n (records)")
        plt.ylabel("avg comparisons (successful search)")
        plt.title("Comparisons vs n")
        plt.legend()
        plt.grid(True, which="both", alpha=0.3)
        plt.savefig("comparisons_plot.png", dpi=120)
        print("\nSaved comparisons_plot.png")
    except ImportError:
        print("(matplotlib not installed - plot skipped)")
