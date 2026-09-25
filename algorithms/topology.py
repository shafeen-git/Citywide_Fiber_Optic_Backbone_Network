"""
Phase 1: Minimum Spanning Tree via Kruskal's Algorithm with DSU.
Solves the minimal trenching cost problem across municipal district hubs.
Complexity: O(E log E)
"""
from typing import List, Tuple
from models import CandidateEdge


class DisjointSetUnion:
    def __init__(self, elements: List[str]):
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}

    def find(self, item: str) -> str:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, item1: str, item2: str) -> bool:
        root1 = self.find(item1)
        root2 = self.find(item2)
        if root1 == root2:
            return False
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        return True


def kruskal_mst(hubs: List[str], candidate_edges: List[CandidateEdge]) -> Tuple[List[CandidateEdge], float]:
    sorted_edges = sorted(candidate_edges, key=lambda e: e.trenching_cost)
    dsu = DisjointSetUnion(hubs)
    mst: List[CandidateEdge] = []
    total_cost = 0.0

    for edge in sorted_edges:
        if dsu.union(edge.u, edge.v):
            mst.append(edge)
            total_cost += edge.trenching_cost
            if len(mst) == len(hubs) - 1:
                break

    if len(mst) != len(hubs) - 1:
        raise ValueError("Network graph is disconnected; MST cannot be formed.")

    return mst, total_cost