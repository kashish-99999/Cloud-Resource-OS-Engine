"""Page replacement algorithms used by the virtual-memory simulator."""

from __future__ import annotations

from collections import deque
from typing import Sequence


def _validate(reference_string: Sequence[int], frame_count: int) -> None:
    if frame_count <= 0:
        raise ValueError("frame_count must be greater than zero")
    if any(page < 0 for page in reference_string):
        raise ValueError("page numbers must be non-negative")


def fifo(reference_string: Sequence[int], frame_count: int) -> dict[str, object]:
    """Simulate first-in, first-out replacement."""
    _validate(reference_string, frame_count)
    frames: list[int] = []
    queue: deque[int] = deque()
    faults = 0
    trace: list[dict[str, object]] = []

    for page in reference_string:
        hit = page in frames
        if not hit:
            faults += 1
            if len(frames) == frame_count:
                evicted = queue.popleft()
                frames[frames.index(evicted)] = page
            else:
                frames.append(page)
            queue.append(page)
        trace.append({"page": page, "hit": hit, "frames": frames.copy()})

    return {"algorithm": "FIFO", "faults": faults, "hits": len(reference_string) - faults, "trace": trace}


def lru(reference_string: Sequence[int], frame_count: int) -> dict[str, object]:
    """Simulate least-recently-used replacement."""
    _validate(reference_string, frame_count)
    frames: list[int] = []
    faults = 0
    trace: list[dict[str, object]] = []

    for page in reference_string:
        hit = page in frames
        if hit:
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            if len(frames) == frame_count:
                frames.pop(0)
            frames.append(page)
        trace.append({"page": page, "hit": hit, "frames": frames.copy()})

    return {"algorithm": "LRU", "faults": faults, "hits": len(reference_string) - faults, "trace": trace}


def optimal(reference_string: Sequence[int], frame_count: int) -> dict[str, object]:
    """Simulate replacement of the page used farthest in the future."""
    _validate(reference_string, frame_count)
    frames: list[int] = []
    faults = 0
    trace: list[dict[str, object]] = []

    for index, page in enumerate(reference_string):
        hit = page in frames
        if not hit:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                future = reference_string[index + 1 :]
                victim = max(
                    frames,
                    key=lambda candidate: future.index(candidate)
                    if candidate in future
                    else len(future),
                )
                frames[frames.index(victim)] = page
        trace.append({"page": page, "hit": hit, "frames": frames.copy()})

    return {"algorithm": "Optimal", "faults": faults, "hits": len(reference_string) - faults, "trace": trace}


ALGORITHMS = {"FIFO": fifo, "LRU": lru, "Optimal": optimal}
