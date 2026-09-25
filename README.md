# 🌐 Citywide Fiber-Optic Backbone Network Design & Resilient Routing Engine

> **CSE 4403: Algorithms Final Term Project**  
> An end-to-end multi-phase algorithmic pipeline solving metropolitan infrastructure topology, real-time routing, fault resilience, and scheduled maintenance.

**Team:** Shafeen Sufian Meead (230041206) · Adef Mahamat (230041219) · Abrar Naguib (230041229)

---

## 📌 Problem Overview

Urban optical fiber backbones must balance high trenching capital expenditures, low end-to-end latency, fault tolerance against physical severing (e.g., construction cuts), and contractual peering SLA credits. 

This engine orchestrates a suite of 7 classical algorithms divided across three pipeline stages:
1. **Phase 1: Offline Topology Design & Capital Allocation** (Kruskal's MST + 0/1 Knapsack DP)
2. **Phase 2: Online Shortest-Path & SLA Credit Verification** (Dijkstra + Bellman-Ford)
3. **Phase 3: Contingency Simulation, Max-Flow Capacity & Scheduling** (Tarjan's DFS + Edmonds-Karp Max-Flow + Greedy Activity Selection)

---

## ✨ Key Features

* **Zero Third-Party Dependencies:** Implemented strictly using the Python 3 standard library (`heapq`, `collections.deque`, `dataclasses`, `typing`, `unittest`).
* **Multi-Phase Algorithmic Pipeline:** Seamlessly connects offline topology generation, online traffic routing, SLA pricing checks, fault contingency, and maintenance scheduling.
* **Resilience & Cut-Contingency Simulation:** Proactively audits network cut-vertices and bridges via Tarjan's DFS and benchmarks maximum flow capacity before and after catastrophic link cuts.
* **Peering SLA Arbitrage Verification:** Employs Bellman-Ford to ensure negative edge costs (carrier peering rebates) do not produce arbitrage feedback loops.
* **Automated Test Coverage:** Includes unit testing across all 7 discrete algorithmic modules.

---

## 🧠 Algorithmic Suite & Complexity

| Phase | Pipeline Component | Algorithm | Purpose | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Primary Grid Foundation | **Kruskal's Algorithm (with DSU)** | Minimum trenching capital expenditure | $\mathcal{O}(E \log E)$ | $\mathcal{O}(V + E)$ |
| **Phase 1** | Resilience Budgeting | **0/1 Knapsack Dynamic Programming** | Optimal structural upgrade selection under budget $W$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ |
| **Phase 2** | Primary Packet Routing | **Dijkstra's Algorithm (Min-Heap)** | Lowest propagation delay path selection | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V + E)$ |
| **Phase 2** | Peering Credit Accounting | **Bellman-Ford Algorithm** | Negative edge weights & peering arbitrage loop detection | $\mathcal{O}(V \cdot E)$ | $\mathcal{O}(V)$ |
| **Phase 3** | Single-Point-of-Failure Audit | **Tarjan's Cut-Vertex & Bridge DFS** | Proactive structural vulnerability identification | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ |
| **Phase 3** | Critical Bandwidth Auditing | **Edmonds-Karp Max-Flow (BFS)** | End-to-end optical throughput verification | $\mathcal{O}(V \cdot E^2)$ | $\mathcal{O}(V + E)$ |
| **Phase 3** | Repair Window Planning | **Greedy Activity Scheduling** | Maximum conflict-free maintenance operations | $\mathcal{O}(M \log M)$ | $\mathcal{O}(M)$ |

---

## 📐 Mathematical Recurrences

### 1. 0/1 Knapsack Structural Upgrade DP
Let $dp[i][w]$ represent the maximum resilience gain attainable using a subset of the first $i$ upgrades within cost budget $w$:

$$dp[i][w] = \begin{cases}  dp[i-1][w] & \text{if } \text{cost}[i] > w \\  \max\left(dp[i-1][w],\; dp[i-1][w - \text{cost}[i]] + \text{gain}[i]\right) & \text{if } \text{cost}[i] \le w  \end{cases}$$

### 2. Peering Credit Path Relaxation (Bellman-Ford)
For each directed fiber edge $(u, v) \in E$ across $\vert{}V\vert{} - 1$ passes:

$$\text{dist}^{(k)}[v] = \min\left(\text{dist}^{(k-1)}[v],\; \text{dist}^{(k-1)}[u] + \text{weight}(u, v)\right)$$

If $\text{dist}[u] + \text{weight}(u, v) < \text{dist}[v]$ holds on pass $\vert{}V\vert{}$, an arbitrage/negative cycle is reported.

---

## ⚙️ Environment & Tech Stack

* **Language:** Python 3.10+ (Standard Library only)
* **External Dependencies:** None (Zero external packages required)
* **Environment Variables:** None; all network topologies, link capacities, and maintenance schedules run out-of-the-box with no `.env` or system configurations.

---

## 🚀 Running it

```bash
# Clone the repository
git clone [https://github.com/shafeen-git/Citywide_Fiber_Optic_Backbone_Network.git](https://github.com/shafeen-git/Citywide_Fiber_Optic_Backbone_Network.git)
cd Citywide_Fiber_Optic_Backbone_Network

# Run full metropolitan pipeline simulation
python main.py

# Run the automated unit test suite
python -m unittest discover tests


## Project Structure

Citywide_Fiber_Optic_Backbone_Network/
├── algorithms/
│   ├── __init__.py
│   ├── knapsack.py       # 0/1 Knapsack DP capital allocation
│   ├── resilience.py     # Tarjan's DFS and Edmonds-Karp max flow
│   ├── routing.py        # Dijkstra (Min-Heap) and Bellman-Ford
│   ├── scheduling.py     # Greedy interval activity selection
│   └── topology.py       # Kruskal's MST with Disjoint Set Union
├── tests/
│   ├── __init__.py
│   └── test_algorithms.py # Unit test coverage across all 7 algorithms
├── models.py             # Data entities (Hub, CandidateEdge, Upgrades, Tasks)
├── pipeline.py           # 3-Phase operational orchestrator
├── main.py               # Metropolitan case study execution driver
├── .gitignore
└── README.md