"""Pack resolver: SCHEMA_PACKS_ROOT or <gateway-root>/schema-packs/."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from core.cluster.types import ClusterLens
from core.geo.scope import parse_cluster_geo_filter, parse_cluster_geo_scope
from core.schema.contracts import (
    FIELD_POLICY_STATES,
    CivicClusteringBlock,
    ExactLensBlock,
    NodeClusteringBlock,
    ReadinessPolicy,
    SchemaContext,
    SchemaRef,
)
from core.schema.errors import UnknownSchemaError, UnsupportedVersionError

_KNOWN_LENS_IDS = frozenset(member.value for member in ClusterLens)
_ID_ALGORITHMS = frozenset({"legacy_hash", "sha256"})
_CIVIC_REQUIRED_KEYS = (
    "active_lenses",
    "primary_lens",
    "min_size",
    "min_size_by_lens",
    "readiness_threshold",
    "signal_source",
    "id_algorithm",
    "geo_filter",
    "geo_scope",
    "tie_breaker",
    "type_resolution",
)

_ENV_PACKS_ROOT = "SCHEMA_PACKS_ROOT"
_MANIFEST_NAME = "pack.json"


def default_packs_root(*, environ: Mapping[str, str] | None = None) -> Path:
    """Config hook: env overrides; else gateway-root ``schema-packs/``."""
    env = environ if environ is not None else os.environ
    raw = env.get(_ENV_PACKS_ROOT)
    if raw:
        return Path(raw)
    # resolver.py → schema → core → src → gateway root
    return Path(__file__).resolve().parents[3] / "schema-packs"


def _read_json(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def _parse_dual_civic_lenses(manifest: Mapping[str, Any]) -> bool:
    """Opt-in civic+exact on one bound story. Absent/false = T-wave exact-only."""
    if "dual_civic_lenses" not in manifest:
        return False
    raw = manifest["dual_civic_lenses"]
    if raw is False:
        return False
    if raw is True:
        return True
    raise UnsupportedVersionError("dual_civic_lenses must be a boolean when present")


def _positive_int(raw: object, *, field: str) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise UnsupportedVersionError(
            f"node_clustering.civic.{field} must be a positive integer"
        )
    if raw < 1:
        raise UnsupportedVersionError(
            f"node_clustering.civic.{field} must be a positive integer"
        )
    return raw


def _parse_civic_clustering(manifest: Mapping[str, Any]) -> CivicClusteringBlock:
    """Fail-fast: ``node_clustering.civic`` required; no silent default. SCHEMA-005."""
    if "node_clustering" not in manifest:
        raise UnsupportedVersionError("node_clustering is required")
    raw_nc = manifest["node_clustering"]
    if not isinstance(raw_nc, dict):
        raise UnsupportedVersionError("node_clustering must be an object")
    if "civic" not in raw_nc:
        raise UnsupportedVersionError("node_clustering.civic is required")
    raw = raw_nc["civic"]
    if not isinstance(raw, dict):
        raise UnsupportedVersionError("node_clustering.civic must be an object")
    missing = [key for key in _CIVIC_REQUIRED_KEYS if key not in raw]
    if missing:
        raise UnsupportedVersionError(
            f"node_clustering.civic missing keys: {missing}"
        )

    lenses_raw = raw["active_lenses"]
    if not isinstance(lenses_raw, list) or not lenses_raw:
        raise UnsupportedVersionError(
            "node_clustering.civic.active_lenses must be a non-empty array"
        )
    active: list[str] = []
    for item in lenses_raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError(
                "node_clustering.civic.active_lenses entries must be non-empty strings"
            )
        lens_id = item.strip()
        if lens_id not in _KNOWN_LENS_IDS:
            raise UnsupportedVersionError(
                f"node_clustering.civic.active_lenses unknown lens: {lens_id}"
            )
        if lens_id not in active:
            active.append(lens_id)
    active_lenses = tuple(active)

    if not isinstance(raw["primary_lens"], str) or not raw["primary_lens"].strip():
        raise UnsupportedVersionError(
            "node_clustering.civic.primary_lens must be a non-empty string"
        )
    primary_lens = raw["primary_lens"].strip()
    if primary_lens not in _KNOWN_LENS_IDS:
        raise UnsupportedVersionError(
            f"node_clustering.civic.primary_lens unknown lens: {primary_lens}"
        )
    if primary_lens not in active_lenses:
        raise UnsupportedVersionError(
            "node_clustering.civic.primary_lens must appear in active_lenses"
        )

    min_size = _positive_int(raw["min_size"], field="min_size")
    by_lens_raw = raw["min_size_by_lens"]
    if not isinstance(by_lens_raw, dict):
        raise UnsupportedVersionError(
            "node_clustering.civic.min_size_by_lens must be an object"
        )
    min_size_by_lens: dict[str, int] = {}
    for lens_id, count in by_lens_raw.items():
        if not isinstance(lens_id, str) or lens_id not in _KNOWN_LENS_IDS:
            raise UnsupportedVersionError(
                f"node_clustering.civic.min_size_by_lens unknown lens: {lens_id}"
            )
        min_size_by_lens[lens_id] = _positive_int(count, field="min_size_by_lens")

    readiness = _positive_int(raw["readiness_threshold"], field="readiness_threshold")
    if readiness > 100:
        raise UnsupportedVersionError(
            "node_clustering.civic.readiness_threshold must be in range 1..100"
        )

    if not isinstance(raw["signal_source"], str):
        raise UnsupportedVersionError(
            "node_clustering.civic.signal_source must be a string"
        )
    signal_source = raw["signal_source"].strip().lower()
    if signal_source != "canonical":
        raise UnsupportedVersionError(
            "node_clustering.civic.signal_source must be canonical"
        )

    if not isinstance(raw["id_algorithm"], str):
        raise UnsupportedVersionError(
            "node_clustering.civic.id_algorithm must be a string"
        )
    id_algorithm = raw["id_algorithm"].strip().lower()
    if id_algorithm not in _ID_ALGORITHMS:
        raise UnsupportedVersionError(
            "node_clustering.civic.id_algorithm must be legacy_hash or sha256"
        )

    if not isinstance(raw["geo_filter"], str):
        raise UnsupportedVersionError(
            "node_clustering.civic.geo_filter must be a string"
        )
    try:
        geo_filter = parse_cluster_geo_filter(raw["geo_filter"])
    except ValueError as exc:
        raise UnsupportedVersionError(str(exc)) from exc

    geo_scope_raw = raw["geo_scope"]
    if geo_scope_raw is None:
        geo_scope: tuple[str, str] | None = None
    elif isinstance(geo_scope_raw, str):
        try:
            geo_scope = parse_cluster_geo_scope(geo_scope_raw)
        except ValueError as exc:
            raise UnsupportedVersionError(str(exc)) from exc
    else:
        raise UnsupportedVersionError(
            "node_clustering.civic.geo_scope must be a string or null"
        )

    if not isinstance(raw["tie_breaker"], str):
        raise UnsupportedVersionError(
            "node_clustering.civic.tie_breaker must be a string"
        )
    tie_breaker = raw["tie_breaker"].strip().lower()
    if tie_breaker != "alpha":
        raise UnsupportedVersionError(
            "node_clustering.civic.tie_breaker must be alpha"
        )

    if not isinstance(raw["type_resolution"], str) or not raw["type_resolution"].strip():
        raise UnsupportedVersionError(
            "node_clustering.civic.type_resolution must be a non-empty string"
        )
    type_resolution = raw["type_resolution"].strip().lower()

    return CivicClusteringBlock(
        active_lenses=active_lenses,
        primary_lens=primary_lens,
        min_size=min_size,
        min_size_by_lens=min_size_by_lens,
        readiness_threshold=readiness,
        signal_source=signal_source,
        id_algorithm=id_algorithm,
        geo_filter=geo_filter,
        geo_scope=geo_scope,
        tie_breaker=tie_breaker,
        type_resolution=type_resolution,
    )


def _parse_card_fields(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    """Optional dotted-path allowlist for named Issue card leaves. Absent/empty = civic form."""
    if "card_fields" not in manifest:
        return ()
    raw = manifest["card_fields"]
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise UnsupportedVersionError("card_fields must be an array of strings when present")
    paths: list[str] = []
    for item in raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError("card_fields entries must be non-empty strings")
        paths.append(item.strip())
    return tuple(paths)


def _parse_readiness(raw: Mapping[str, Any]) -> ReadinessPolicy:
    return ReadinessPolicy(
        min_readiness_score=int(raw["min_readiness_score"]),
        min_stories=int(raw["min_stories"]),
        require_actionable_canonical_type=bool(raw["require_actionable_canonical_type"]),
    )


def _parse_lens(raw: Mapping[str, Any]) -> ExactLensBlock:
    fields = raw.get("source_fields") or ()
    return ExactLensBlock(
        lens_id=str(raw["lens_id"]),
        source_fields=tuple(str(x) for x in fields),
        algorithm=str(raw["algorithm"]),
        scope=str(raw["scope"]),
        scale=str(raw["scale"]),
        missing_value_policy=str(raw["missing_value_policy"]),
        min_size=int(raw["min_size"]),
        readiness_policy=_parse_readiness(raw["readiness_policy"]),
        version=str(raw["version"]),
    )


def load_pack(pack_dir: Path, expected: SchemaRef) -> SchemaContext:
    manifest_path = pack_dir / _MANIFEST_NAME
    if not manifest_path.is_file():
        raise UnsupportedVersionError(
            f"unsupported schema version: {expected.schema_id}/{expected.schema_version}"
        )
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise UnsupportedVersionError("pack.json must be an object")
    schema_id = str(manifest.get("schema_id", ""))
    schema_version = str(manifest.get("schema_version", ""))
    if schema_id != expected.schema_id:
        raise UnknownSchemaError(f"unknown schema: {expected.schema_id}")
    if schema_version != expected.schema_version:
        raise UnsupportedVersionError(
            f"unsupported schema version: {expected.schema_id}/{expected.schema_version}"
        )
    schema_file = str(manifest.get("payload_schema") or "payload.schema.json")
    payload_schema = _read_json(pack_dir / schema_file)
    if not isinstance(payload_schema, dict):
        raise UnsupportedVersionError("payload schema must be an object")
    raw_policy = manifest.get("field_policy") or {}
    if not isinstance(raw_policy, dict):
        raise UnsupportedVersionError("field_policy must be an object")
    field_policy: dict[str, str] = {}
    for key, state in raw_policy.items():
        value = str(state)
        if value not in FIELD_POLICY_STATES:
            raise UnsupportedVersionError(f"unknown field_policy state: {value}")
        field_policy[str(key)] = value
    raw_lenses = manifest.get("exact_lenses") or []
    if not isinstance(raw_lenses, list) or not raw_lenses:
        raise UnsupportedVersionError("exact_lenses must be a non-empty array")
    lenses = tuple(_parse_lens(item) for item in raw_lenses if isinstance(item, dict))
    raw_profiles = manifest.get("compatible_profiles") or ()
    profiles = tuple(str(p) for p in raw_profiles)
    return SchemaContext(
        ref=expected,
        payload_schema=payload_schema,
        field_policy=field_policy,
        exact_lenses=lenses,
        compatible_profiles=profiles,
        pack_dir=pack_dir,
        node_clustering=NodeClusteringBlock(civic=_parse_civic_clustering(manifest)),
        dual_civic_lenses=_parse_dual_civic_lenses(manifest),
        card_fields=_parse_card_fields(manifest),
    )


def resolve_pack(
    schema_ref: SchemaRef,
    *,
    packs_root: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> SchemaContext:
    root = packs_root if packs_root is not None else default_packs_root(environ=environ)
    schema_dir = root / schema_ref.schema_id
    if not schema_dir.is_dir():
        raise UnknownSchemaError(f"unknown schema: {schema_ref.schema_id}")
    version_dir = schema_dir / schema_ref.schema_version
    if not version_dir.is_dir():
        raise UnsupportedVersionError(
            f"unsupported schema version: {schema_ref.schema_id}/{schema_ref.schema_version}"
        )
    return load_pack(version_dir, schema_ref)
