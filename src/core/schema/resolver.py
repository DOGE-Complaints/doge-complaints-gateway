"""Pack resolver: SCHEMA_PACKS_ROOT or <gateway-root>/schema-packs/."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from core.schema.contracts import (
    FIELD_POLICY_STATES,
    ExactLensBlock,
    ReadinessPolicy,
    SchemaContext,
    SchemaRef,
)
from core.schema.errors import UnknownSchemaError, UnsupportedVersionError

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
        dual_civic_lenses=_parse_dual_civic_lenses(manifest),
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
