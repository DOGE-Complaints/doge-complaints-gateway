"""Deterministic payload_hash (DATA-004 / D-SSR-5).

Do not treat a client-supplied hash as authority — compute after validate.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


def canonical_payload_json(payload: Mapping[str, Any]) -> str:
    """Stable JSON for hashing: sorted keys, compact separators, UTF-8 text."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def payload_hash_for(payload: Mapping[str, Any]) -> str:
    """SHA-256 hex digest of canonical JSON of a validated payload."""
    return hashlib.sha256(canonical_payload_json(payload).encode("utf-8")).hexdigest()


def authoritative_payload_hash(payload: Mapping[str, Any] | None) -> str | None:
    """Persist-path hash: compute from payload, or None. Ignore client-supplied digests."""
    if payload is None:
        return None
    return payload_hash_for(payload)
