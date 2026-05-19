"""REQ-41 GAP-41-04: env-only config loading in isolated subprocess (CE-01..03)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"

_SUBPROCESS_SCRIPT = """
import json
import os
import sys

sys.path.insert(0, os.environ["GW_SRC"])
from core.config import ConfigError, load_config_from_env

env = json.loads(os.environ["GW_ENV_JSON"])
op = os.environ["GW_OP"]

try:
    if op == "load":
        cfg = load_config_from_env(env)
        print(
            json.dumps(
                {
                    "ok": True,
                    "cluster_cron_enabled": cfg.cluster_cron_enabled,
                    "db_backend": cfg.db_backend,
                }
            )
        )
    elif op == "fail":
        load_config_from_env(env)
        print(json.dumps({"ok": False, "error": "expected ConfigError"}))
except ConfigError as exc:
    print(json.dumps({"ok": False, "error": str(exc)}))
"""


def _demo_env(**overrides: str) -> dict[str, str]:
    base = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "https://demo.example/api",
        "REQUEST_TIMEOUT_S": "15",
        "DB_BACKEND": "in_memory",
        "SUPABASE_URL": "",
        "SUPABASE_SERVICE_ROLE": "",
    }
    base.update(overrides)
    return base


def _run_config_subprocess(
    *,
    env: dict[str, str],
    op: str,
    cwd: Path,
) -> dict[str, object]:
    proc_env = {
        "GW_SRC": str(_SRC),
        "GW_ENV_JSON": json.dumps(env),
        "GW_OP": op,
        "PATH": os.environ.get("PATH", ""),
    }
    completed = subprocess.run(
        [sys.executable, "-c", _SUBPROCESS_SCRIPT],
        env=proc_env,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout.strip())


@pytest.fixture()
def isolated_cwd(tmp_path: Path) -> Path:
    """Empty directory without project .env for subprocess cwd."""
    return tmp_path


def test_ce01_load_config_from_env_dict_without_dotenv(isolated_cwd: Path) -> None:
    """CE-01: explicit env dict yields valid AppConfig (subprocess, no .env cwd)."""
    result = _run_config_subprocess(env=_demo_env(), op="load", cwd=isolated_cwd)
    assert result["ok"] is True
    assert result["db_backend"] == "in_memory"


def test_ce02_missing_required_field_raises_config_error(isolated_cwd: Path) -> None:
    """CE-02: missing API_BASE_URL → ConfigError."""
    env = _demo_env()
    del env["API_BASE_URL"]
    result = _run_config_subprocess(env=env, op="fail", cwd=isolated_cwd)
    assert result["ok"] is False
    assert "API_BASE_URL" in str(result["error"])


def test_ce03_cluster_cron_enabled_false_from_env(isolated_cwd: Path) -> None:
    """CE-03: CLUSTER_CRON_ENABLED=false read from env only."""
    result = _run_config_subprocess(
        env=_demo_env(CLUSTER_CRON_ENABLED="false"),
        op="load",
        cwd=isolated_cwd,
    )
    assert result["ok"] is True
    assert result["cluster_cron_enabled"] is False
