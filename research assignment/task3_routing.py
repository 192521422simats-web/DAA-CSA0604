"""
Assignment 4B - Task 3: Routing engine - Dijkstra, Bellman-Ford, Floyd, Warshall.
Graph: 8 vertices, 13 directed edges.
Run: python task3_routing.py
"""
import heapq

INF = float("inf")
V = ["S", "A", "B", "C", "D", "E", "F", "G"]
EDGES = [("S", "A", 7), ("S", "B", 4), ("S", "C", 3), ("A", "D", 3), ("A", "B", 1), ("B", "C", 2),
         ("B", "E", 5), ("C", "D", 8), ("C", "F", 6), ("D", "G", 2), ("E", "G", 3), ("E", "F", 2),
         ("F", "G", 1)]


def adj_of(edges):
    adj = {v: [] for v in V}
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def path_to(pred, t):
    p = []
    while t is not None:
        p.append(t); t = pred[t]
    return p[::-1]


def dijkstra(edges, src, verbose=True):
    adj = adj_of(edges)
    dist = {v: INF for v in V}; pred = {v: None for v in V}
    dist[src] = 0
    done, order = set(), []
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u); order.append(u)               # u is FINALISED here (assumes no negative edges)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w; pred[v] = u
                heapq.heappush(pq, (dist[v], v))
    if verbose:
        print("  Finalisation order:", order)
        for v in V:
            print(f"  {src}->{v}: dist={dist[v]}  path={' -> '.join(path_to(pred, v)) if dist[v] < INF else 'unreachable'}  predecessor={pred[v]}")
    return dist, pred


def bellman_ford(edges, src, verbose=True):
    dist = {v: INF for v in V}; pred = {v: None for v in V}
    dist[src] = 0
    for it in range(len(V) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w; pred[v] = u; changed = True
        if not changed:
            break
    # V-th pass: any further improvement means a reachable negative cycle
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None, None
    if verbose:
        for v in V:
            print(f"  {src}->{v}: dist={dist[v]}  path={' -> '.join(path_to(pred, v)) if dist[v] < INF else 'unreachable'}")
    return dist, pred


def floyd(edges):
    n = len(V); idx = {v: i for i, v in enumerate(V)}
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[idx[u]][idx[v]] = min(d[idx[u]][idx[v]], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def warshall(edges):
    n = len(V); idx = {v: i for i, v in enumerate(V)}
    r = [[i == j for j in range(n)] for i in range(n)]
    for u, v, _ in edges:
        r[idx[u]][idx[v]] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


def show_matrix(m, fmt):
    print("      " + " ".join(f"{v:>4}" for v in V))
    for i, row in enumerate(m):
        print(f"  {V[i]:>3} " + " ".join(f"{fmt(x):>4}" for x in row))


if __name__ == "__main__":
    print("STAGE A - Dijkstra on the normal network, source S")
    dijkstra(EDGES, "S")

    print("\nSTAGE B - introduce negative edge B->C = -2 (was +2)")
    print("PREDICTION: C is finalised (dist 3, via S->C) BEFORE B (dist 4). Dijkstra will never revisit C, so it will")
    print("miss the cheaper route S->B->C = 4-2 = 2, and everything reached through C (D, F, G) may be wrong.")
    neg = [(u, v, -2 if (u, v) == ("B", "C") else w) for u, v, w in EDGES]
    print("Dijkstra on modified graph:")
    dd, _ = dijkstra(neg, "S")
    print("Bellman-Ford on modified graph:")
    bd, _ = bellman_ford(neg, "S")
    wrong = [v for v in V if dd[v] != bd[v]]
    print("  Vertices where Dijkstra is WRONG:", wrong)
    for v in wrong:
        print(f"    {v}: Dijkstra={dd[v]}  correct(Bellman-Ford)={bd[v]}")

    print("\nSTAGE C - reachable negative cycle: add G->B = -10 (cycle B->E->G->B = 5+3-10 = -2)")
    cyc = neg + [("G", "B", -10)]
    d, _ = bellman_ford(cyc, "S", verbose=False)
    if d is None:
        print("  NEGATIVE CYCLE DETECTED - shortest paths are undefined, no distances returned.")
    print("  Detection: after V-1 = 7 relaxation passes all true shortest paths (<= 7 edges) are final; if an edge can")
    print("  STILL be relaxed in pass V, the improvement can only come from a cycle of negative total weight.")

    print("\nSTAGE D - all-pairs (original network)")
    print("Floyd distance matrix (INF = unreachable):")
    show_matrix(floyd(EDGES), lambda x: "INF" if x == INF else int(x))
    print("Warshall reachability matrix (1 = reachable):")
    show_matrix(warshall(EDGES), lambda x: 1 if x else 0)
    print("Interpretation: row S can reach every vertex; G reaches only itself (sink). Floyd gives cost, Warshall only yes/no.")
