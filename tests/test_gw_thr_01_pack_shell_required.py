"""GW-THR-01: mandatory shell capabilities sidecar; fail-closed resolve."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.config import ConfigError, load_config_from_env
from core.schema import SchemaRef, UnsupportedVersionError
from core.schema.resolver import resolve_pack
from core.schema.shell_capabilities import (
    CAP_VERIFICATION_VALIDATION_TYPE,
    SHELL_CAPABILITIES_FILENAME,
    write_shell_capabilities,
)

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def _minimal_manifest(schema_id: str = "fixture_shell", schema_version: str = "v1") -> dict:
    return {
        "schema_id": schema_id,
        "schema_version": schema_version,
        "payload_schema": "payload.schema.json",
        "field_policy": {"note": "optional"},
        "compatible_profiles": ["demo"],
        "exact_lenses": [
            {
                "lens_id": "police_station",
                "source_fields": ["note"],
                "algorithm": "exact",
                "scope": "node",
                "scale": "micro",
                "missing_value_policy": "skip",
                "min_size": 3,
                "version": "v1",
                "readiness_policy": {
                    "min_readiness_score": 40,
                    "min_stories": 3,
                    "require_actionable_canonical_type": False,
                },
            }
        ],
        "node_clustering": {
            "civic": {
                "active_lenses": [
                    "composite_primary_micro",
                    "civic_domain_micro",
                    "failure_pattern_micro",
                    "civic_weight_systemic",
                    "desired_outcome_local",
                    "affected_group_local",
                    "geographic_district_micro",
                    "service_object_micro",
                    "deep_need_local",
                    "ecosystem_signal_systemic",
                ],
                "primary_lens": "composite_primary_micro",
                "min_size": 5,
                "min_size_by_lens": {
                    "composite_primary_micro": 8,
                    "service_object_micro": 3,
                    "deep_need_local": 3,
                    "ecosystem_signal_systemic": 3,
                },
                "readiness_threshold": 60,
                "signal_source": "canonical",
                "id_algorithm": "sha256",
                "geo_filter": "country",
                "geo_scope": None,
                "tie_breaker": "alpha",
                "type_resolution": "canonical_priority",
            }
        },
        "geo_intake": {"mode": "optional", "merge": True, "mirror_to_payload": False},
    }


def _payload_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "properties": {"note": {"type": "string"}},
    }


def _write_fixture_pack(
    root: Path,
    *,
    schema_id: str = "fixture_shell",
    schema_version: str = "v1",
    with_shell: bool = True,
    integration_name: str = "fixture_phone_sms",
) -> Path:
    pack_dir = root / schema_id / schema_version
    pack_dir.mkdir(parents=True)
    (pack_dir / "pack.json").write_text(
        json.dumps(_minimal_manifest(schema_id, schema_version)), encoding="utf-8"
    )
    (pack_dir / "payload.schema.json").write_text(
        json.dumps(_payload_schema()), encoding="utf-8"
    )
    if with_shell:
        write_shell_capabilities(
            pack_dir,
            validation_type="phone",
            integration_name=integration_name,
        )
    return pack_dir


def test_warehouse_activatable_packs_resolve_with_shell_caps() -> None:
    tallinn = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert tallinn.shell_capabilities.validation_type == "phone"
    assert tallinn.shell_capabilities.integration_name == "tallinn_phone_sms"
    assert tallinn.shell_capabilities.max_reactions_per_actor == 3

    uus = resolve_pack(SchemaRef("uus_veerenni_civic", "v3"), packs_root=PACKS_ROOT)
    assert uus.shell_capabilities.validation_type == "phone"
    assert uus.shell_capabilities.integration_name == "uus_phone_sms"
    assert uus.shell_capabilities.reaction_enables["amused"] is False


def test_complete_pack_resolves_success(tmp_path: Path) -> None:
    _write_fixture_pack(tmp_path)
    ctx = resolve_pack(SchemaRef("fixture_shell", "v1"), packs_root=tmp_path)
    assert ctx.shell_capabilities.validation_type == "phone"
    assert ctx.shell_capabilities.max_depth >= 1
    assert "image/jpeg" in ctx.shell_capabilities.media_allowed_types


def test_missing_shell_sidecar_fail_closed(tmp_path: Path) -> None:
    _write_fixture_pack(tmp_path, with_shell=False)
    with pytest.raises(UnsupportedVersionError, match="shell_capabilities"):
        resolve_pack(SchemaRef("fixture_shell", "v1"), packs_root=tmp_path)


def test_incomplete_capabilities_fail_closed_no_silent_defaults(tmp_path: Path) -> None:
    pack_dir = _write_fixture_pack(tmp_path)
    # Strip verification type entry — must not invent phone silently.
    path = pack_dir / SHELL_CAPABILITIES_FILENAME
    body = json.loads(path.read_text(encoding="utf-8"))
    body["entries"] = [
        e for e in body["entries"] if e["id"] != CAP_VERIFICATION_VALIDATION_TYPE
    ]
    path.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="missing mandatory"):
        resolve_pack(SchemaRef("fixture_shell", "v1"), packs_root=tmp_path)


def test_node_schema_boot_maps_missing_caps_to_config_error(tmp_path: Path) -> None:
    _write_fixture_pack(tmp_path, with_shell=False)
    env = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "https://demo.example/api",
        "REQUEST_TIMEOUT_S": "30",
        "NODE_SCHEMA_ID": "fixture_shell",
        "NODE_SCHEMA_VERSION": "v1",
        "SCHEMA_PACKS_ROOT": str(tmp_path),
        "SCHEMA_PACK_BOOT_SOFT": "0",
    }
    with pytest.raises(ConfigError, match="does not resolve|shell_capabilities"):
        load_config_from_env(env)


def test_pack_json_has_no_invented_threads_key_block() -> None:
    """AC-GW-THR01-04: capabilities live in sidecar; pack.json not forced key table."""
    for rel in (
        "tallinn_civic/v1/pack.json",
        "uus_veerenni_civic/v3/pack.json",
    ):
        manifest = json.loads((PACKS_ROOT / rel).read_text(encoding="utf-8"))
        assert "threads" not in manifest
        assert "verification" not in manifest
        assert (PACKS_ROOT / rel).with_name(SHELL_CAPABILITIES_FILENAME).is_file()


def test_copy_pack_without_sidecar_still_fail_closed(tmp_path: Path) -> None:
    src = PACKS_ROOT / "legal_process" / "v1"
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    shutil.copy(src / "pack.json", dest / "pack.json")
    # Intentionally omit shell_capabilities.json
    with pytest.raises(UnsupportedVersionError, match="shell_capabilities"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)
