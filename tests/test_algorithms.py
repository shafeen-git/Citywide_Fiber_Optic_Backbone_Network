"""
Unit Test Suite for Verification of Algorithmic Modules.
Execute via: python -m unittest discover tests
"""
import unittest
from models import CandidateEdge, RedundancyUpgrade, MaintenanceTask
from algorithms.topology import kruskal_mst
from algorithms.knapsack import allocate_redundancy_budget
from algorithms.routing import dijkstra_shortest_path, bellman_ford_sla_routing
from algorithms.resilience import (
    find_critical_failures_tarjan,
    bfs_connectivity,
    EdmondsKarpMaxFlow,
)
from algorithms.scheduling import schedule_maintenance_windows


class TestFiberBackbonePipeline(unittest.TestCase):

    def test_kruskal_mst(self):
        nodes = ["H1", "H2", "H3"]
        edges = [
            CandidateEdge("H1", "H2", trenching_cost=10, latency_ms=1.0, capacity_gbps=10),
            CandidateEdge("H2", "H3", trenching_cost=20, latency_ms=1.0, capacity_gbps=10),
            CandidateEdge("H1", "H3", trenching_cost=40, latency_ms=1.0, capacity_gbps=10),
        ]
        mst, cost = kruskal_mst(nodes, edges)
        self.assertEqual(len(mst), 2)
        self.assertEqual(cost, 30.0)

    def test_knapsack_optimality(self):
        items = [
            RedundancyUpgrade("U1", "A", "B", cost=10, resilience_gain=60, description=""),
            RedundancyUpgrade("U2", "B", "C", cost=20, resilience_gain=100, description=""),
            RedundancyUpgrade("U3", "C", "D", cost=30, resilience_gain=120, description=""),
        ]
        selected, gain, spent = allocate_redundancy_budget(items, budget=50)
        self.assertEqual(gain, 220)
        self.assertEqual(spent, 50)
        self.assertEqual(len(selected), 2)

    def test_dijkstra_shortest_path(self):
        graph = {
            "A": [("B", 1.0), ("C", 4.0)],
            "B": [("C", 2.0), ("D", 6.0)],
            "C": [("D", 1.0)],
            "D": [],
        }
        path, latency = dijkstra_shortest_path(graph, "A", "D")
        self.assertEqual(path, ["A", "B", "C", "D"])
        self.assertEqual(latency, 4.0)

    def test_bellman_ford_arbitrage_cycle(self):
        nodes = ["A", "B", "C"]
        edges = [("A", "B", 1.0), ("B", "C", -5.0), ("C", "A", 2.0)]
        _, _, has_cycle = bellman_ford_sla_routing(nodes, edges, "A")
        self.assertTrue(has_cycle)

    def test_tarjan_bridges_and_articulation(self):
        nodes = ["A", "B", "C"]
        adj = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}
        bridges, cut_nodes = find_critical_failures_tarjan(nodes, adj)
        self.assertEqual(len(bridges), 2)
        self.assertIn("B", cut_nodes)

    def test_edmonds_karp_max_flow(self):
        net = EdmondsKarpMaxFlow(["S", "U", "V", "T"])
        net.add_edge("S", "U", 10)
        net.add_edge("S", "V", 10)
        net.add_edge("U", "V", 2)
        net.add_edge("U", "T", 10)
        net.add_edge("V", "T", 10)
        flow = net.compute_max_flow("S", "T")
        self.assertEqual(flow, 20.0)

    def test_greedy_scheduling_optimal_count(self):
        tasks = [
            MaintenanceTask("T1", ("A", "B"), 1.0, 3.0, "Alpha"),
            MaintenanceTask("T2", ("B", "C"), 2.0, 5.0, "Beta"),
            MaintenanceTask("T3", ("C", "D"), 3.5, 6.0, "Alpha"),
        ]
        res = schedule_maintenance_windows(tasks)
        self.assertEqual(len(res), 2)
        self.assertEqual([t.task_id for t in res], ["T1", "T3"])


if __name__ == "__main__":
    unittest.main()