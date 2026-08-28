"""Schema Runtime contracts (REQ3-RUNTIME-001). Signatures MAY differ from parent sketch."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

# SCHEMA-003 representable states (this loader).
FIELD_POLICY_STATES: frozenset[str] = frozenset(
    {
        "required",
        "optional",
        "disabled",
        "forbidden",
        "node_private",
        "derived",
        "computed_aggregate_only",
    }
)


@dataclass(frozen=True)
class SchemaRef:
    schema_id: str
    schema_version: str


@dataclass(frozen=True)
class ReadinessPolicy:
    """Pack-side 3 knobs matching PromotionGatePolicy. Numbers come from pack files."""

    min_readiness_score: int
    min_stories: int
    require_actionable_canonical_type: bool


@dataclass(frozen=True)
class ExactLensBlock:
    lens_id: str
    source_fields: tuple[str, ...]
    algorithm: str
    scope: str
    scale: str
    missing_value_policy: str
    min_size: int
    readiness_policy: ReadinessPolicy
    version: str


@dataclass(frozen=True)
class SchemaContext:
    ref: SchemaRef
    payload_schema: Mapping[str, Any]
    field_policy: Mapping[str, str]
    exact_lenses: tuple[ExactLensBlock, ...]
    compatible_profiles: tuple[str, ...]
    pack_dir: Path


class SchemaRuntime(Protocol):
    """In-process schema pack runtime. Parent Protocol — signatures MAY differ."""

    def resolve(
        self, schema_ref: SchemaRef, profile_ref: str | None = None
    ) -> SchemaContext: ...

    def validate(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> None: ...

    def canonicalize(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> dict[str, Any]: ...

    def enforce_policy(
        self,
        schema_context: SchemaContext,
        payload: Mapping[str, Any],
        policy_context: Mapping[str, Any],
    ) -> None: ...

    def build_index(
        self, schema_context: SchemaContext, payload: Mapping[str, Any]
    ) -> None: ...

    def project(
        self, payload: Mapping[str, Any], target_schema_ref: SchemaRef
    ) -> None: ...
