"""Run the CROVME virtual-memory and paging demonstration."""

from Memory.virtual_memory import VirtualMemoryManager


def main() -> None:
    process_id = 1
    manager = VirtualMemoryManager(frame_count=3, page_size=256, tlb_capacity=3)

    pages = manager.create_virtual_pages(process_id, 5)
    allocated = manager.allocate_frames(process_id, 3)
    print(f"Process {process_id}: created {len(pages)} virtual pages")
    print(f"Allocated pages: {[page.virtual_page_number for page in allocated]}")

    reference_string = [0, 1, 2, 0, 3, 0, 4, 2, 3, 1]
    print(f"Reference string: {reference_string}")
    for algorithm in ("FIFO", "LRU", "Optimal"):
        result = manager.run_replacement(reference_string, algorithm)
        print(f"{algorithm}: {result['faults']} page faults, {result['hits']} hits")

    print("\nAddress translations:")
    for logical_address in (10, 266, 520, 10):
        translation = manager.translate(logical_address)
        if translation is None:
            print(f"{logical_address}: page not resident")
        else:
            print(
                f"{logical_address} -> page {translation.page_number}, "
                f"frame {translation.frame_number}, physical {translation.physical_address}"
            )

    print(f"\nTLB analytics: {manager.tlb_stats()}")


if __name__ == "__main__":
    main()
