"""Graph processing: Dijkstra + Nearest-Neighbour TSP approximation."""
import heapq


def build_graph(edges):
    """edges: iterable of (u, v, weight). Returns an undirected adjacency list."""
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, {})[v] = w
        graph.setdefault(v, {})[u] = w
    return graph


def dijkstra(graph, source):
    """Return (dist, prev) from source. Non-negative weights, O((V+E) log V)."""
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                      # stale heap entry
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def get_path(prev, target):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]


def nearest_neighbour_route(graph, depot, stops):
    """Greedy TSP approximation using Dijkstra distances.

    Returns (order, total_distance, full_path) where order is
    depot -> stops... -> depot and full_path expands every leg
    through intermediate nodes. Time: (k+1) Dijkstra runs + O(k^2).
    """
    stops = list(dict.fromkeys(s for s in stops if s != depot))
    sp = {n: dijkstra(graph, n) for n in [depot] + stops}   # all-pairs among stops

    order, total, full_path = [depot], 0, [depot]
    current, remaining = depot, set(stops)
    while remaining:
        nxt = min(remaining, key=lambda s: sp[current][0][s])
        total += sp[current][0][nxt]
        full_path += get_path(sp[current][1], nxt)[1:]
        order.append(nxt)
        remaining.remove(nxt)
        current = nxt
    total += sp[current][0][depot]
    full_path += get_path(sp[current][1], depot)[1:]
    order.append(depot)
    return order, total, full_path
