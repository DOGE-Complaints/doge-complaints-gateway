"""Named Issue-card leaves from a pack allowlist. Not SchemaRuntime.project."""

from __future__ import annotations

from typing import Any, Mapping

_BLOCKED_STATES: frozenset[str] = frozenset({"forbidden", "node_private"})


def _lookup(payload: Mapping[str, Any], dotted: str) -> tuple[bool, Any]:
    current: Any = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _path_blocked(path: str, field_policy: Mapping[str, str]) -> bool:
    if field_policy.get(path) in _BLOCKED_STATES:
        return True
    parts = path.split(".")
    for index in range(1, len(parts)):
        prefix = ".".join(parts[:index])
        if field_policy.get(prefix) in _BLOCKED_STATES:
            return True
    return False


def project_card_fields(
    payload: Mapping[str, Any],
    card_fields: tuple[str, ...],
    field_policy: Mapping[str, str],
) -> dict[str, Any]:
    """Return named allowlist leaves. Empty allowlist or all-blocked → empty dict (civic form)."""
    if not card_fields:
        return {}
    out: dict[str, Any] = {}
    for path in card_fields:
        if _path_blocked(path, field_policy):
            continue
        present, value = _lookup(payload, path)
        if present:
            out[path] = value
    return out
