"""
Assignment 5 Part B - B1 (instrumented backtracking) and B2 (adversarial input) for Graph Colouring.
Decision: can the vertices be coloured with at most k colours so that no edge joins two equal colours?
Search tree node = partial assignment of colours to the first t vertices of the chosen order.
Pruning: a colour c is rejected for vertex v if a neighbour that is already coloured has colour c.
Version 1: vertices in input order.
Version 2: static ordering heuristic: highest degree first, then the vertex with most already-ordered
           neighbours (ties by degree). Idea: constrained vertices are decided early so conflicts show up
           near the root of the search tree where they prune huge subtrees.
Run: python b1_b2_graph_colouring.py
"""
import sys

sys.setrecursionlimit(10000)


def make_adj(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return adj


def order_input(n, adj):
    return list(range(n))


def order_heuristic(n, adj):
    order, left = [], set(range(n))
    while left:
        placed = set(order)
        v = max(left, key=lambda x: (len(adj[x] & placed), len(adj[x]), -x))
        order.append(v); left.remove(v)
    return order


def colour(n, edges, k, order_fn=order_input):
    adj = make_adj(n, edges)
    order = order_fn(n, adj)
    col = [-1] * n
    st = {"nodes": 0, "candidates": 0, "rejected": 0, "backtracks": 0, "max_depth": 0}

    def solve(t):
        st["nodes"] += 1
        st["max_depth"] = max(st["max_depth"], t)
        if t == n:
            return True
        v = order[t]
        for c in range(k):
            st["candidates"] += 1
            if any(col[u] == c for u in adj[v]):          # feasibility test (pruning)
                st["rejected"] += 1
                continue
            col[v] = c                                    # assign
            if solve(t + 1):                              # explore
                return True
            col[v] = -1                                   # undo
            st["backtracks"] += 1
        return False

    ok = solve(0)
    return ok, (col[:] if ok else None), st


def valid(n, edges, col):
    return all(col[u] != col[v] for u, v in edges)


def show(name, n, edges, k, order_fn=order_input):
    ok, col, st = colour(n, edges, k, order_fn)
    print(f"  {name}: colourable={ok}, colouring={col}, nodes={st['nodes']}, candidates={st['candidates']}, "
          f"rejected={st['rejected']}, backtracks={st['backtracks']}, max depth={st['max_depth']}")
    if ok:
        assert valid(n, edges, col)
    return ok, st


if __name__ == "__main__":
    print("=== B1.1 Validation tests ===")
    print("Test 1: 5-cycle with k=3 (colourable). Verifies the search finds a valid colouring.")
    c5 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    assert show("C5,k=3", 5, c5, 3)[0]
    print("Test 2: K4 (complete graph on 4 vertices) with k=3 (NOT colourable). Verifies failure is reported.")
    k4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    assert not show("K4,k=3", 4, k4, 3)[0]
    print("Test 3 (boundary): single vertex k=1, no vertices, and one edge with k=1.")
    show("1 vertex,k=1", 1, [], 1)
    show("0 vertices,k=1", 0, [], 1)
    show("edge,k=1", 2, [(0, 1)], 1)

    print("\n=== B1.2 Design vs implementation ===")
    print("Implementation difference from the pseudocode: neighbours are stored as sets so the feasibility test only")
    print("scans the neighbours of the current vertex (not all edges); a 'colour array' with -1 = uncoloured is used, and")
    print("counters were added for nodes/candidates/rejections/backtracks.")

    print("\n=== B1.3/B1.4 Version 1 (input order) vs Version 2 (degree/connectivity heuristic) ===")
    # Graph where a dense core appears late in the input order, plus loosely connected early vertices.
    n = 14
    edges = [(i, i + 1) for i in range(9)] + [(10, 11), (10, 12), (10, 13), (11, 12), (11, 13), (12, 13)]
    graphs = {
        "Ring of 10 + 2 chords (k=3, colourable)":
            (10, [(i, (i + 1) % 10) for i in range(10)] + [(0, 5), (2, 7)], 3),
        "Path of 10 + K4 (k=3, NOT colourable)": (n, edges, 3),
        "Complete bipartite K4,4 (k=2)": (8, [(i, j) for i in range(4) for j in range(4, 8)], 2),
    }
    print(f"{'Graph':<46}{'Measure':<22}{'Version 1':>10}{'Version 2':>10}")
    for name, (gn, ge, gk) in graphs.items():
        _, _, s1 = colour(gn, ge, gk, order_input)
        _, _, s2 = colour(gn, ge, gk, order_heuristic)
        for key, label in (("nodes", "Search nodes"), ("candidates", "Candidate assignments"),
                           ("rejected", "Rejected branches"), ("backtracks", "Backtracks")):
            print(f"{name if key == 'nodes' else '':<46}{label:<22}{s1[key]:>10}{s2[key]:>10}")
    print("""
Answer: yes on the graphs with a hidden dense core (Path + K4): the heuristic starts with the K4 vertices, finds that
3 colours cannot colour them after a handful of nodes and stops, while input order first enumerates thousands of
colourings of the path before reaching the K4. On graphs that are easy in any order (ring with chords, K4,4) the
two versions behave similarly, so the heuristic helps when conflicts are concentrated in a dense part of the graph.""")

    print("\n=== B2 Adversarial input: same n = 16 vertices, same k = 3 ===")
    # Graph A: a path 0-1-...-15 (easy, colourable, pruning rarely needed)
    A = [(i, i + 1) for i in range(15)]
    # Graph B: a path on vertices 0..11 (many valid colourings) and a K4 on vertices 12..15 (impossible with 3 colours)
    B = [(i, i + 1) for i in range(11)] + [(12 + i, 12 + j) for i in range(4) for j in range(i + 1, 4)]
    print("PREDICTION: Graph B needs far more search. The K4 (not 3-colourable) is only reached at depth 12; before that the")
    print("algorithm happily assigns the path vertices (3*2^11 = 6144 colourings), and each one fails at the K4. Rejected")
    print("branches will appear only late (deep in the tree), so pruning happens late. Graph A succeeds on the first dive.")
    for name, g in (("Graph A (path, easy)", A), ("Graph B (path + hidden K4)", B)):
        show(name, 16, g, 3)
    print("""
Why input size alone is not enough: both graphs have 16 vertices and k=3, yet the search effort differs by orders of
magnitude. Backtracking cost depends on the STRUCTURE of the instance - where conflicts occur relative to the search
order. In Graph B the contradiction (K4 needing 4 colours) is independent of the path vertices, but the search cannot
know that, so it re-explores every path colouring (thrashing). Structural property: a dense subgraph (clique larger
than k) that is ordered last and disconnected from the earlier vertices.
(Version 2 order, for comparison:)""")
    show("Graph B, Version 2 order", 16, B, 3, order_heuristic)
