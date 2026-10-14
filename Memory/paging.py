"""Two-level page-table simulation and address translation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Translation:
    logical_address: int
    page_number: int
    offset: int
    frame_number: int
    physical_address: int
    level_one_index: int
    level_two_index: int


class MultiLevelPageTable:
    """Map virtual pages through a two-level page-table hierarchy."""

    def __init__(self, page_size: int = 256, entries_per_level: int = 16) -> None:
        if page_size <= 0 or entries_per_level <= 0:
            raise ValueError("page_size and entries_per_level must be greater than zero")
        self.page_size = page_size
        self.entries_per_level = entries_per_level
        self._entries: dict[tuple[int, int], int] = {}

    def map_page(self, virtual_page: int, frame_number: int) -> None:
        if virtual_page < 0 or frame_number < 0:
            raise ValueError("page and frame numbers must be non-negative")
        level_two = virtual_page % self.entries_per_level
        level_one = virtual_page // self.entries_per_level
        self._entries[(level_one, level_two)] = frame_number

    def unmap_page(self, virtual_page: int) -> None:
        self._entries.pop(self._indices(virtual_page), None)

    def translate(self, logical_address: int) -> Translation:
        if logical_address < 0:
            raise ValueError("logical_address must be non-negative")
        page_number, offset = divmod(logical_address, self.page_size)
        indices = self._indices(page_number)
        try:
            frame_number = self._entries[indices]
        except KeyError as exc:
            raise KeyError(f"virtual page {page_number} is not mapped") from exc
        return Translation(
            logical_address,
            page_number,
            offset,
            frame_number,
            frame_number * self.page_size + offset,
            indices[0],
            indices[1],
        )

    def _indices(self, virtual_page: int) -> tuple[int, int]:
        if virtual_page < 0:
            raise ValueError("virtual_page must be non-negative")
        return divmod(virtual_page, self.entries_per_level)
