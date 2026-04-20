from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "src" / "core"


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_domain_has_no_application_api_or_infrastructure_imports() -> None:
    content = _read("domain/contracts.py")
    assert "core.application" not in content
    assert "core.api" not in content
    assert "core.infrastructure" not in content


def test_application_does_not_import_api_or_infrastructure() -> None:
    content = _read("application/services.py")
    assert "core.api" not in content
    assert "core.infrastructure" not in content


def test_infrastructure_does_not_import_api_or_application() -> None:
    content = _read("infrastructure/repositories.py")
    assert "core.api" not in content
    assert "core.application" not in content


def test_api_dependencies_use_service_factory_provider() -> None:
    content = _read("api/dependencies.py")
    assert "provide_service_factory" in content
    assert "InMemoryHealthRepository(" not in content
    assert "HealthService(" not in content

