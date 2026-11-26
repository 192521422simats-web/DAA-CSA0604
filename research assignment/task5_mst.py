"""
Assignment 4B - Task 5: Kruskal, Prim and Boruvka on the same weighted graph.
Run: python task5_mst.py
"""
import heapq

V = ["A", "B", "C", "D", "E", "F", "G"]
EDGES = [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7), ("C", "E", 5),
         ("D", "E", 15), ("D", "F", 6), ("E", "F", 8), ("E", "G", 9), ("F", "G", 11)]


class DSU:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[ra] = rb
        return True


def kruskal(edges, verbose=True):
    d = DSU(V); mst = []
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if d.union(u, v):
            mst.append((u, v, w))
            if verbose: print(f"  Kruskal adds {u}-{v} ({w})  [joins two different components]")
        elif verbose:
            print(f"  Kruskal rejects {u}-{v} ({w})  [would form a cycle]")
    return mst


def prim(edges, start="A", verbose=True):
    adj = {v: [] for v in V}
    for u, v, w in edges:
        adj[u].append((w, u, v)); adj[v].append((w, v, u))
    seen = {start}; heap = list(adj[start]); heapq.heapify(heap); mst = []
    while heap and len(seen) < len(V):
        w, u, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v); mst.append((u, v, w))
        if verbose: print(f"  Prim adds {u}-{v} ({w})  [cheapest edge leaving the tree]")
        for e in adj[v]:
            if e[2] not in seen:
                heapq.heappush(heap, e)
    return mst


def boruvka(edges, verbose=True):
    d = DSU(V); mst = []; rnd = 0
    while len({d.find(v) for v in V}) > 1:
        rnd += 1
        cheapest = {}
        for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):    # fixed tie-break order
            ru, rv = d.find(u), d.find(v)
            if ru == rv:
                continue
            for r in (ru, rv):
                if r not in cheapest:
                    cheapest[r] = (u, v, w)
        added = set()
        for u, v, w in cheapest.values():
            if d.union(u, v):
                mst.append((u, v, w)); added.add((u, v, w))
        if verbose: print(f"  Boruvka round {rnd}: each component picks its cheapest outgoing edge -> adds {sorted(added)}")
    return mst


def total(m):
    return sum(w for _, _, w in m)


def norm(m):
    return sorted(tuple(sorted((u, v))) + (w,) for u, v, w in m)


if __name__ == "__main__":
    print("=== Same graph, three algorithms ===")
    res = {}
    for name, fn in (("Kruskal", kruskal), ("Prim", prim), ("Boruvka", boruvka)):
        print(name)
        m = fn(EDGES)
        res[name] = m
        print(f"  MST edges: {norm(m)}\n  Total cost = {total(m)}\n")
    assert total(res["Kruskal"]) == total(res["Prim"]) == total(res["Boruvka"])

    print("=== Stress: make several MSTs with equal total cost (ties) ===")
    # Square with all weights 1: any 3 of the 4 edges is an MST.
    TV = ["P", "Q", "R", "S"]
    TE = [("P", "Q", 1), ("Q", "R", 1), ("R", "S", 1), ("S", "P", 1), ("P", "R", 2)]
    V[:] = TV
    k = kruskal(TE, False); p = prim(TE, "P", False); b = boruvka(TE, False)
    # Prim from another start and Kruskal with reversed tie order give different but equal-cost trees
    p2 = prim(TE, "R", False)
    for name, m in (("Kruskal", k), ("Prim from P", p), ("Prim from R", p2), ("Boruvka", b)):
        print(f"  {name:<12} edges {norm(m)} total {total(m)}")
    print("Observation: the algorithms can return DIFFERENT edge sets, all with the same minimum total (here 3).")
    print("All are correct: the MST is unique only when edge weights are distinct; ties allow several optimal trees.")

    print("""
=== Industry decision ===
A. Sparse network (E ~ V): Kruskal - sorting E edges is cheap, union-find is tiny, simple edge-list storage.
   Prim with a binary heap is also fine (O(E log V)).
B. Dense network (E ~ V^2): Prim with an adjacency matrix / array (O(V^2)) avoids sorting ~V^2 edges and scans
   neighbours of one growing tree sequentially; Kruskal would waste time sorting a huge edge list.
C. Very large graph on parallel/distributed hardware: Boruvka - every component picks its cheapest edge
   independently in each round, components at least halve each round (O(log V) rounds), so the work parallelises;
   Kruskal's single global sorted order and Prim's single growing tree are inherently sequential.""")
