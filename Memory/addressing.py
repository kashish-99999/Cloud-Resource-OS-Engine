"""Logical-address helpers for paged memory."""

from __future__ import annotations


def split_address(logical_address: int, page_size: int) -> tuple[int, int]:
    """Return ``(page_number, offset)`` for a logical byte address."""
    if logical_address < 0:
        raise ValueError("logical_address must be non-negative")
    if page_size <= 0:
        raise ValueError("page_size must be greater than zero")
    return divmod(logical_address, page_size)


def compose_address(page_number: int, offset: int, page_size: int) -> int:
    """Build a logical address from a page number and page offset."""
    if page_number < 0 or offset < 0:
        raise ValueError("page_number and offset must be non-negative")
    if page_size <= 0:
        raise ValueError("page_size must be greater than zero")
    if offset >= page_size:
        raise ValueError("offset must be smaller than page_size")
    return page_number * page_size + offset
