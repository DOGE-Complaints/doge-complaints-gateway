"""GW-SSR-23: geo_detail parse + pack geo_intake + merge with location_query."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.cluster import ClusterLens
from core.domain import StoryGeoSnapshot
from core.geo.intake_merge import merge_client_geo_detail
from core.intake import IntakeValidationError, parse_story_intake_request
from core.intake.contracts import GeoDetail, GeoDetailAddress
from core.schema.contracts import GeoIntakeBlock, SchemaRef
from core.schema.errors import UnsupportedVersionError
from core.schema.resolver import load_pack, resolve_pack
from gw_ssr_16_node_schema import monkeypatch_node_schema
from tests.intake_v2_fixtures import valid_v2_intake_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts
from tests.test_gw_ssr_04_schema_driven_cluster_lens import CLUSTERLENS_BASELINE

PACKS_ROOT = Path(__file__).resolve().parents[1] / "schema-packs"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch_node_schema(monkeypatch)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    _clear_api_dependencies_cache()


def _intake(
    *,
    location_query: str | None = None,
    geo_detail: dict | None = None,
    omit_location: bool = False,
) -> dict:
    narrative = {
        "original_text": "Road damage near the center.",
        "language": "en",
        "session_language": "en",
        "title": {"et": "Tee", "ru": "Дорога", "en": "Road"},
        "description": {"et": "Kahju", "ru": "Повреждение", "en": "Damage"},
        "canonical_type": "complaint",
        "canonical_labels": ["roads"],
    }
    if not omit_location:
        narrative["location_query"] = location_query or ""
    elif location_query is not None:
        narrative["location_query"] = location_query
    payload = valid_v2_intake_payload(narrative=narrative)
    if geo_detail is not None:
        payload["geo_detail"] = geo_detail
    return payload


def test_clusterlens_still_ten_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10


def test_three_packs_have_geo_intake() -> None:
    for schema_id in ("tallinn_civic", "legal_process", "mobility_observation"):
        ctx = resolve_pack(SchemaRef(schema_id, "v1"))
        assert ctx.geo_intake.mode == "optional"
        assert ctx.geo_intake.merge is True


def test_accept_geo_detail_202(client: TestClient) -> None:
    response = post_intake_via_story_drafts(
        client,
        json=_intake(
            location_query="Tallinn, Estonia",
            geo_detail={
                "latitude": 59.437,
                "longitude": 24.7536,
                "address": {"district": "kalamaja", "settlement": "tallinn"},
                "normalized_label": "Kalamaja",
            },
        ),
        headers={"idempotency-key": "ssr23-accept-detail"},
    )
    assert response.status_code == 202, response.text


def test_invalid_lat_without_lon_400(client: TestClient) -> None:
    response = post_intake_via_story_drafts(
        client,
        json=_intake(
            location_query="Tallinn, Estonia",
            geo_detail={"latitude": 59.437},
        ),
        headers={"idempotency-key": "ssr23-invalid-pair"},
    )
    assert response.status_code == 400
    assert "longitude" in response.json()["error"]["message"]


def test_house_xor_invalid() -> None:
    payload = _intake(
        location_query="Tallinn",
        geo_detail={"address": {"house": "12", "house_range": "10-14"}},
    )
    with pytest.raises(IntakeValidationError, match="house"):
        parse_story_intake_request(payload)


def test_optional_omit_202(client: TestClient) -> None:
    response = post_intake_via_story_drafts(
        client,
        json=_intake(omit_location=True),
        headers={"idempotency-key": "ssr23-optional-omit"},
    )
    assert response.status_code == 202, response.text


def test_require_detail_miss_400(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    from core.config import schema as config_schema

    def _require(*, schema_id: str, schema_version: str) -> GeoIntakeBlock:
        return GeoIntakeBlock(
            mode="require_detail", merge=True, mirror_to_payload=False
        )

    monkeypatch.setattr(config_schema, "geo_intake_from_active_node", _require)
    response = post_intake_via_story_drafts(
        client,
        json=_intake(location_query="Tallinn, Estonia"),
        headers={"idempotency-key": "ssr23-require-detail-miss"},
    )
    assert response.status_code == 400
    assert "geo_detail" in response.json()["error"]["message"]


def test_require_location_or_detail_miss_400(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    from core.config import schema as config_schema

    def _require(*, schema_id: str, schema_version: str) -> GeoIntakeBlock:
        return GeoIntakeBlock(
            mode="require_location_or_detail",
            merge=True,
            mirror_to_payload=False,
        )

    monkeypatch.setattr(config_schema, "geo_intake_from_active_node", _require)
    response = post_intake_via_story_drafts(
        client,
        json=_intake(omit_location=True),
        headers={"idempotency-key": "ssr23-require-either-miss"},
    )
    assert response.status_code == 400
    assert "location_query or geo_detail" in response.json()["error"]["message"]


def test_merge_client_district_wins() -> None:
    provider = StoryGeoSnapshot(
        normalized_label="Kalamaja, Tallinn, EE",
        latitude=59.448,
        longitude=24.738,
        confidence=0.85,
        provider="fixture",
        admin_district="kalamaja",
        admin_settlement="tallinn",
        admin_region="harju maakond",
        admin_country="EE",
    )
    detail = GeoDetail(
        address=GeoDetailAddress(district="mustamäe"),
    )
    merged = merge_client_geo_detail(provider, detail, merge=True)
    assert merged is not None
    assert merged.admin_district == "mustamäe"
    assert merged.admin_settlement == "tallinn"
    assert merged.latitude == 59.448


def test_merge_client_coords_on_provider_miss() -> None:
    detail = GeoDetail(latitude=59.4, longitude=24.7, normalized_label="client-pin")
    merged = merge_client_geo_detail(None, detail, merge=True)
    assert merged is not None
    assert merged.provider == "client"
    assert merged.normalized_label == "client-pin"


def test_merge_address_only_does_not_invent_coords() -> None:
    detail = GeoDetail(address=GeoDetailAddress(street="Pikk", house="12"))
    assert merge_client_geo_detail(None, detail, merge=True) is None


def test_missing_geo_intake_fails_loader(tmp_path: Path) -> None:
    src = PACKS_ROOT / "legal_process" / "v1"
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    manifest = (src / "pack.json").read_text(encoding="utf-8")
    import json

    raw = json.loads(manifest)
    del raw["geo_intake"]
    (dest / "pack.json").write_text(json.dumps(raw), encoding="utf-8")
    (dest / "payload.schema.json").write_text(
        (src / "payload.schema.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    with pytest.raises(UnsupportedVersionError, match="geo_intake"):
        load_pack(dest, SchemaRef("legal_process", "v1"))
