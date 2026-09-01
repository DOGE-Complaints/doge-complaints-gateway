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
    GEO_INTAKE_MODES,
    GEO_PRECISION_LEVELS,
    GPT_INSTANCE_RULE_TYPES,
    CivicClusteringBlock,
    ExactLensBlock,
    GeoIntakeBlock,
    GeoModelBlock,
    GptInstanceTerritoryBlock,
    GptInstanceTerritoryRule,
    NodeClusteringBlock,
    ReadinessPolicy,
    SchemaContext,
    SchemaRef,
    TaxonomyCanonicalKey,
    TaxonomyPack,
)
from core.schema.errors import UnknownSchemaError, UnsupportedVersionError
from core.taxonomy.axes import TAXONOMY_AXIS_VALUES
from core.taxonomy.disposition import LABEL_DISPOSITION_VALUES

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


def _parse_taxonomy_pack(
    pack_dir: Path,
    manifest: Mapping[str, Any],
    expected: SchemaRef,
) -> TaxonomyPack | None:
    """Optional Contour2 vocabulary. Absent ``taxonomy_schema`` → None (orphan file ignored)."""
    if "taxonomy_schema" not in manifest:
        return None
    raw_name = manifest["taxonomy_schema"]
    if not isinstance(raw_name, str) or not raw_name.strip():
        raise UnsupportedVersionError(
            "taxonomy_schema must be a non-empty string when present"
        )
    filename = raw_name.strip()
    path = pack_dir / filename
    if not path.is_file():
        raise UnsupportedVersionError(f"taxonomy file missing: {filename}")
    raw = _read_json(path)
    if not isinstance(raw, dict):
        raise UnsupportedVersionError("taxonomy.json must be an object")

    schema_id = str(raw.get("schema_id", ""))
    schema_version = str(raw.get("schema_version", ""))
    if schema_id != expected.schema_id or schema_version != expected.schema_version:
        raise UnsupportedVersionError(
            "taxonomy.json schema_id/schema_version must match pack.json"
        )

    axes_raw = raw.get("axes")
    if not isinstance(axes_raw, list) or not axes_raw:
        raise UnsupportedVersionError("taxonomy.json axes must be a non-empty array")
    axes_list: list[str] = []
    for item in axes_raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError(
                "taxonomy.json axes entries must be non-empty strings"
            )
        axis = item.strip()
        if axis not in TAXONOMY_AXIS_VALUES:
            raise UnsupportedVersionError(f"unknown axis: {axis}")
        if axis in axes_list:
            raise UnsupportedVersionError(f"duplicate axis in axes[]: {axis}")
        axes_list.append(axis)
    axes = tuple(axes_list)
    if set(axes) != TAXONOMY_AXIS_VALUES:
        missing = sorted(TAXONOMY_AXIS_VALUES - set(axes))
        raise UnsupportedVersionError(
            f"taxonomy.json axes must equal all 13 taxonomy axes; missing: {missing}"
        )

    internal_raw = raw.get("internal_axes") or []
    if not isinstance(internal_raw, list):
        raise UnsupportedVersionError("taxonomy.json internal_axes must be an array")
    internal_axes_list: list[str] = []
    for item in internal_raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError(
                "taxonomy.json internal_axes entries must be non-empty strings"
            )
        axis = item.strip()
        if axis not in axes:
            raise UnsupportedVersionError(
                f"taxonomy.json internal_axes entry not in axes: {axis}"
            )
        if axis not in internal_axes_list:
            internal_axes_list.append(axis)
    internal_axes = tuple(internal_axes_list)

    keys_raw = raw.get("canonical_keys")
    if keys_raw is None:
        keys_raw = {}
    if not isinstance(keys_raw, dict):
        raise UnsupportedVersionError("taxonomy.json canonical_keys must be an object")
    canonical_keys: dict[str, tuple[TaxonomyCanonicalKey, ...]] = {}
    for axis, entries in keys_raw.items():
        if not isinstance(axis, str) or axis not in axes:
            raise UnsupportedVersionError(f"unknown axis in canonical_keys: {axis}")
        if not isinstance(entries, list):
            raise UnsupportedVersionError(
                f"taxonomy.json canonical_keys[{axis}] must be an array"
            )
        seen: set[str] = set()
        parsed: list[TaxonomyCanonicalKey] = []
        for entry in entries:
            if not isinstance(entry, dict):
                raise UnsupportedVersionError(
                    f"taxonomy.json canonical_keys[{axis}] entries must be objects"
                )
            key_raw = entry.get("key")
            if not isinstance(key_raw, str) or not key_raw.strip():
                raise UnsupportedVersionError(
                    f"taxonomy.json canonical_keys[{axis}] key must be a non-empty string"
                )
            key = key_raw.strip()
            if key in seen:
                raise UnsupportedVersionError(
                    f"duplicate key in canonical_keys[{axis}]: {key}"
                )
            seen.add(key)
            meaning_raw = entry.get("meaning")
            meaning: str | None
            if meaning_raw is None:
                meaning = None
            elif isinstance(meaning_raw, str):
                meaning = meaning_raw
            else:
                raise UnsupportedVersionError(
                    f"taxonomy.json canonical_keys[{axis}].meaning must be a string when present"
                )
            parsed.append(TaxonomyCanonicalKey(key=key, meaning=meaning))
        canonical_keys[axis] = tuple(parsed)

    map_raw = raw.get("axis_to_signal_map")
    if map_raw is None:
        map_raw = {}
    if not isinstance(map_raw, dict):
        raise UnsupportedVersionError(
            "taxonomy.json axis_to_signal_map must be an object"
        )
    axis_to_signal_map: dict[str, str] = {}
    for axis, path in map_raw.items():
        if not isinstance(axis, str) or axis not in axes:
            raise UnsupportedVersionError(
                f"unknown axis in axis_to_signal_map: {axis}"
            )
        if not isinstance(path, str) or not path.strip():
            raise UnsupportedVersionError(
                f"axis_to_signal_map[{axis}] must be a non-empty dotted path"
            )
        axis_to_signal_map[axis] = path.strip()

    disp_raw = raw.get("dispositions")
    if disp_raw is None:
        dispositions = tuple(sorted(LABEL_DISPOSITION_VALUES))
    else:
        if not isinstance(disp_raw, list) or not disp_raw:
            raise UnsupportedVersionError(
                "taxonomy.json dispositions must be a non-empty array when present"
            )
        dispositions_list: list[str] = []
        for item in disp_raw:
            if not isinstance(item, str) or not item.strip():
                raise UnsupportedVersionError(
                    "taxonomy.json dispositions entries must be non-empty strings"
                )
            value = item.strip()
            if value not in LABEL_DISPOSITION_VALUES:
                raise UnsupportedVersionError(
                    f"unknown disposition in taxonomy.json: {value}"
                )
            if value not in dispositions_list:
                dispositions_list.append(value)
        dispositions = tuple(dispositions_list)

    return TaxonomyPack(
        schema_id=schema_id,
        schema_version=schema_version,
        axes=axes,
        internal_axes=internal_axes,
        canonical_keys=canonical_keys,
        axis_to_signal_map=axis_to_signal_map,
        dispositions=dispositions,
    )


