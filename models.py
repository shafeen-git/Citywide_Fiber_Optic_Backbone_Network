"""
Domain entities and data classes for Citywide Fiber-Optic Backbone Network.
"""
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Hub:
    id: str
    name: str
    category: str  # 'DataCenter', 'Hospital', 'Civic', 'Commercial', 'Telecom'


@dataclass
class CandidateEdge:
    u: str
    v: str
    trenching_cost: float       # Cost in thousands of USD ($k)
    latency_ms: float           # Direct propagation latency (ms)
    capacity_gbps: float        # Optical duct bandwidth (Gbps)
    sla_credit_weight: Optional[float] = None  # Mixed-sign metric for Bellman-Ford


@dataclass
class RedundancyUpgrade:
    id: str
    source: str
    target: str
    cost: int                   # Integer cost in thousands ($k)
    resilience_gain: int        # Structural risk-reduction score (1 - 100)
    description: str


@dataclass
class MaintenanceTask:
    task_id: str
    link: Tuple[str, str]
    start_hour: float           # e.g., 1.5 = 01:30 AM
    end_hour: float             # e.g., 3.5 = 03:30 AM
    required_crew: str