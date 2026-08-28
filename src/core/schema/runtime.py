"""Local-first SchemaRuntime (REQ3-RUNTIME-002). Not wired into intake."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from core.schema.contracts import SchemaContext, SchemaRef
from core.schema.errors import ProfileIncompatibilityError
from core.schema.field_policy import enforce_field_policy
from core.schema.resolver import resolve_pack
from core.schema.validator import validate_payload

_IDX_LATER = "build_index is not implemented in T-wave (SSR-06 later)"
_PROC_LATER = "project is not implemented in T-wave (SSR-07 later)"


class LocalSchemaRuntime:
    """In-process loader + validate. ``build_index`` / ``project`` are explicit stubs."""

    def __init__(self, *, packs_root: Path | None = None) -> None:
        self._packs_root = packs_root

    def resolve(
        self, schema_ref: SchemaRef, profile_ref: str | None = None
    ) -> SchemaContext:
        context = resolve_pack(schema_ref, packs_root=self._packs_root)
        if profile_ref is not None and context.compatible_profiles:
            if profile_ref not in context.compatible_profiles:
                raise ProfileIncompatibilityError(
                    f"profile {profile_ref!r} incompatible with {schema_ref.schema_id}"
                )
        return context

    def validate(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> None:
        validate_payload(schema_context.payload_schema, payload)

    def canonicalize(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        del schema_context
        # No silent coerce: do not invent missing required values.
        return dict(payload)

    def enforce_policy(
        self,
        schema_context: SchemaContext,
        payload: Mapping[str, Any],
        policy_context: Mapping[str, Any],
    ) -> None:
        # D-SSR-3: do not read identity claims from policy_context.
        profile_ref = policy_context.get("profile_ref")
        if isinstance(profile_ref, str) and schema_context.compatible_profiles:
            if profile_ref not in schema_context.compatible_profiles:
                raise ProfileIncompatibilityError(
                    f"profile {profile_ref!r} incompatible with {schema_context.ref.schema_id}"
                )
        enforce_field_policy(schema_context.field_policy, payload)

    def build_index(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> None:
        del schema_context, payload
        raise NotImplementedError(_IDX_LATER)

    def project(
        self, payload: Mapping[str, Any], target_schema_ref: SchemaRef
    ) -> None:
        del payload, target_schema_ref
        raise NotImplementedError(_PROC_LATER)
