from core import bootstrap_app


def test_bootstrap_builds_all_layers() -> None:
    runtime = bootstrap_app()
    assert runtime.api.health_service.get_status() == "ok"

