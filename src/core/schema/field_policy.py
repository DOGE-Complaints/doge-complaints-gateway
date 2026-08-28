"""Field-policy enforcement (SCHEMA-003 states). No identity claims."""

from __future__ import annotations

from typing import Any, Mapping

from core.schema.errors import ForbiddenFieldError, MissingRequiredError, PolicyViolationError


def _lookup(payload: Mapping[str, Any], dotted: str) -> tuple[bool, Any]:
    current: Any = payload
    for part in dotted.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return False, None
        current = current[part]
    return True, current


def enforce_field_policy(
    field_policy: Mapping[str, str], payload: Mapping[str, Any]
) -> None:
    for path, state in field_policy.items():
        present, value = _lookup(payload, path)
        if state == "required" and not present:
            raise MissingRequiredError(f"missing required field: {path}")
        if state == "forbidden" and present:
            raise ForbiddenFieldError(f"forbidden field present: {path}")
        if state == "disabled" and present:
            raise PolicyViolationError(f"disabled field present: {path}")
        if state == "node_private" and present and value is not None:
            # Present is allowed in-process; no identity/federation export in T-wave.
            continue
