"""
Pipeline Orchestrator: Bridges the three operational phases of the fiber network.
"""
from typing import Dict, List, Tuple
from models import Hub, CandidateEdge, RedundancyUpgrade, MaintenanceTask
from algorithms.topology import kruskal_mst
from algorithms.knapsack import allocate_redundancy_budget
from algorithms.routing import dijkstra_shortest_path, bellman_ford_sla_routing
from algorithms.resilience import (
    find_critical_failures_tarjan,
    bfs_connectivity,
    EdmondsKarpMaxFlow,
)
from algorithms.scheduling import schedule_maintenance_windows


class CityFiberBackbonePipeline:
    def __init__(
        self,
        hubs: List[Hub],
        candidate_edges: List[CandidateEdge],
        upgrades: List[RedundancyUpgrade],
        maintenance_tasks: List[MaintenanceTask],
        upgrade_budget: int,
    ):
        self.hubs = hubs
        self.hub_ids = [h.id for h in hubs]
        self.candidate_edges = candidate_edges
        self.upgrades = upgrades
        self.maintenance_tasks = maintenance_tasks
        self.upgrade_budget = upgrade_budget

        self.mst_edges: List[CandidateEdge] = []
        self.funded_upgrades: List[RedundancyUpgrade] = []
        self.active_edges: List[CandidateEdge] = []

    def run_phase_1_offline_design(self) -> Dict:
        mst, mst_cost = kruskal_mst(self.hub_ids, self.candidate_edges)
        self.mst_edges = mst

        funded, score, spent = allocate_redundancy_budget(self.upgrades, self.upgrade_budget)
        self.funded_upgrades = funded

        self.active_edges = list(self.mst_edges)
        for upg in self.funded_upgrades:
            matching = [
                e for e in self.candidate_edges
                if (e.u == upg.source and e.v == upg.target) or (e.v == upg.source and e.u == upg.target)
            ]
            if matching and matching[0] not in self.active_edges:
                self.active_edges.append(matching[0])

        return {
            "mst_links_count": len(mst),
            "mst_trenching_cost": mst_cost,
            "funded_upgrades": [u.id for u in funded],
            "resilience_score": score,
            "budget_spent": spent,
            "active_links_count": len(self.active_edges),
        }

    def _build_graph_views(self):
        latency_graph = {h: [] for h in self.hub_ids}
        adj = {h: [] for h in self.hub_ids}
        flow_net = EdmondsKarpMaxFlow(self.hub_ids)

        for e in self.active_edges:
            latency_graph[e.u].append((edge_v := e.v, e.latency_ms))
            latency_graph[e.v].append((e.u, e.latency_ms))
            adj[e.u].append(e.v)
            adj[e.v].append(e.u)
            flow_net.add_edge(e.u, e.v, e.capacity_gbps)
            flow_net.add_edge(e.v, e.u, e.capacity_gbps)

        return latency_graph, adj, flow_net

    def run_phase_2_online_routing(self, source: str, target: str) -> Dict:
        lat_graph, _, _ = self._build_graph_views()
        path, latency = dijkstra_shortest_path(lat_graph, source, target)

        directed_edges = []
        for e in self.active_edges:
            w = e.sla_credit_weight if e.sla_credit_weight is not None else e.latency_ms
            directed_edges.append((e.u, e.v, w))
            directed_edges.append((e.v, e.u, w))

        bf_dist, _, has_neg_cycle = bellman_ford_sla_routing(self.hub_ids, directed_edges, source)

        return {
            "primary_path": path,
            "primary_latency_ms": latency,
            "sla_cost_to_target": bf_dist.get(target, float("inf")),
            "arbitrage_cycle_detected": has_neg_cycle,
        }

    def run_phase_3_contingency(self, cut_link: Tuple[str, str], src: str, dst: str) -> Dict:
        lat_graph, adj, flow_net = self._build_graph_views()
        bridges, cut_vertices = find_critical_failures_tarjan(self.hub_ids, adj)
        max_flow_before = flow_net.compute_max_flow(src, dst)

        u_cut, v_cut = cut_link
        self.active_edges = [
            e for e in self.active_edges
            if not ((e.u == u_cut and e.v == v_cut) or (e.u == v_cut and e.v == u_cut))
        ]

        post_lat, post_adj, post_flow = self._build_graph_views()
        reachable = bfs_connectivity(self.hub_ids, post_adj, src)
        is_partitioned = len(reachable) < len(self.hub_ids)

        rerouted_path, rerouted_lat = dijkstra_shortest_path(post_lat, src, dst)
        max_flow_after = post_flow.compute_max_flow(src, dst)

        tasks = schedule_maintenance_windows(self.maintenance_tasks)

        return {
            "initial_bridges": bridges,
            "initial_cut_vertices": cut_vertices,
            "max_flow_pre_cut": max_flow_before,
            "cut_simulated": f"{u_cut} <---> {v_cut}",
            "is_partitioned": is_partitioned,
            "rerouted_path": rerouted_path,
            "rerouted_latency_ms": rerouted_lat,
            "max_flow_post_cut": max_flow_after,
            "scheduled_maintenance_tasks": [t.task_id for t in tasks],
        }