"""
Algorithms 5 & 6: Tarjan's Bridge/Cut-Vertex DFS & Edmonds-Karp Max-Flow.
Tarjan's: Discovers single points of failure in O(V + E).
Edmonds-Karp: Verifies point-to-point bandwidth capacity via BFS in O(V * E^2).
"""
from collections import deque
from typing import Dict, List, Set, Tuple, Optional


def find_critical_failures_tarjan(
    nodes: List[str], adj: Dict[str, List[str]]
) -> Tuple[List[Tuple[str, str]], List[str]]:
    discovery_time: Dict[str, int] = {}
    low: Dict[str, int] = {}
    parent: Dict[str, Optional[str]] = {node: None for node in nodes}
    visited: Set[str] = set()

    bridges: List[Tuple[str, str]] = []
    cut_vertices: Set[str] = set()
    timer = 0

    def dfs(u: str):
        nonlocal timer
        visited.add(u)
        discovery_time[u] = low[u] = timer
        timer += 1
        children = 0

        for v in adj.get(u, []):
            if v == parent[u]:
                continue
            if v in visited:
                low[u] = min(low[u], discovery_time[v])
            else:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])

                if parent[u] is None and children > 1:
                    cut_vertices.add(u)
                if parent[u] is not None and low[v] >= discovery_time[u]:
                    cut_vertices.add(u)

                if low[v] > discovery_time[u]:
                    bridges.append((u, v))

    for node in nodes:
        if node not in visited:
            dfs(node)

    return bridges, sorted(list(cut_vertices))


def bfs_connectivity(nodes: List[str], adj: Dict[str, List[str]], start: str) -> Set[str]:
    visited = {start}
    q = deque([start])
    while q:
        curr = q.popleft()
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return visited


class EdmondsKarpMaxFlow:
    def __init__(self, nodes: List[str]):
        self.nodes = nodes
        self.capacity: Dict[str, Dict[str, float]] = {u: {} for u in nodes}
        self.adj: Dict[str, List[str]] = {u: [] for u in nodes}

    def add_edge(self, u: str, v: str, cap: float):
        self.capacity[u][v] = self.capacity[u].get(v, 0.0) + cap
        self.capacity[v][u] = self.capacity[v].get(u, 0.0)
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def _bfs_augmenting_path(self, source: str, sink: str, parent: Dict[str, str]) -> float:
        visited = {source}
        q = deque([(source, float("inf"))])

        while q:
            curr, flow = q.popleft()
            for neighbor in self.adj[curr]:
                residual = self.capacity[curr][neighbor]
                if neighbor not in visited and residual > 1e-9:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    new_flow = min(flow, residual)
                    if neighbor == sink:
                        return new_flow
                    q.append((neighbor, new_flow))
        return 0.0

    def compute_max_flow(self, source: str, sink: str) -> float:
        total_flow = 0.0
        parent: Dict[str, str] = {}

        while True:
            parent.clear()
            pushed_flow = self._bfs_augmenting_path(source, sink, parent)
            if pushed_flow <= 1e-9:
                break
            total_flow += pushed_flow

            curr = sink
            while curr != source:
                p = parent[curr]
                self.capacity[p][curr] -= pushed_flow
                self.capacity[curr][p] += pushed_flow
                curr = p

        return total_flow