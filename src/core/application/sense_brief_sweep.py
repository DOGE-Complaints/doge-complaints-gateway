"""GW-REQ57-03: sweep eligible Issues and re-nudge (no ready overwrite, no version bump)."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Mapping, Protocol

from core.application.sense_brief_nudge import (
    INITIAL_GENERATION_VERSION,
    SenseBriefNudgeResult,
    SenseBriefNudgeService,
)

logger = logging.getLogger(__name__)

SWEEP_ELIGIBLE_STATUSES: frozenset[str] = frozenset({"pending", "failed"})
READY_STATUS = "ready"


class SenseBriefSweepProjectionSource(Protocol):
    def list_projections(self, **kwargs: Any) -> list[dict[str, object]]: ...

    def get_projection(self, issue_id: str) -> dict[str, object] | None: ...


@dataclass(frozen=True)
class SweepEligibleIssue:
    issue_id: str
    generation_status: str
    generation_version: str


@dataclass(frozen=True)
class SenseBriefSweepRunResult:
    eligible_count: int
    nudged_count: int
    skipped_ready_count: int
    nudge_results: tuple[SenseBriefNudgeResult, ...]


def generation_status_of(payload: Mapping[str, Any]) -> str | None:
    raw = payload.get("generation_status")
    if raw is None:
        return None
    text = str(raw).strip().lower()
    return text or None


def generation_version_of(payload: Mapping[str, Any]) -> str:
    raw = payload.get("generation_version")
    if raw is None:
        return INITIAL_GENERATION_VERSION
    text = str(raw).strip()
    return text or INITIAL_GENERATION_VERSION


def is_sweep_eligible(payload: Mapping[str, Any]) -> bool:
    """True only for pending/failed lacking successful brief apply — never ready."""
    status = generation_status_of(payload)
    if status is None:
        return False
    if status == READY_STATUS:
        return False
    return status in SWEEP_ELIGIBLE_STATUSES


def list_sweep_eligible_issues(
    store: SenseBriefSweepProjectionSource,
) -> list[SweepEligibleIssue]:
    """Select Issues with generation_status pending|failed (AC / arch 02 §2.4)."""
    eligible: list[SweepEligibleIssue] = []
    for row in store.list_projections():
        if not is_sweep_eligible(row):
            continue
        issue_id = str(row.get("id") or row.get("issue_id") or "").strip()
        if not issue_id:
            continue
        status = generation_status_of(row)
        assert status is not None
        eligible.append(
            SweepEligibleIssue(
                issue_id=issue_id,
                generation_status=status,
                generation_version=generation_version_of(row),
            )
        )
    return eligible


@dataclass(frozen=True)
class SenseBriefSweepService:
    """One-shot sweep: re-nudge eligible Issues; never overwrite ready with alpha."""

    store: SenseBriefSweepProjectionSource
    nudge_service: SenseBriefNudgeService

    def run_once(self) -> SenseBriefSweepRunResult:
        eligible = list_sweep_eligible_issues(self.store)
        nudge_results: list[SenseBriefNudgeResult] = []
        nudged = 0
        skipped_ready = 0

        for item in eligible:
            live = self.store.get_projection(item.issue_id)
            if live is None:
                continue
            # T04 / AC-02: re-check ready so we never silently replace a ready brief.
            if generation_status_of(live) == READY_STATUS:
                skipped_ready += 1
                logger.info(
                    "sense_brief_sweep.skip_ready issue_id=%s",
                    item.issue_id,
                )
                continue
            if not is_sweep_eligible(live):
                continue

            version = generation_version_of(live)
            result = self.nudge_service.nudge(
                issue_id=item.issue_id,
                generation_version=version,
                corpus=None,
            )
            nudge_results.append(result)
            if result.attempted:
                nudged += 1
            logger.info(
                "sense_brief_sweep.nudge issue_id=%s generation_version=%s "
                "attempted=%s succeeded=%s skip_reason=%s",
                item.issue_id,
                version,
                result.attempted,
                result.succeeded,
                result.skip_reason,
            )

        return SenseBriefSweepRunResult(
            eligible_count=len(eligible),
            nudged_count=nudged,
            skipped_ready_count=skipped_ready,
            nudge_results=tuple(nudge_results),
        )


def assert_ready_payload_unchanged(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
) -> None:
    """Test helper claim: ready brief fields must survive a sweep pass."""
    assert generation_status_of(before) == READY_STATUS
    assert generation_status_of(after) == READY_STATUS
    assert before.get("poster_url") == after.get("poster_url")
    assert generation_version_of(before) == generation_version_of(after)
