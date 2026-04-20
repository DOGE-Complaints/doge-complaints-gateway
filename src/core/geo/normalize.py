from __future__ import annotations


def normalize_location_query(query: str) -> str:
    """Canonical cache key: lowercase, collapsed whitespace."""
    return " ".join(query.lower().strip().split())