def _parse_readiness(raw: Mapping[str, Any]) -> ReadinessPolicy:
    return ReadinessPolicy(
        min_readiness_score=int(raw["min_readiness_score"]),
        min_stories=int(raw["min_stories"]),
        require_actionable_canonical_type=bool(raw["require_actionable_canonical_type"]),
    )


def _parse_geo_intake(manifest: Mapping[str, Any]) -> GeoIntakeBlock:
    """Fail-fast: ``geo_intake`` required; no silent default. SCHEMA-005."""
    if "geo_intake" not in manifest:
        raise UnsupportedVersionError("geo_intake is required")
    raw = manifest["geo_intake"]
    if not isinstance(raw, dict):
        raise UnsupportedVersionError("geo_intake must be an object")
    mode_raw = raw.get("mode")
    if not isinstance(mode_raw, str) or mode_raw.strip() not in GEO_INTAKE_MODES:
        raise UnsupportedVersionError(
            "geo_intake.mode must be optional | require_location_or_detail | require_detail"
        )
    merge = raw.get("merge")
    if not isinstance(merge, bool):
        raise UnsupportedVersionError("geo_intake.merge must be a boolean")
    mirror = raw.get("mirror_to_payload")
    if not isinstance(mirror, bool):
        raise UnsupportedVersionError("geo_intake.mirror_to_payload must be a boolean")
    unknown = set(raw.keys()) - {"mode", "merge", "mirror_to_payload"}
    if unknown:
        raise UnsupportedVersionError(
            "Unknown geo_intake keys: " + ", ".join(sorted(str(key) for key in unknown))
        )
    return GeoIntakeBlock(
        mode=mode_raw.strip(),
        merge=merge,
        mirror_to_payload=mirror,
    )


def _parse_geo_model(manifest: Mapping[str, Any]) -> GeoModelBlock | None:
    """Optional pack precision vocabulary. Absent → None."""
    if "geo_model" not in manifest:
        return None
    raw = manifest["geo_model"]
    if not isinstance(raw, dict):
        raise UnsupportedVersionError("geo_model must be an object")
    levels_raw = raw.get("precision_levels")
    if not isinstance(levels_raw, list) or not levels_raw:
        raise UnsupportedVersionError("geo_model.precision_levels must be a non-empty array")
    levels: list[str] = []
    for item in levels_raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError(
                "geo_model.precision_levels entries must be non-empty strings"
            )
        token = item.strip()
        if token not in GEO_PRECISION_LEVELS:
            raise UnsupportedVersionError(f"unknown geo_model precision level: {token}")
        levels.append(token)
    inference: str | None = None
    if "default_precision_inference" in raw and raw.get("default_precision_inference") is not None:
        inference_raw = raw.get("default_precision_inference")
        if not isinstance(inference_raw, str) or not inference_raw.strip():
            raise UnsupportedVersionError(
                "geo_model.default_precision_inference must be a non-empty string when present"
            )
        inference = inference_raw.strip()
    unknown = set(raw.keys()) - {"precision_levels", "default_precision_inference"}
    if unknown:
        raise UnsupportedVersionError(
            "Unknown geo_model keys: " + ", ".join(sorted(str(key) for key in unknown))
        )
    return GeoModelBlock(
        precision_levels=tuple(levels),
        default_precision_inference=inference,
    )


