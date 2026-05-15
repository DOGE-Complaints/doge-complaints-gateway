from __future__ import annotations

from hashlib import sha256


def resolve_idempotency_key(header_value: str | None, raw_body: bytes) -> str:
    if header_value is not None and header_value.strip():
        return header_value.strip()
    return sha256(raw_body).hexdigest()
