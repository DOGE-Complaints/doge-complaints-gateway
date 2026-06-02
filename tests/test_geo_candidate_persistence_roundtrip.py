from __future__ import annotations

from core.application import StoryIntakeService
from core.domain import StoryGeoSnapshot
from core.geo import GeoResolverChain, GeoResolverPolicy, GeoService, InMemoryGeoCacheRepository, InMemoryGeoMetrics
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteIssueCandidateStore, SqliteStoryRepository
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus


class _GeoProvider:
    provider_id = "tc_geo_provider"

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        if canonical_key != "tallinn":
            return None
        return StoryGeoSnapshot(
            normalized_label="Tallinn, EE",
            latitude=59.437,
            longitude=24.7536,
            confidence=0.92,
            provider=self.provider_id,
            cluster_tags=("capital", "urban"),
        )


def _geo_service() -> GeoService:
    metrics = InMemoryGeoMetrics()
    return GeoService(
        cache=InMemoryGeoCacheRepository(),
        resolver=GeoResolverChain(
            providers=(_GeoProvider(),),
            policy=GeoResolverPolicy(max_attempts_per_provider=1),
            metrics=metrics,
        ),
        metrics=metrics,
    )


def test_geo_snapshot_roundtrip_persists_on_story_record() -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=_geo_service(),
    )
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "geo-roundtrip-user", "identity_issuer": "https://idp.example.com/eid"},
            "narrative": {
            "original_text": "Street condition issue near center.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Street condition issue"},
            "description": {"et": "d", "ru": "d", "en": "Street condition issue near center."},
                "location_query": "Tallinn",
            },
        }
    )

    saved = service.create_story(request).story

    assert saved.geo is not None
    assert saved.geo.normalized_label == "Tallinn, EE"
    assert saved.geo.provider == "tc_geo_provider"
    assert saved.geo.cluster_tags == ("capital", "urban")


def test_geo_admin_fields_survive_sqlite_roundtrip() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    snapshot = StoryGeoSnapshot(
        normalized_label="Tallinn, EE",
        latitude=59.437,
        longitude=24.7536,
        confidence=0.88,
        provider="stub",
        cluster_tags=("place:tallinn",),
        admin_district="kalamaja",
        admin_settlement="tallinn",
        admin_region="harju maakond",
        admin_country="EE",
    )
    record = make_story_record(story_id="sqlite-geo-admin-roundtrip", geo=snapshot)

    repo.save_story(record)
    loaded = repo.get_story(record.story_id)

    assert loaded is not None
    assert loaded.geo is not None
    assert loaded.geo.admin_settlement == "tallinn"
    assert loaded.geo.admin_country == "EE"
    assert loaded.geo.admin_district == "kalamaja"
    assert loaded.geo.admin_region == "harju maakond"


def test_issue_candidate_sqlite_roundtrip_and_delete() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    store = SqliteIssueCandidateStore(db)
    candidate = IssueCandidateRecord(
        candidate_id="candidate-tc-p1-04",
        status=IssueCandidateStatus.READY_FOR_REVIEW,
        cluster_id="cluster:tc:p1:04",
        story_ids=("story-a", "story-b"),
        readiness_score=88,
        title="Candidate title",
    )

    saved = store.save(candidate)
    fetched = store.get(candidate.candidate_id)
    store.delete(candidate.candidate_id)
    missing = store.get(candidate.candidate_id)

    assert saved == candidate
    assert fetched is not None
    assert fetched.candidate_id == "candidate-tc-p1-04"
    assert fetched.cluster_id == "cluster:tc:p1:04"
    assert fetched.story_ids == ("story-a", "story-b")
    assert fetched.readiness_score == 88
    assert fetched.status == IssueCandidateStatus.READY_FOR_REVIEW
    assert missing is None
