"""
Assignment 2 - Q2: Sequential search for tool tracking.
Experiments: successful searches at different positions, unsuccessful searches, different list sizes.
Run: python q2_sequential_search.py
"""
import random


def sequential_search(tools, target):
    comps = 0
    for i, t in enumerate(tools):
        comps += 1
        if t == target:
            return i, comps
    return -1, comps


if __name__ == "__main__":
    random.seed(3)
    print("Experiment 1: successful search at different positions (list size n = 1000)")
    n = 1000
    tools = [f"T-{i}" for i in range(n)]
    for label, pos in (("first", 0), ("quarter", n // 4), ("middle", n // 2),
                       ("three-quarter", 3 * n // 4), ("last", n - 1)):
        idx, c = sequential_search(tools, tools[pos])
        print(f"  {label:<14} position {pos:>4}: comparisons = {c}")

    print("\nExperiment 2: unsuccessful search (tool not issued: T-9999)")
    print(f"  comparisons = {sequential_search(tools, 'T-9999')[1]}  (always n)")

    print("\nExperiment 3: different list sizes (average over 1000 random successful searches)")
    print(f"  {'n':>8} {'avg comps (found)':>18} {'comps (not found)':>18}   n/2")
    for n in (10, 100, 1000, 10000, 100000):
        tools = [f"T-{i}" for i in range(n)]
        total = sum(sequential_search(tools, random.choice(tools))[1] for _ in range(1000))
        print(f"  {n:>8} {total / 1000:>18.1f} {sequential_search(tools, 'none')[1]:>18} {n / 2:>8.0f}")

    print("\nExperiment 4: changed condition - 20 facilities, lookups per day")
    for records, lookups in ((200, 500), (4000, 10000), (40000, 200000)):
        work = records / 2 * lookups
        print(f"  records={records:>6}, lookups/day={lookups:>7}: ~{work:,.0f} comparisons/day")

    print("""
CONCLUSION
Sequential search is reasonable when the list is small (hundreds of records) and lookups are
infrequent, because the list changes constantly and keeping it sorted/indexed would cost more than
it saves. Average cost is ~n/2, worst/unsuccessful is n.
When the organisation grows to 20 facilities (many more records and lookups) the total work grows as
(records x lookups), so I would stop recommending it above roughly a few thousand records with
frequent lookups and switch to a hash table keyed by Tool ID (O(1) average, easy insert/delete).""")
