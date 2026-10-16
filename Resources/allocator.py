"""Resource allocator: waiting queue and event log on top of Banker's Algorithm.

``deadlock.py`` decides whether a request is safe. This module decides what to
do with that answer: blocked requests wait in a FIFO queue, they are retried
whenever resources are freed, and every action is recorded in an event log.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from enum import Enum

from Resources.deadlock import BankersAlgorithm, RequestResult


class Action(str, Enum):
    """Event types written to the event log."""

    REGISTER = "REGISTER"
    TERMINATE = "TERMINATE"
    REQUEST = "REQUEST"
    RELEASE = "RELEASE"
    GRANT_FROM_WAIT = "GRANT_FROM_WAIT"


class ResourceAllocator:
    """Banker's Algorithm plus a waiting queue and an execution log."""

    def __init__(self, resource_names: list[str], total: list[int]) -> None:
        self.banker = BankersAlgorithm(resource_names, total)
        self.waiting: deque[tuple[str, list[int]]] = deque()
        self.events: list[dict] = []  # later persisted as execution logs in the DB

    # ------------------------------------------------------------------
    # Process lifecycle
    # ------------------------------------------------------------------
    def register_process(
        self,
        process_id: str,
        max_demand: list[int],
        allocation: list[int] | None = None,
    ) -> None:
        self.banker.add_process(process_id, max_demand, allocation)
        self._log(Action.REGISTER, process_id, max_demand, "OK", "Process registered")

    def terminate_process(self, process_id: str) -> list[RequestResult]:
        """Free a process's resources and grant any waiting requests that now fit."""
        self.waiting = deque(entry for entry in self.waiting if entry[0] != process_id)
        self.banker.remove_process(process_id)
        self._log(Action.TERMINATE, process_id, [], "OK", "Process terminated, resources freed")
        return self._retry_waiting()

    # ------------------------------------------------------------------
    # Request / release
    # ------------------------------------------------------------------
    def request(self, process_id: str, request: list[int]) -> RequestResult:
        """Ask for resources. Blocked requests are queued instead of dropped."""
        if self._is_waiting(process_id):
            result = RequestResult(
                process_id, request, "DENIED",
                "A request from this process is already waiting",
            )
        else:
            result = self.banker.request_resources(process_id, request)
            if result.status == "WAIT":
                self.waiting.append((process_id, list(request)))

        self._log(Action.REQUEST, process_id, request, result.status, result.reason)
        return result

    def release(self, process_id: str, release: list[int] | None = None) -> list[RequestResult]:
        """Release resources (all of them if ``release`` is None).

        Returns the waiting requests that were granted as a result.
        """
        released = self.banker.release_resources(process_id, release)
        self._log(Action.RELEASE, process_id, released, "OK", "Resources released")
        return self._retry_waiting()

    # ------------------------------------------------------------------
    # Status for the dashboard / API
    # ------------------------------------------------------------------
    def status(self) -> dict:
        data = self.banker.snapshot()
        data["waiting"] = [{"process_id": pid, "request": list(req)} for pid, req in self.waiting]
        return data

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _is_waiting(self, process_id: str) -> bool:
        return any(pid == process_id for pid, _ in self.waiting)

    def _retry_waiting(self) -> list[RequestResult]:
        """Keep granting waiting requests until none of them can proceed."""
        granted: list[RequestResult] = []
        while (result := self._grant_next_waiting()) is not None:
            granted.append(result)
        return granted

    def _grant_next_waiting(self) -> RequestResult | None:
        """Grant the first waiting request (FIFO order) that is now safe, if any."""
        for entry in self.waiting:
            process_id, request = entry
            result = self.banker.request_resources(process_id, request)
            if result.granted:
                self.waiting.remove(entry)
                self._log(Action.GRANT_FROM_WAIT, process_id, request, result.status, result.reason)
                return result
        return None

    def _log(self, action: Action, process_id: str, vector: list[int], status: str, reason: str) -> None:
        self.events.append(
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "action": action.value,
                "process_id": process_id,
                "vector": list(vector),
                "status": status,
                "reason": reason,
                "available_after": list(self.banker.available),
            }
        )