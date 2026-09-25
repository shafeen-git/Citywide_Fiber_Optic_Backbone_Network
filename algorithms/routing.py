"""
Algorithms 3 & 4: Dijkstra's Algorithm (Min-Heap) and Bellman-Ford Algorithm.
Dijkstra: Computes the path with minimum end-to-end latency in O((V + E) log V).
Bellman-Ford: Handles mixed-sign SLA credit pricing and detects arbitrage cycles in O(V * E).
"""
import heapq
from typing import Dict, List, Optional, Tuple


def dijkstra_shortest_path(
    graph: Dict[str, List[Tuple[str, float]]], source: str, target: str
) -> Tuple[Optional[List[str]], float]:
    distances: Dict[str, float] = {node: float("inf") for node in graph}
    parent: Dict[str, Optional[str]] = {node: None for node in graph}
    distances[source] = 0.0

    pq = [(0.0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances[u]:
            continue
        if u == target:
            break

        for v, weight in graph.get(u, []):
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))

    if distances[target] == float("inf"):
        return None, float("inf")

    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path, distances[target]


def bellman_ford_sla_routing(
    nodes: List[str],
    edges: List[Tuple[str, str, float]],
    source: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool]:
    dist = {node: float("inf") for node in nodes}
    pred: Dict[str, Optional[str]] = {node: None for node in nodes}
    dist[source] = 0.0
    num_vertices = len(nodes)

    for _ in range(num_vertices - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != float("inf") and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
                updated = True
        if not updated:
            break

    # Negative cycle detection pass
    has_negative_cycle = False
    for u, v, weight in edges:
        if dist[u] != float("inf") and dist[u] + weight < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle