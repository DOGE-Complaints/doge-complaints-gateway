"""GW-SSR-02: schema/profile binding + structured_payload persist."""

from __future__ import annotations

import inspect
from pathlib import Path

from core.application import StoryIntakeService
from core.cluster.types import ClusterLens
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure.db_supabase import REQUIRED_READINESS_TABLES, SupabaseDatabase
from core.intake import parse_story_intake_request
from core.intake.contracts import INTAKE_SCHEMA_VERSION, StoryIntakeRequest
from core.schema.payload import authoritative_payload_hash, payload_hash_for
from tests.intake_v2_fixtures import make_story_record, valid_v2_intake_payload

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
CLUSTERLENS_BASELINE = (
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
)
LEGAL_PAYLOAD = {"institution": {"office_id": "s1", "name": "Tallinn"}}
MOBILITY_PAYLOAD = {"route_id": "t1", "stop_id": "n2"}


def _sqlite_repo() -> SqliteStoryRepository:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    return SqliteStoryRepository(db)


def _bound_record(*, story_id: str, schema_id: str, payload: dict[str, object]) -> StoryRecord:
    return make_story_record(
        story_id=story_id,
        schema_id=schema_id,
        bound_schema_version="v1",
        profile_id="default",
        profile_version="1",
        structured_payload=payload,
        payload_hash="client-supplied-must-be-ignored",
    )


def test_clusterlens_baseline_unchanged() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE


def test_payload_hash_is_deterministic_canonical_json() -> None:
    first = payload_hash_for(LEGAL_PAYLOAD)
    nested_reordered = payload_hash_for({"institution": {"name": "Tallinn", "office_id": "s1"}})
    assert first == nested_reordered
    assert first != payload_hash_for(MOBILITY_PAYLOAD)
    assert len(first) == 64
    assert first != "client-supplied-must-be-ignored"


def test_two_payloads_same_sqlite_table() -> None:
    repo = _sqlite_repo()
    legal = _bound_record(story_id="ssr02-legal", schema_id="legal_process", payload=LEGAL_PAYLOAD)
    mobility = _bound_record(
        story_id="ssr02-mobility", schema_id="mobility_observation", payload=MOBILITY_PAYLOAD
    )
    repo.save_story(legal)
    repo.save_story(mobility)

    fetched_legal = repo.get_story("ssr02-legal")
    fetched_mobility = repo.get_story("ssr02-mobility")
    assert fetched_legal is not None
    assert fetched_mobility is not None
    assert fetched_legal.schema_id == "legal_process"
    assert fetched_mobility.schema_id == "mobility_observation"
    assert fetched_legal.bound_schema_version == "v1"
    assert fetched_legal.structured_payload == LEGAL_PAYLOAD
    assert fetched_mobility.structured_payload == MOBILITY_PAYLOAD
    assert fetched_legal.payload_hash == payload_hash_for(LEGAL_PAYLOAD)
    assert fetched_mobility.payload_hash == payload_hash_for(MOBILITY_PAYLOAD)
    assert fetched_legal.schema_version == INTAKE_SCHEMA_VERSION
    assert fetched_mobility.schema_version == INTAKE_SCHEMA_VERSION


def test_sqlite_and_memory_roundtrip_and_upsert() -> None:
    sqlite_repo = _sqlite_repo()
    memory_repo = InMemoryStoryRepository()
    original = _bound_record(
        story_id="ssr02-roundtrip", schema_id="legal_process", payload=LEGAL_PAYLOAD
    )
    sqlite_returned = sqlite_repo.save_story(original)
    memory_returned = memory_repo.save_story(original)

    sqlite_fetched = sqlite_repo.get_story("ssr02-roundtrip")
    memory_fetched = memory_repo.get_story("ssr02-roundtrip")
    assert sqlite_fetched is not None
    assert memory_fetched is not None
    digest = payload_hash_for(LEGAL_PAYLOAD)
    assert sqlite_returned.payload_hash == digest
    assert memory_returned.payload_hash == digest
    assert sqlite_returned.payload_hash != original.payload_hash
    assert sqlite_fetched.payload_hash == digest
    assert memory_fetched.payload_hash == digest
    assert sqlite_fetched.payload_hash != "client-supplied-must-be-ignored"
    assert memory_fetched.profile_id == "default"
    assert memory_fetched.profile_version == "1"

    updated = make_story_record(
        story_id="ssr02-roundtrip",
        schema_id="legal_process",
        bound_schema_version="v1",
        profile_id="default",
        profile_version="1",
        structured_payload=MOBILITY_PAYLOAD,
        payload_hash="stale-client-hash",
    )
    returned_updated = sqlite_repo.save_story(updated)
    assert returned_updated.payload_hash == payload_hash_for(MOBILITY_PAYLOAD)
    assert returned_updated.payload_hash != "stale-client-hash"
    refetched = sqlite_repo.get_story("ssr02-roundtrip")
    assert refetched is not None
    assert refetched.structured_payload == MOBILITY_PAYLOAD
    assert refetched.payload_hash == payload_hash_for(MOBILITY_PAYLOAD)


