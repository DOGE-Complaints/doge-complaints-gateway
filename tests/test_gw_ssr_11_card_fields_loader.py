"""GW-SSR-11 T01: pack.json card_fields allowlist; absent = civic form."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.schema import LocalSchemaRuntime, SchemaRef, UnsupportedVersionError
from core.schema.resolver import resolve_pack

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def test_legal_process_absent_card_fields_is_civic_form() -> None:
    manifest = json.loads((PACKS_ROOT / "legal_process" / "v1" / "pack.json").read_text())
    assert "card_fields" not in manifest
    ctx = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    assert ctx.card_fields == ()


def test_tallinn_civic_absent_card_fields_is_civic_form() -> None:
    manifest = json.loads((PACKS_ROOT / "tallinn_civic" / "v1" / "pack.json").read_text())
    assert "card_fields" not in manifest
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert ctx.card_fields == ()


def test_empty_array_is_civic_form(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["card_fields"] = []
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    ctx = LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
    assert ctx.card_fields == ()


def test_explicit_paths_are_loaded(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["card_fields"] = ["institution.office_id", "process.stage"]
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    ctx = LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
    assert ctx.card_fields == ("institution.office_id", "process.stage")


def test_non_array_card_fields_rejected(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["card_fields"] = "institution.office_id"
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError):
        LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
