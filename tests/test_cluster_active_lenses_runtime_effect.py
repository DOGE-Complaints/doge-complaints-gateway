from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.intake_v2_fixtures import unbound_civic_ready


def _sqlite_path_from_url(database_url: str) -> Path:
    return Path(database_url.removeprefix("sqlite:///"))


def _write_lens_pack(root: Path, pack_id: str, primary: str) -> None:
    src = Path(__file__).resolve().parents[1] / "schema-packs" / "tallinn_civic" / "v1"
    dest = root / pack_id / "v1"
    dest.mkdir(parents=True)
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    manifest["schema_id"] = pack_id
    civic = manifest["node_clustering"]["civic"]
    civic["active_lenses"] = [primary]
    civic["primary_lens"] = primary
    civic["min_size"] = 2
    civic["min_size_by_lens"] = {primary: 2}
    civic["readiness_threshold"] = 1
    civic["geo_scope"] = None
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")


def _run_for_lens(
    monkeypatch: pytest.MonkeyPatch,
    sqlite_db_url: str,
    packs_root: Path,
    pack_id: str,
    primary: str,
) -> str:
    _write_lens_pack(packs_root, pack_id, primary)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", sqlite_db_url)
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("SCHEMA_PACKS_ROOT", str(packs_root))
    monkeypatch.setenv("NODE_SCHEMA_ID", pack_id)
    monkeypatch.setenv("NODE_SCHEMA_VERSION", "v1")
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        _ = client
        repo = get_api_dependencies().story_cluster_orchestrator.story_repository
        repo.save_story(unbound_civic_ready("lens-1"))
        repo.save_story(unbound_civic_ready("lens-2"))
        get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    _clear_api_dependencies_cache()

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        row = connection.execute(
            "SELECT cluster_id FROM issue_story_links ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    finally:
        connection.close()
    assert row is not None
    return str(row[0])


def test_cluster_active_lenses_from_pack_change_runtime_cluster_id_prefix(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packs_root = tmp_path / "packs"
    domain_db = f"sqlite:///{tmp_path / 'lens-domain.sqlite3'}"
    failure_db = f"sqlite:///{tmp_path / 'lens-failure.sqlite3'}"

    domain_cluster_id = _run_for_lens(
        monkeypatch, domain_db, packs_root, "lens_domain", "civic_domain_micro"
    )
    failure_cluster_id = _run_for_lens(
        monkeypatch, failure_db, packs_root, "lens_failure", "failure_pattern_micro"
    )

    assert domain_cluster_id.startswith("cluster:civic_domain_micro:")
    assert failure_cluster_id.startswith("cluster:failure_pattern_micro:")
    assert domain_cluster_id != failure_cluster_id