def _parse_gpt_instance_territory_rule(
    raw: Mapping[str, Any], *, index: int
) -> GptInstanceTerritoryRule:
    type_raw = raw.get("type")
    if not isinstance(type_raw, str) or not type_raw.strip():
        raise UnsupportedVersionError(
            f"gpt_instance_territory.rules[{index}].type must be a non-empty string"
        )
    rule_type = type_raw.strip()
    if rule_type not in GPT_INSTANCE_RULE_TYPES:
        raise UnsupportedVersionError(
            f"unknown gpt_instance_territory rule type: {rule_type}"
        )
    if rule_type == "admin_token":
        level = raw.get("level")
        value = raw.get("value")
        if not isinstance(level, str) or not level.strip():
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] admin_token requires level"
            )
        if not isinstance(value, str) or not value.strip():
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] admin_token requires value"
            )
        allowed = {"type", "level", "value"}
        unknown = set(raw.keys()) - allowed
        if unknown:
            raise UnsupportedVersionError(
                "Unknown gpt_instance_territory.rules keys: "
                + ", ".join(sorted(str(key) for key in unknown))
            )
        return GptInstanceTerritoryRule(
            type=rule_type, level=level.strip(), value=value.strip()
        )
    if rule_type == "admin_id":
        level = raw.get("level")
        scheme = raw.get("scheme")
        value = raw.get("value")
        if not isinstance(level, str) or not level.strip():
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] admin_id requires level"
            )
        if not isinstance(scheme, str) or not scheme.strip():
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] admin_id requires scheme"
            )
        if not isinstance(value, str) or not value.strip():
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] admin_id requires value"
            )
        allowed = {"type", "level", "scheme", "value"}
        unknown = set(raw.keys()) - allowed
        if unknown:
            raise UnsupportedVersionError(
                "Unknown gpt_instance_territory.rules keys: "
                + ", ".join(sorted(str(key) for key in unknown))
            )
        return GptInstanceTerritoryRule(
            type=rule_type,
            level=level.strip(),
            scheme=scheme.strip(),
            value=value.strip(),
        )
    # bbox
    for key in ("west", "south", "east", "north"):
        if key not in raw or not isinstance(raw[key], (int, float)) or isinstance(raw[key], bool):
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] bbox requires numeric {key}"
            )
    allowed = {"type", "west", "south", "east", "north"}
    unknown = set(raw.keys()) - allowed
    if unknown:
        raise UnsupportedVersionError(
            "Unknown gpt_instance_territory.rules keys: "
            + ", ".join(sorted(str(key) for key in unknown))
        )
    return GptInstanceTerritoryRule(
        type=rule_type,
        west=float(raw["west"]),
        south=float(raw["south"]),
        east=float(raw["east"]),
        north=float(raw["north"]),
    )


def _parse_gpt_instance_territory(
    manifest: Mapping[str, Any],
) -> GptInstanceTerritoryBlock | None:
    """Optional GPT instance territory. Absent → None. Parse-only (no intake enforce)."""
    if "gpt_instance_territory" not in manifest:
        return None
    raw = manifest["gpt_instance_territory"]
    if not isinstance(raw, dict):
        raise UnsupportedVersionError("gpt_instance_territory must be an object")
    enabled = raw.get("enabled")
    if not isinstance(enabled, bool):
        raise UnsupportedVersionError("gpt_instance_territory.enabled must be a boolean")
    rules_raw = raw.get("rules")
    if not isinstance(rules_raw, list):
        raise UnsupportedVersionError("gpt_instance_territory.rules must be an array")
    rules: list[GptInstanceTerritoryRule] = []
    for index, item in enumerate(rules_raw):
        if not isinstance(item, dict):
            raise UnsupportedVersionError(
                f"gpt_instance_territory.rules[{index}] must be an object"
            )
        rules.append(_parse_gpt_instance_territory_rule(item, index=index))
    unknown = set(raw.keys()) - {"enabled", "rules"}
    if unknown:
        raise UnsupportedVersionError(
            "Unknown gpt_instance_territory keys: "
            + ", ".join(sorted(str(key) for key in unknown))
        )
    return GptInstanceTerritoryBlock(enabled=enabled, rules=tuple(rules))


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
        geo_intake=_parse_geo_intake(manifest),
        dual_civic_lenses=_parse_dual_civic_lenses(manifest),
        card_fields=_parse_card_fields(manifest),
        taxonomy=_parse_taxonomy_pack(pack_dir, manifest, expected),
        geo_model=_parse_geo_model(manifest),
        gpt_instance_territory=_parse_gpt_instance_territory(manifest),
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