def test_sqlite_save_story_return_uses_authoritative_hash() -> None:
    repo = _sqlite_repo()
    original = _bound_record(
        story_id="ssr02-return-hash", schema_id="legal_process", payload=LEGAL_PAYLOAD
    )
    assert original.payload_hash == "client-supplied-must-be-ignored"
    returned = repo.save_story(original)
    digest = authoritative_payload_hash(LEGAL_PAYLOAD)
    assert digest == payload_hash_for(LEGAL_PAYLOAD)
    assert returned.payload_hash == digest
    assert returned.payload_hash != original.payload_hash
    assert original.payload_hash == "client-supplied-must-be-ignored"


def test_civic_save_all_none_binding_stays_green() -> None:
    sqlite_repo = _sqlite_repo()
    memory_repo = InMemoryStoryRepository()
    civic = make_story_record(story_id="ssr02-civic")
    assert civic.schema_id is None
    assert civic.bound_schema_version is None
    assert civic.profile_id is None
    assert civic.profile_version is None
    assert civic.structured_payload is None
    assert civic.payload_hash is None

    sqlite_repo.save_story(civic)
    memory_repo.save_story(civic)
    sqlite_fetched = sqlite_repo.get_story("ssr02-civic")
    memory_fetched = memory_repo.get_story("ssr02-civic")
    assert sqlite_fetched is not None
    assert memory_fetched is not None
    assert sqlite_fetched.schema_id is None
    assert sqlite_fetched.bound_schema_version is None
    assert sqlite_fetched.structured_payload is None
    assert sqlite_fetched.payload_hash is None
    assert sqlite_fetched.schema_version == INTAKE_SCHEMA_VERSION
    assert memory_fetched.schema_version == INTAKE_SCHEMA_VERSION


def test_civic_intake_create_leaves_binding_none() -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    saved = service.create_story(parse_story_intake_request(valid_v2_intake_payload())).story
    assert saved.schema_version == INTAKE_SCHEMA_VERSION
    assert saved.schema_id is None
    assert saved.bound_schema_version is None
    assert saved.structured_payload is None
    assert saved.payload_hash is None


def test_lifecycle_advance_keeps_binding() -> None:
    repository = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repository,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    accepted = repository.save_story(
        make_story_record(
            story_id="ssr02-lifecycle",
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            schema_id="legal_process",
            bound_schema_version="v1",
            profile_id="default",
            profile_version="1",
            structured_payload=LEGAL_PAYLOAD,
            payload_hash=payload_hash_for(LEGAL_PAYLOAD),
        )
    )
    advanced = service.advance_story_readiness(
        story_id=accepted.story_id, narrative_complete=True
    )
    assert advanced.lifecycle_status == StoryLifecycleStatus.READY_FOR_PROFILE
    assert advanced.schema_id == "legal_process"
    assert advanced.bound_schema_version == "v1"
    assert advanced.profile_id == "default"
    assert advanced.profile_version == "1"
    assert advanced.structured_payload == LEGAL_PAYLOAD
    assert advanced.payload_hash == payload_hash_for(LEGAL_PAYLOAD)
    assert advanced.schema_version == INTAKE_SCHEMA_VERSION


def test_sqlite_alter_adds_binding_columns_without_create_rewrite() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    cols = {row[1] for row in db.connection.execute("PRAGMA table_info(stories)").fetchall()}
    for name in (
        "schema_id",
        "bound_schema_version",
        "profile_id",
        "profile_version",
        "structured_payload",
        "payload_hash",
    ):
        assert name in cols
    assert "envelope_version" not in cols
    src = (GATEWAY_ROOT / "src" / "core" / "infrastructure" / "db_sqlite.py").read_text(
        encoding="utf-8"
    )
    create_start = src.index("CREATE TABLE IF NOT EXISTS stories")
    alter_start = src.index("def _ensure_sqlite_schema_migrations")
    create_block = src[create_start:alter_start]
    assert "bound_schema_version" not in create_block
    assert "structured_payload" not in create_block
    assert "ALTER TABLE stories ADD COLUMN bound_schema_version" in src
    assert "ON CONFLICT(story_id) DO UPDATE SET" in src
    assert "bound_schema_version = excluded.bound_schema_version" in src


def test_intake_parser_has_no_schema_binding() -> None:
    assert "schema_binding" not in StoryIntakeRequest.__dataclass_fields__
    contracts = (GATEWAY_ROOT / "src" / "core" / "intake" / "contracts.py").read_text(
        encoding="utf-8"
    )
    init_mod = (GATEWAY_ROOT / "src" / "core" / "intake" / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert "schema_binding" not in contracts
    assert "schema_binding" not in init_mod


def test_readiness_probe_does_not_require_binding_columns() -> None:
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for token in (
        "schema_id",
        "bound_schema_version",
        "profile_id",
        "profile_version",
        "structured_payload",
        "payload_hash",
    ):
        assert token not in source
    assert "story_dimensions" not in REQUIRED_READINESS_TABLES
