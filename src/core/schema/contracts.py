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
class CivicClusteringBlock:
    """Civic ClusterLens knobs from pack.json ``node_clustering.civic`` (SCHEMA-005)."""

    active_lenses: tuple[str, ...]
    primary_lens: str
    min_size: int
    min_size_by_lens: Mapping[str, int]
    readiness_threshold: int
    signal_source: str
    id_algorithm: str
    geo_filter: str
    geo_scope: tuple[str, str] | None
    tie_breaker: str
    type_resolution: str


@dataclass(frozen=True)
class NodeClusteringBlock:
    """Pack clustering contract. Civic contour only in SSR-19; exact stays ``exact_lenses``."""

    civic: CivicClusteringBlock


GEO_INTAKE_MODES: frozenset[str] = frozenset(
    {"optional", "require_location_or_detail", "require_detail"}
)


@dataclass(frozen=True)
class GeoIntakeBlock:
    """Pack geo-detail intake policy (SCHEMA-005). No env override."""

    mode: str
    merge: bool
    mirror_to_payload: bool


@dataclass(frozen=True)
class TaxonomyCanonicalKey:
    """One pack vocabulary entry under an axis (SCHEMA-005 taxonomy.json)."""

    key: str
    meaning: str | None = None


@dataclass(frozen=True)
class TaxonomyPack:
    """Parsed pack ``taxonomy.json`` (Contour2 vocabulary). Optional on SchemaContext."""

    schema_id: str
    schema_version: str
    axes: tuple[str, ...]
    internal_axes: tuple[str, ...]
    canonical_keys: Mapping[str, tuple[TaxonomyCanonicalKey, ...]]
    axis_to_signal_map: Mapping[str, str]
    dispositions: tuple[str, ...]


@dataclass(frozen=True)
class SchemaContext:
    ref: SchemaRef
    payload_schema: Mapping[str, Any]
    field_policy: Mapping[str, str]
    exact_lenses: tuple[ExactLensBlock, ...]
    compatible_profiles: tuple[str, ...]
    pack_dir: Path
    node_clustering: NodeClusteringBlock
    geo_intake: GeoIntakeBlock
    dual_civic_lenses: bool = False
    card_fields: tuple[str, ...] = ()
    taxonomy: TaxonomyPack | None = None


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
