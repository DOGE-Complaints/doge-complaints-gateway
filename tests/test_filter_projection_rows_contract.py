"""REQ-39 Zone M: filter_projection_rows() filter engine contract."""

from __future__ import annotations

from core.projection.read_filters import filter_projection_rows, normalize_geo_token


def _row(
    issue_id: str,
    *,
    status: str = "PUBLISHED",
    issue_type: str = "INCIDENT",
    labels: list[str] | None = None,
    institution: str | dict[str, str] | None = None,
    geo: dict[str, object] | None = None,
    created_at: str = "2026-05-01T00:00:00+00:00",
) -> tuple[str, dict[str, object], str]:
    payload: dict[str, object] = {
        "id": issue_id,
        "status": status,
        "type": issue_type,
        "labels": labels or [],
        "institution": institution if institution is not None else "",
    }
    if geo is not None:
        payload["geo"] = geo
    return (status, payload, created_at)


def test_m01_empty_status_list_returns_all() -> None:
    rows = [
        _row("a", status="PUBLISHED"),
        _row("b", status="DRAFT"),
    ]
    result = filter_projection_rows(rows, status=[])
    assert len(result) == 2


def test_m02_issue_type_filter_exact_match() -> None:
    rows = [
        _row("a", issue_type="IMPROVEMENT"),
        _row("b", issue_type="BUG"),
    ]
    result = filter_projection_rows(rows, issue_type="IMPROVEMENT")
    ids = {str(r["id"]) for r in result}
    assert ids == {"a"}


def test_m03_labels_filter_or_semantics() -> None:
    rows = [
        _row("a", labels=["infrastructure", "transport"]),
        _row("b", labels=["waste"]),
        _row("c", labels=["safety"]),
    ]
    result = filter_projection_rows(rows, labels=["infrastructure", "waste"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"a", "b"}


def test_m04_institution_filter_exact_match() -> None:
    rows = [
        _row(
            "a",
            institution={
                "et": "tallinn-city",
                "ru": "tallinn-city",
                "en": "tallinn-city",
            },
        ),
        _row(
            "b",
            institution={
                "et": "state-roads",
                "ru": "state-roads",
                "en": "state-roads",
            },
        ),
    ]
    result = filter_projection_rows(rows, institution="tallinn-city")
    ids = {str(r["id"]) for r in result}
    assert ids == {"a"}


def test_m05_temporal_filters_boundary_conditions() -> None:
    rows = [
        _row("exact", created_at="2026-05-01T00:00:00+00:00"),
        _row("after", created_at="2026-05-02T00:00:00+00:00"),
        _row("before", created_at="2026-04-30T00:00:00+00:00"),
    ]
    result_after = filter_projection_rows(rows, created_after="2026-05-01T00:00:00+00:00")
    ids_after = {str(r["id"]) for r in result_after}
    assert "after" in ids_after
    assert "before" not in ids_after

    result_before = filter_projection_rows(rows, created_before="2026-05-01T00:00:00+00:00")
    ids_before = {str(r["id"]) for r in result_before}
    assert "before" in ids_before
    assert "after" not in ids_before


def test_m06_geo_null_excluded_when_bbox_active() -> None:
    rows = [
        _row("no-geo", geo=None),
        _row("with-geo", geo={"lat": 59.44, "lon": 24.75}),
    ]
    result = filter_projection_rows(rows, geo_lat_min=59.0)
    ids = {str(r["id"]) for r in result}
    assert "with-geo" in ids
    assert "no-geo" not in ids


def test_m07_bbox_and_district_and_semantics() -> None:
    rows = [
        _row(
            "match",
            geo={"lat": 59.44, "lon": 24.75, "district": "põhjatallinn"},
        ),
        _row(
            "wrong-district",
            geo={"lat": 59.44, "lon": 24.75, "district": "mustamäe"},
        ),
        _row(
            "outside-bbox",
            geo={"lat": 58.0, "lon": 24.75, "district": "põhjatallinn"},
        ),
    ]
    result = filter_projection_rows(
        rows,
        geo_lat_min=59.0,
        geo_district=["põhja-tallinn"],
    )
    ids = {str(r["id"]) for r in result}
    assert ids == {"match"}


def test_m08_district_multi_value_or_semantics() -> None:
    rows = [
        _row("dist-a", geo={"district": "põhjatallinn"}),
        _row("dist-b", geo={"district": "mustamäe"}),
        _row("dist-c", geo={"district": "kesklinn"}),
    ]
    result = filter_projection_rows(rows, geo_district=["põhja-tallinn", "mustamäe"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"dist-a", "dist-b"}


def test_m09_geo_settlement_filter_or_semantics() -> None:
    rows = [
        _row("settle-a", geo={"settlement": "Tallinn"}),
        _row("settle-b", geo={"settlement": "Tartu"}),
        _row("settle-c", geo={"settlement": "Narva"}),
    ]
    result = filter_projection_rows(rows, geo_settlement=["tallinn", "tartu"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"settle-a", "settle-b"}
    assert normalize_geo_token("Tallinn") == normalize_geo_token("tallinn")


def test_m10_geo_region_filter() -> None:
    rows = [
        _row("region-a", geo={"region": "Harju maakond"}),
        _row("region-b", geo={"region": "Tartu maakond"}),
    ]
    result = filter_projection_rows(rows, geo_region=["harju maakond"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"region-a"}


def test_m11_geo_country_filter() -> None:
    rows = [
        _row("country-ee", geo={"country": "EE"}),
        _row("country-fi", geo={"country": "FI"}),
    ]
    result = filter_projection_rows(rows, geo_country=["ee"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"country-ee"}


def test_m12_geo_postal_code_filter() -> None:
    rows = [
        _row("postal-a", geo={"postal_code": "10145"}),
        _row("postal-b", geo={"postal_code": "51003"}),
        _row("postal-c", geo={"postal_code": ""}),
    ]
    result = filter_projection_rows(rows, geo_postal_code=["10145"])
    ids = {str(r["id"]) for r in result}
    assert ids == {"postal-a"}
