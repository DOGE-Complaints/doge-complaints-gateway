from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from core.redaction import redact_pii
from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.application.services import StoryIntakeService, _canonical_story_embedding_source
from core.cluster import ClusteringEngine
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryIdempotencyRepository,
    InMemoryStoryRepository,
)
from core.intake import parse_story_intake_request
from core.logging_setup import StoryDebugLogger, configure_logging, open_story_debug_logger
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict


def test_redact_pii_true_returns_redacted() -> None:
    assert redact_pii("secret narrative", True) == "[REDACTED]"


def test_redact_pii_false_returns_original() -> None:
    assert redact_pii("open narrative", False) == "open narrative"


def test_story_debug_logger_no_op_without_dir() -> None:
    with open_story_debug_logger("story-no-dir", None) as logger:
        logger.log("intake", "story_accepted", {"lifecycle": "ACCEPTED"})
    assert True


def test_story_debug_logger_writes_jsonl(tmp_path: Path) -> None:
    story_id = "story-jsonl-001"
    with open_story_debug_logger(story_id, str(tmp_path)) as logger:
        logger.log("intake", "story_accepted", {"lifecycle": "READY_FOR_PROFILE"})
    log_file = tmp_path / f"{story_id}.jsonl"
    assert log_file.is_file()
    line = json.loads(log_file.read_text(encoding="utf-8").strip())
    assert line["stage"] == "intake"
    assert line["event"] == "story_accepted"
    assert line["story_id"] == story_id


def test_embedding_source_redacts_pii_text() -> None:
    story = make_story_record(
        narrative_original_text="PII secret line",
        privacy_contains_pii=True,
    )
    source = _canonical_story_embedding_source(story)
    assert "PII secret line" not in source
    assert "text=[REDACTED]" in source


def test_intake_debug_jsonl_five_stages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    configure_logging("INFO", log_debug_dir=str(tmp_path))

    stories = InMemoryStoryRepository()
    intake = StoryIntakeService(
        repository=stories,
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
        log_debug_dir=str(tmp_path),
    )
    payload = intake_payload_simple(
        original_text="Street light broken near district center.",
        title_en="Broken light",
    )
    payload["narrative"]["canonical_type"] = "complaint"
    payload["narrative"]["canonical_labels"] = ["roads", "broken_infrastructure"]
    created = intake.create_story(parse_story_intake_request(payload))
    story_id = created.story.story_id

    stories.save_story(
        make_story_record(
            story_id="s2",
            narrative_original_text="street light still broken in same district",
            submitter_external_user_id="user-s2",
            narrative_title=narrative_dict(en="Street light issue"),
            narrative_canonical_type="complaint",
            narrative_canonical_labels=("roads", "broken_infrastructure"),
        )
    )

    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
        log_debug_dir=str(tmp_path),
    )
    assert orchestrator.process_story(story_id) is not None

    log_file = tmp_path / f"{story_id}.jsonl"
    assert log_file.is_file()
    stages = {json.loads(line)["stage"] for line in log_file.read_text(encoding="utf-8").splitlines() if line}
    assert stages >= {"intake", "geo", "signals", "cluster", "promotion"}


def test_intake_no_debug_file_when_dir_unset(tmp_path: Path) -> None:
    stories = InMemoryStoryRepository()
    intake = StoryIntakeService(
        repository=stories,
        idempotency_repository=InMemoryIdempotencyRepository(),
        log_debug_dir=None,
    )
    created = intake.create_story(
        parse_story_intake_request(intake_payload_simple())
    )
    assert not (tmp_path / f"{created.story.story_id}.jsonl").exists()


def test_debug_jsonl_independent_of_log_level(tmp_path: Path) -> None:
    configure_logging("INFO", log_debug_dir=str(tmp_path))
    assert logging.getLogger().level == logging.INFO
    with StoryDebugLogger("lvl-test", str(tmp_path)) as logger:
        logger.log("intake", "story_accepted", {})
    assert (tmp_path / "lvl-test.jsonl").is_file()
