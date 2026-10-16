"""Resource Allocation Graph and deadlock status (data for the dashboard).

This module only reads the allocator's state and never modifies it.
Banker's Algorithm *avoids* deadlock; here we additionally *verify* that with
a detection algorithm and build the graph data the dashboard draws.
"""

from __future__ import annotations

from enum import Enum

from Resources.allocator import ResourceAllocator


class EdgeType(str, Enum):
    """Edge kinds in the Resource Allocation Graph."""

    ASSIGNMENT = "assignment"  # resource -> process: the process holds it
    REQUEST = "request"        # process -> resource: the process is waiting for it
    CLAIM = "claim"            # process -> resource: remaining future need


def _fits(vector: list[int], limit: list[int]) -> bool:
    """True if every entry of ``vector`` is <= the matching entry of ``limit``."""
    return all(v <= m for v, m in zip(vector, limit))


def _edge(source: str, target: str, kind: EdgeType, count: int) -> dict:
    return {"from": source, "to": target, "type": kind.value, "count": count}


class ResourceGraph:
    """Read-only view of an allocator as a graph plus deadlock diagnostics."""

    def __init__(self, allocator: ResourceAllocator) -> None:
        self.allocator = allocator

    @property
    def _banker(self):
        return self.allocator.banker

    # ------------------------------------------------------------------
    # Resource Allocation Graph (nodes + edges)
    # ------------------------------------------------------------------
    def build_graph(self, include_claims: bool = False) -> dict:
        """Return ``{"nodes": [...], "edges": [...]}`` for the dashboard."""
        edges = self._assignment_edges() + self._request_edges()
        if include_claims:
            edges += self._claim_edges()
        return {"nodes": self._nodes(), "edges": edges}

    def _nodes(self) -> list[dict]:
        banker = self._banker
        nodes = [{"id": pid, "type": "process"} for pid in banker.max_demand]
        nodes += [
            {
                "id": name,
                "type": "resource",
                "total": banker.total[i],
                "available": banker.available[i],
            }
            for i, name in enumerate(banker.resource_names)
        ]
        return nodes

    def _assignment_edges(self) -> list[dict]:
        banker = self._banker
        return [
            _edge(name, pid, EdgeType.ASSIGNMENT, banker.allocation[pid][i])
            for pid in banker.max_demand
            for i, name in enumerate(banker.resource_names)
            if banker.allocation[pid][i] > 0
        ]

    def _request_edges(self) -> list[dict]:
        names = self._banker.resource_names
        return [
            _edge(pid, name, EdgeType.REQUEST, request[i])
            for pid, request in self.allocator.waiting
            for i, name in enumerate(names)
            if request[i] > 0
        ]

    def _claim_edges(self) -> list[dict]:
        banker = self._banker
        edges = []
        for pid in banker.max_demand:
            need = banker.need(pid)
            edges += [
                _edge(pid, name, EdgeType.CLAIM, need[i])
                for i, name in enumerate(banker.resource_names)
                if need[i] > 0
            ]
        return edges

    # ------------------------------------------------------------------
    # Wait-for graph: Pi -> Pj means Pi waits for a resource that Pj holds
    # ------------------------------------------------------------------
    def wait_for_graph(self) -> list[dict]:
        banker = self._banker
        edges: list[dict] = []
        for pid, request in self.allocator.waiting:
            for i, name in enumerate(banker.resource_names):
                if request[i] <= banker.available[i]:
                    continue  # enough instances are free, so nobody is blocking this
                edges += [
                    {"from": pid, "to": holder, "resource": name}
                    for holder in banker.max_demand
                    if holder != pid and banker.allocation[holder][i] > 0
                ]
        return edges

    # ------------------------------------------------------------------
    # Deadlock detection (multiple instances per resource type)
    # ------------------------------------------------------------------
    def detect_deadlock(self) -> list[str]:
        """Return the processes that can never finish (empty list = no deadlock)."""
        banker = self._banker
        no_request = [0] * len(banker.resource_names)
        pending = {pid: list(request) for pid, request in self.allocator.waiting}

        work = list(banker.available)
        finished = {pid: not any(banker.allocation[pid]) for pid in banker.max_demand}

        progress = True
        while progress:
            progress = False
            for pid in banker.max_demand:
                if finished[pid] or not _fits(pending.get(pid, no_request), work):
                    continue
                work = [w + a for w, a in zip(work, banker.allocation[pid])]
                finished[pid] = True
                progress = True

        return [pid for pid, done in finished.items() if not done]

    # ------------------------------------------------------------------
    # Combined status for the dashboard
    # ------------------------------------------------------------------
    def deadlock_status(self) -> dict:
        safety = self._banker.is_safe()
        deadlocked = self.detect_deadlock()
        return {
            "state_safe": safety.is_safe,
            "safe_sequence": safety.safe_sequence,
            "deadlock_detected": bool(deadlocked),
            "deadlocked_processes": deadlocked,
            "waiting_processes": [pid for pid, _ in self.allocator.waiting],
            "wait_for_edges": self.wait_for_graph(),
        }