# Cloud-Resource-OS-Engine

CROVME is an OS and DBMS learning project covering process management,
resource allocation, virtual memory, paging, and deadlock management.

## Virtual memory demo

Run from the project root:

```powershell
python .\main.py
```

The demo creates virtual pages for a process, allocates physical frames,
translates logical addresses through a two-level page table, compares FIFO,
LRU, and Optimal page replacement, and prints TLB hit/miss analytics.

### Memory module functions

- `Memory.replacement.fifo`, `lru`, and `optimal` return page-fault counts,
  hit counts, and a frame trace.
- `Memory.paging.MultiLevelPageTable.map_page` maps a virtual page to a frame.
- `Memory.paging.MultiLevelPageTable.translate` returns page, offset, hierarchy
  indices, frame, and physical address.
- `Memory.virtual_memory.VirtualMemoryManager` coordinates page creation,
  frame allocation, TLB lookup, translation, replacement, and analytics.

The simulation is in-memory and does not require PostgreSQL to run.

Example output:

```text
Process 1: created 5 virtual pages
Allocated pages: [0, 1, 2]
FIFO: 9 page faults, 1 hits
LRU: 8 page faults, 2 hits
Optimal: 6 page faults, 4 hits
10 -> page 0, frame 0, physical 10
266 -> page 1, frame 1, physical 266
520 -> page 2, frame 2, physical 520
10 -> page 0, frame 0, physical 10
TLB analytics: {'hits': 1, 'misses': 3, 'lookups': 4, 'hit_ratio': 0.25, 'miss_ratio': 0.75}
```
