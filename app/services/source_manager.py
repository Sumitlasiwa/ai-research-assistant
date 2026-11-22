
def assign_source_ids(sources: list[dict]) -> list[dict]:
    """Assign stable IDs to sources for report citations."""
    identified_sources = []

    for index, source in enumerate(sources, start=1):
        identified_sources.append({
            **source,
            "source_id": f"S{index}"
        })

    return identified_sources
