"""Virtual-memory manager with paging, TLB analytics, and replacement support."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Sequence

from .paging import MultiLevelPageTable, Translation
from .replacement import ALGORITHMS


@dataclass(frozen=True)
class Page:
    process_id: int
    virtual_page_number: int
    frame_number: int


class VirtualMemoryManager:
    def __init__(self, frame_count: int = 3, page_size: int = 256, tlb_capacity: int = 4) -> None:
        if frame_count <= 0 or tlb_capacity <= 0:
            raise ValueError("frame_count and tlb_capacity must be greater than zero")
        self.frame_count = frame_count
        self.page_table = MultiLevelPageTable(page_size=page_size)
        self.frames: list[int] = []
        self.pages: dict[int, Page] = {}
        self.tlb: OrderedDict[int, int] = OrderedDict()
        self.tlb_capacity = tlb_capacity
        self.tlb_hits = 0
        self.tlb_misses = 0

    def create_virtual_pages(self, process_id: int, num_pages: int) -> list[Page]:
        if process_id < 0 or num_pages < 0:
            raise ValueError("process_id and num_pages must be non-negative")
        pages = []
        for virtual_page in range(num_pages):
            page = Page(process_id, virtual_page, -1)
            self.pages[virtual_page] = page
            pages.append(page)
        return pages

    def allocate_frames(self, process_id: int, num_frames: int) -> list[Page]:
        if num_frames < 0:
            raise ValueError("num_frames must be non-negative")
        allocated = []
        for virtual_page, page in self.pages.items():
            if page.process_id != process_id or page.frame_number >= 0:
                continue
            if len(self.frames) >= self.frame_count or len(allocated) >= num_frames:
                break
            frame = len(self.frames)
            self.frames.append(virtual_page)
            mapped = Page(process_id, virtual_page, frame)
            self.pages[virtual_page] = mapped
            self.page_table.map_page(virtual_page, frame)
            allocated.append(mapped)
        return allocated

    def lookup(self, virtual_page: int) -> int | None:
        if virtual_page in self.tlb:
            self.tlb_hits += 1
            frame = self.tlb.pop(virtual_page)
            self.tlb[virtual_page] = frame
            return frame
        self.tlb_misses += 1
        page = self.pages.get(virtual_page)
        if page is None or page.frame_number < 0:
            return None
        self._cache_tlb(virtual_page, page.frame_number)
        return page.frame_number

    def translate(self, logical_address: int) -> Translation | None:
        page, _ = divmod(logical_address, self.page_table.page_size)
        if self.lookup(page) is None:
            return None
        return self.page_table.translate(logical_address)

    def run_replacement(self, reference_string: Sequence[int], algorithm: str) -> dict[str, object]:
        try:
            replacement = ALGORITHMS[algorithm]
        except KeyError as exc:
            raise ValueError(f"unknown algorithm {algorithm!r}; choose FIFO, LRU, or Optimal") from exc
        return replacement(reference_string, self.frame_count)

    def tlb_stats(self) -> dict[str, float | int]:
        total = self.tlb_hits + self.tlb_misses
        return {
            "hits": self.tlb_hits,
            "misses": self.tlb_misses,
            "lookups": total,
            "hit_ratio": self.tlb_hits / total if total else 0.0,
            "miss_ratio": self.tlb_misses / total if total else 0.0,
        }

    def _cache_tlb(self, virtual_page: int, frame: int) -> None:
        self.tlb.pop(virtual_page, None)
        self.tlb[virtual_page] = frame
        if len(self.tlb) > self.tlb_capacity:
            self.tlb.popitem(last=False)


def create_virtual_pages(manager: VirtualMemoryManager, process_id: int, num_pages: int) -> list[Page]:
    """Compatibility helper for callers that prefer functions."""
    return manager.create_virtual_pages(process_id, num_pages)
