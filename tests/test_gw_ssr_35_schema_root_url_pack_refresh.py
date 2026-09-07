"""GW-SSR-35: SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH (mocked HTTP, no live network)."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from core.config import ConfigError, ENV_SCHEMA, load_config_from_env
from core.schema.contracts import SchemaRef
from core.schema.remote_fetch import (
    ensure_remote_pack,
    manifest_url,
    maybe_fetch_active_pack,
    pack_cache_fresh,
)
from core.schema.resolver import resolve_pack

_SCHEMA_ID = "remote_fixture"
_SCHEMA_VER = "v1"
_REGISTRY = "https://registry.test/schema-packs"

# Minimal resolvable pack (civic block required by resolver / NODE_SCHEMA boot).
_PACK_JSON = {
    "schema_id": _SCHEMA_ID,
    "schema_version": _SCHEMA_VER,
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

_PAYLOAD_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": True,
    "properties": {"note": {"type": "string"}},
}


def _base_env(tmp_path: Path, **extra: str) -> dict[str, str]:
    env = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "https://demo.example/api",
        "NODE_SCHEMA_ID": _SCHEMA_ID,
        "NODE_SCHEMA_VERSION": _SCHEMA_VER,
        "SCHEMA_PACKS_ROOT": str(tmp_path),
    }
    env.update(extra)
    return env


def _mock_registry(
    *,
    pack: dict | None = None,
    corrupt_manifest: bool = False,
    missing_pack_url: bool = False,
    hit_counter: list[int] | None = None,
) -> httpx.MockTransport:
    pack_body = json.dumps(pack or _PACK_JSON).encode("utf-8")
    payload_body = json.dumps(_PAYLOAD_SCHEMA).encode("utf-8")
    pack_url = f"{_REGISTRY}/files/pack.json"
    payload_url = f"{_REGISTRY}/files/payload.schema.json"
    counters = hit_counter if hit_counter is not None else []

    def handler(request: httpx.Request) -> httpx.Response:
        counters.append(1)
        url = str(request.url)
        if url.endswith("/manifest.json"):
            if corrupt_manifest:
                return httpx.Response(200, text="{not-json")
            if missing_pack_url:
                body = {
                    "schema_id": _SCHEMA_ID,
                    "schema_version": _SCHEMA_VER,
                    "files": {"payload.schema.json": payload_url},
                }
            else:
                body = {
                    "schema_id": _SCHEMA_ID,
                    "schema_version": _SCHEMA_VER,
                    "files": {
                        "pack.json": pack_url,
                        "payload.schema.json": payload_url,
                    },
                }
            return httpx.Response(200, json=body)
        if url == pack_url:
            return httpx.Response(200, content=pack_body)
        if url == payload_url:
            return httpx.Response(200, content=payload_body)
        return httpx.Response(404, text="not found")

    return httpx.MockTransport(handler)


def test_env_schema_lists_schema_root_url_and_refresh() -> None:
    names = {spec.name for spec in ENV_SCHEMA}
    assert "SCHEMA_ROOT_URL" in names
    assert "SCHEMA_PACK_REFRESH" in names


def test_schema_root_url_rejects_volume_path() -> None:
    with pytest.raises(ConfigError, match="not a filesystem/Volume path"):
        load_config_from_env(
            _base_env(Path("/tmp"), SCHEMA_ROOT_URL="/data/schema-packs")
        )


def test_schema_root_url_rejects_file_scheme(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not a filesystem/Volume path"):
        load_config_from_env(
            _base_env(tmp_path, SCHEMA_ROOT_URL="file:///tmp/schema-packs")
        )


def test_fetch_on_cache_miss_then_resolve_pack(tmp_path: Path) -> None:
    hits: list[int] = []
    client = httpx.Client(transport=_mock_registry(hit_counter=hits))
    assert ensure_remote_pack(
        schema_root_url=_REGISTRY,
        schema_id=_SCHEMA_ID,
        schema_version=_SCHEMA_VER,
        packs_root=tmp_path,
        refresh=False,
        client=client,
    )
    assert pack_cache_fresh(tmp_path, _SCHEMA_ID, _SCHEMA_VER)
    ctx = resolve_pack(
        SchemaRef(schema_id=_SCHEMA_ID, schema_version=_SCHEMA_VER),
        packs_root=tmp_path,
    )
    assert ctx.ref.schema_id == _SCHEMA_ID
    assert len(hits) >= 3  # manifest + pack + payload


def test_fresh_cache_skips_refetch(tmp_path: Path) -> None:
    hits: list[int] = []
    client = httpx.Client(transport=_mock_registry(hit_counter=hits))
    assert ensure_remote_pack(
        schema_root_url=_REGISTRY,
        schema_id=_SCHEMA_ID,
        schema_version=_SCHEMA_VER,
        packs_root=tmp_path,
        client=client,
    )
    first = len(hits)
    assert (
        ensure_remote_pack(
            schema_root_url=_REGISTRY,
            schema_id=_SCHEMA_ID,
            schema_version=_SCHEMA_VER,
            packs_root=tmp_path,
            refresh=False,
            client=client,
        )
        is False
    )
    assert len(hits) == first


def test_refresh_overwrites_cached_pack(tmp_path: Path) -> None:
    client = httpx.Client(transport=_mock_registry())
    ensure_remote_pack(
        schema_root_url=_REGISTRY,
        schema_id=_SCHEMA_ID,
        schema_version=_SCHEMA_VER,
        packs_root=tmp_path,
        client=client,
    )
    pack_path = tmp_path / _SCHEMA_ID / _SCHEMA_VER / "pack.json"
    original = pack_path.read_bytes()
    pack_path.write_text('{"corrupt": true}', encoding="utf-8")
    assert pack_path.read_bytes() != original

    updated = dict(_PACK_JSON)
    updated["field_policy"] = {"note": "optional", "extra_marker": "optional"}
    client2 = httpx.Client(transport=_mock_registry(pack=updated))
    assert ensure_remote_pack(
        schema_root_url=_REGISTRY,
        schema_id=_SCHEMA_ID,
        schema_version=_SCHEMA_VER,
        packs_root=tmp_path,
        refresh=True,
        client=client2,
    )
    rewritten = json.loads(pack_path.read_text(encoding="utf-8"))
    assert "extra_marker" in rewritten["field_policy"]


def test_corrupt_manifest_fail_fast_no_tallinn(tmp_path: Path) -> None:
    client = httpx.Client(transport=_mock_registry(corrupt_manifest=True))
    with pytest.raises(ConfigError, match="No foreign default pack"):
        ensure_remote_pack(
            schema_root_url=_REGISTRY,
            schema_id=_SCHEMA_ID,
            schema_version=_SCHEMA_VER,
            packs_root=tmp_path,
            client=client,
        )
    assert not (tmp_path / "tallinn_civic").exists()
    assert not pack_cache_fresh(tmp_path, _SCHEMA_ID, _SCHEMA_VER)


def test_boot_load_config_fetches_via_mock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hits: list[int] = []
    transport = _mock_registry(hit_counter=hits)

    class _Client(httpx.Client):
        def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("core.schema.remote_fetch.httpx.Client", _Client)
    env = _base_env(tmp_path, SCHEMA_ROOT_URL=_REGISTRY)
    cfg = load_config_from_env(env)
    assert cfg.schema_root_url == _REGISTRY
    assert cfg.schema_pack_refresh is False
    assert cfg.node_schema_id == _SCHEMA_ID
    assert pack_cache_fresh(tmp_path, _SCHEMA_ID, _SCHEMA_VER)
    assert len(hits) >= 3


def test_url_unset_does_not_fetch(tmp_path: Path) -> None:
    # SSR-34 path: no SCHEMA_ROOT_URL — boot uses on-disk tallinn via default helper
    # when NODE_SCHEMA points at fixture that exists under real packs root.
    # Here: URL unset + remote id missing → ConfigError (no fetch attempted).
    with pytest.raises(ConfigError, match="does not resolve"):
        load_config_from_env(_base_env(tmp_path))


def test_manifest_url_shape() -> None:
    assert (
        manifest_url(_REGISTRY, _SCHEMA_ID, _SCHEMA_VER)
        == f"{_REGISTRY}/{_SCHEMA_ID}/{_SCHEMA_VER}/manifest.json"
    )


def test_maybe_fetch_noop_without_url(tmp_path: Path) -> None:
    assert (
        maybe_fetch_active_pack(
            schema_root_url=None,
            schema_id=_SCHEMA_ID,
            schema_version=_SCHEMA_VER,
            refresh=False,
            environ={"SCHEMA_PACKS_ROOT": str(tmp_path)},
        )
        is False
    )


def test_missing_pack_json_in_manifest_fail_fast(tmp_path: Path) -> None:
    client = httpx.Client(transport=_mock_registry(missing_pack_url=True))
    with pytest.raises(ConfigError, match="pack.json"):
        ensure_remote_pack(
            schema_root_url=_REGISTRY,
            schema_id=_SCHEMA_ID,
            schema_version=_SCHEMA_VER,
            packs_root=tmp_path,
            client=client,
        )
