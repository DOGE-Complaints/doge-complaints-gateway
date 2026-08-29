"""GW-SSR-09 T03: ``schema-packs/`` visible to resolver default.

``SCHEMA_PACKS_ROOT`` is env-only (``resolver.py``); not an ``AppConfig`` field.
Dockerfile in gateway tree is Not found — do not invent. Live image = operator
(G9), not overnight proof. Pack id ``tallinn_civic`` stays.
"""

from __future__ import annotations

from pathlib import Path

from core.schema.contracts import SchemaRef
from core.schema.resolver import default_packs_root, resolve_pack
from core.schema.runtime import LocalSchemaRuntime

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def test_schema_packs_directory_exists() -> None:
    assert PACKS_ROOT.is_dir()
    assert (PACKS_ROOT / "legal_process" / "v1" / "pack.json").is_file()
    assert (PACKS_ROOT / "tallinn_civic" / "v1" / "pack.json").is_file()


def test_default_packs_root_resolves_example_packs() -> None:
    root = default_packs_root(environ={})
    assert root == PACKS_ROOT
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=root)
    assert legal.ref.schema_id == "legal_process"
    civic = LocalSchemaRuntime(packs_root=root).resolve(SchemaRef("tallinn_civic", "v1"))
    assert civic.ref.schema_id == "tallinn_civic"
    assert civic.ref.schema_version == "v1"


def test_schema_packs_root_env_overrides_without_appconfig(tmp_path: Path) -> None:
    override = default_packs_root(environ={"SCHEMA_PACKS_ROOT": str(tmp_path)})
    assert override == tmp_path
    config_dir = GATEWAY_ROOT / "src" / "core" / "config"
    for path in config_dir.rglob("*.py"):
        assert "SCHEMA_PACKS_ROOT" not in path.read_text(encoding="utf-8")


def test_no_dockerfile_invented_in_gateway_tree() -> None:
    assert not (GATEWAY_ROOT / "Dockerfile").exists()
    assert not (GATEWAY_ROOT / "Dockerfile.prod").exists()
    assert list(GATEWAY_ROOT.glob("Dockerfile*")) == []


def test_asgi_has_no_new_filter_http() -> None:
    text = (GATEWAY_ROOT / "src" / "core" / "api" / "asgi_app.py").read_text(encoding="utf-8")
    assert "story_dimensions" not in text
    assert "/schema-filter" not in text
    assert '@app.get("/tallinn/issues")' in text
