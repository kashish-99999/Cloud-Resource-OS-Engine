"""Banker's Algorithm for deadlock avoidance (Resources module).

"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SafetyResult:
    """Safety Algorithm ka output (dashboard ke liye trace ke saath)."""

    is_safe: bool
    safe_sequence: list[str] = field(default_factory=list)
    steps: list[dict] = field(default_factory=list)


@dataclass
class RequestResult:
    """Resource-Request Algorithm ka output."""

    process_id: str
    request: list[int]
    status: str  # "GRANTED" | "WAIT" | "DENIED"
    reason: str
    safety: SafetyResult | None = None

    @property
    def granted(self) -> bool:
        return self.status == "GRANTED"


class BankersAlgorithm:
    def __init__(self, resource_names: list[str], total: list[int]) -> None:
        if len(resource_names) != len(total):
            raise ValueError("resource_names aur total ki length same honi chahiye")
        if any(t < 0 for t in total):
            raise ValueError("total instances negative nahi ho sakte")
        self.resource_names = list(resource_names)
        self.total = list(total)
        self.available = list(total)
        self.max_demand: dict[str, list[int]] = {}
        self.allocation: dict[str, list[int]] = {}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _check_vector(self, vector: list[int], label: str) -> None:
        if len(vector) != len(self.resource_names):
            raise ValueError(f"{label} mein {len(self.resource_names)} values honi chahiye")
        if any(v < 0 for v in vector):
            raise ValueError(f"{label} negative nahi ho sakta")

    @staticmethod
    def _leq(a: list[int], b: list[int]) -> bool:
        return all(x <= y for x, y in zip(a, b))

    def need(self, process_id: str) -> list[int]:
        """Need = Max - Allocation."""
        return [m - a for m, a in zip(self.max_demand[process_id], self.allocation[process_id])]

    # ------------------------------------------------------------------
    # Process registration
    # ------------------------------------------------------------------
    def add_process(
        self,
        process_id: str,
        max_demand: list[int],
        allocation: list[int] | None = None,
    ) -> None:
        if process_id in self.max_demand:
            raise ValueError(f"{process_id} already registered hai")
        allocation = allocation or [0] * len(self.resource_names)
        self._check_vector(max_demand, "max_demand")
        self._check_vector(allocation, "allocation")
        if not self._leq(max_demand, self.total):
            raise ValueError("max_demand system ke total resources se zyada hai")
        if not self._leq(allocation, max_demand):
            raise ValueError("allocation max_demand se zyada nahi ho sakti")
        if not self._leq(allocation, self.available):
            raise ValueError("itne resources available nahi hain")

        self.max_demand[process_id] = list(max_demand)
        self.allocation[process_id] = list(allocation)
        self.available = [av - al for av, al in zip(self.available, allocation)]

    def remove_process(self, process_id: str) -> None:
        """Process terminate hone par uske saare resources wapas available."""
        if process_id not in self.max_demand:
            raise KeyError(process_id)
        self.available = [av + al for av, al in zip(self.available, self.allocation[process_id])]
        del self.max_demand[process_id]
        del self.allocation[process_id]

    # ------------------------------------------------------------------
    # Safety Algorithm
    # ------------------------------------------------------------------
    def is_safe(self) -> SafetyResult:
        work = list(self.available)
        finished = {pid: False for pid in self.max_demand}
        sequence: list[str] = []
        steps: list[dict] = []

        progress = True
        while progress:
            progress = False
            for pid in self.max_demand:
                if finished[pid]:
                    continue
                need = self.need(pid)
                if self._leq(need, work):
                    steps.append({"process": pid, "need": need, "work_before": list(work)})
                    work = [w + a for w, a in zip(work, self.allocation[pid])]
                    steps[-1]["work_after"] = list(work)
                    finished[pid] = True
                    sequence.append(pid)
                    progress = True

        safe = all(finished.values())
        return SafetyResult(
            is_safe=safe,
            safe_sequence=sequence if safe else [],
            steps=steps,
        )

    # ------------------------------------------------------------------
    # Resource-Request Algorithm
    # ------------------------------------------------------------------
    def request_resources(self, process_id: str, request: list[int]) -> RequestResult:
        if process_id not in self.max_demand:
            raise KeyError(f"{process_id} registered nahi hai")
        self._check_vector(request, "request")

        # Step 1: request <= Need?
        if not self._leq(request, self.need(process_id)):
            return RequestResult(
                process_id, request, "DENIED",
                "Request process ki declared max claim (Need) se zyada hai",
            )

        # Step 2: request <= Available?
        if not self._leq(request, self.available):
            return RequestResult(
                process_id, request, "WAIT",
                "Resources abhi available nahi hain, process wait karega",
            )

        # Step 3: pretend allocation, phir safety check
        self.available = [av - r for av, r in zip(self.available, request)]
        self.allocation[process_id] = [a + r for a, r in zip(self.allocation[process_id], request)]

        safety = self.is_safe()
        if safety.is_safe:
            return RequestResult(
                process_id, request, "GRANTED",
                "Allocation ke baad system safe state mein hai", safety,
            )

        # Unsafe: rollback
        self.available = [av + r for av, r in zip(self.available, request)]
        self.allocation[process_id] = [a - r for a, r in zip(self.allocation[process_id], request)]
        return RequestResult(
            process_id, request, "WAIT",
            "Grant karne se system unsafe ho jaata, isliye request wait par hai", safety,
        )

    # ------------------------------------------------------------------
    # Release
    # ------------------------------------------------------------------
    def release_resources(self, process_id: str, release: list[int] | None = None) -> list[int]:
        """Resources wapas karo. release=None ka matlab sab kuch release."""
        if process_id not in self.max_demand:
            raise KeyError(f"{process_id} registered nahi hai")
        release = list(release) if release is not None else list(self.allocation[process_id])
        self._check_vector(release, "release")
        if not self._leq(release, self.allocation[process_id]):
            raise ValueError("jitna allocated hai usse zyada release nahi ho sakta")

        self.allocation[process_id] = [a - r for a, r in zip(self.allocation[process_id], release)]
        self.available = [av + r for av, r in zip(self.available, release)]
        return release

    # ------------------------------------------------------------------
    # Dashboard 
    # ------------------------------------------------------------------
    def snapshot(self) -> dict:
        safety = self.is_safe()
        return {
            "resources": self.resource_names,
            "total": list(self.total),
            "available": list(self.available),
            "processes": {
                pid: {
                    "max": list(self.max_demand[pid]),
                    "allocation": list(self.allocation[pid]),
                    "need": self.need(pid),
                }
                for pid in self.max_demand
            },
            "is_safe": safety.is_safe,
            "safe_sequence": safety.safe_sequence,
        }