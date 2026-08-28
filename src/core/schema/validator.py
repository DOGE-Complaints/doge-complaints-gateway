"""JSON Schema validate + SEC-002 limits. No eval / no pack-as-Python."""

from __future__ import annotations

import json
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from core.schema.errors import (
    ForbiddenFieldError,
    InvalidConstraintError,
    InvalidTypeError,
    MissingRequiredError,
    PolicyViolationError,
)

# Module constants — not product REQ thresholds (story T04).
MAX_PAYLOAD_BYTES = 65_536
MAX_NESTING_DEPTH = 32


def payload_byte_size(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def nesting_depth(value: Any, *, current: int = 0) -> int:
    if isinstance(value, dict):
        if not value:
            return current + 1
        return max(nesting_depth(v, current=current + 1) for v in value.values())
    if isinstance(value, list):
        if not value:
            return current + 1
        return max(nesting_depth(v, current=current + 1) for v in value)
    return current


def _collect_ref_strings(node: Any, acc: list[str]) -> None:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            acc.append(ref)
        for child in node.values():
            _collect_ref_strings(child, acc)
    elif isinstance(node, list):
        for child in node:
            _collect_ref_strings(child, acc)


def assert_schema_safe(schema: Mapping[str, Any]) -> None:
    refs: list[str] = []
    _collect_ref_strings(schema, refs)
    for ref in refs:
        if ref.startswith("http://") or ref.startswith("https://"):
            raise InvalidConstraintError("uncontrolled external $ref is not allowed")
    defs = schema.get("$defs") or schema.get("definitions") or {}
    if not isinstance(defs, dict):
        return

    def _def_name(ref: str) -> str | None:
        for prefix in ("#/$defs/", "#/definitions/"):
            if ref.startswith(prefix):
                return ref[len(prefix) :].split("/", 1)[0]
        return None

    def visit(name: str, stack: tuple[str, ...]) -> None:
        if name in stack:
            raise InvalidConstraintError("cyclic $ref")
        target = defs.get(name)
        if not isinstance(target, dict):
            return
        nested: list[str] = []
        _collect_ref_strings(target, nested)
        next_stack = stack + (name,)
        for nested_ref in nested:
            child = _def_name(nested_ref)
            if child:
                visit(child, next_stack)

    top_refs: list[str] = []
    _collect_ref_strings(dict(schema), top_refs)
    for ref in top_refs:
        name = _def_name(ref)
        if name:
            visit(name, ())
    for def_name in defs:
        visit(str(def_name), ())


def _map_jsonschema_error(exc: ValidationError) -> None:
    validator = exc.validator
    if validator == "required":
        raise MissingRequiredError(str(exc.message)) from exc
    if validator == "type":
        raise InvalidTypeError(str(exc.message)) from exc
    if validator in {"enum", "const", "minLength", "maxLength", "pattern", "minimum", "maximum"}:
        raise InvalidConstraintError(str(exc.message)) from exc
    if validator == "additionalProperties":
        raise ForbiddenFieldError(str(exc.message)) from exc
    raise InvalidConstraintError(str(exc.message)) from exc


def validate_payload(schema: Mapping[str, Any], payload: Mapping[str, Any]) -> None:
    if payload_byte_size(payload) > MAX_PAYLOAD_BYTES:
        raise PolicyViolationError("payload exceeds MAX_PAYLOAD_BYTES")
    if nesting_depth(payload) > MAX_NESTING_DEPTH:
        raise PolicyViolationError("payload exceeds MAX_NESTING_DEPTH")
    assert_schema_safe(schema)
    validator = Draft202012Validator(schema)
    try:
        validator.validate(payload)
    except ValidationError as exc:
        _map_jsonschema_error(exc)
