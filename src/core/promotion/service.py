from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from core.promotion.gates import PromotionGatePolicy, evaluate_promotion_gates
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
    IssueCandidateStore,
    ReviewAuditLogRepository,
)
from core.promotion.types import (
    IssueCandidateRecord,
    IssueCandidateStatus,
    ReviewAuditEntry,
    ReviewDecision,
)


class PromotionStateError(ValueError):
    """Raised when an issue candidate transition is invalid."""


def _require_transition(current: IssueCandidateStatus, expected: IssueCandidateStatus) -> None:
    if current != expected:
        raise PromotionStateError(f"Invalid state: expected {expected.value}, got {current.value}.")


@dataclass
class IssuePromotionService:
    candidates: IssueCandidateStore
    audit_log: ReviewAuditLogRepository
    gate_policy: PromotionGatePolicy

    @classmethod
    def baseline(
        cls,
        *,
        candidates: IssueCandidateStore | None = None,
        audit_log: ReviewAuditLogRepository | None = None,
        gate_policy: PromotionGatePolicy | None = None,
    ) -> IssuePromotionService:
        return cls(
            candidates=candidates or InMemoryIssueCandidateStore(),
            audit_log=audit_log or InMemoryReviewAuditLogRepository(),
            gate_policy=gate_policy or PromotionGatePolicy(),
        )

    def _get(self, candidate_id: str) -> IssueCandidateRecord:
        record = self.candidates.get(candidate_id)
        if record is None:
            raise PromotionStateError(f"Unknown candidate_id: {candidate_id}.")
        return record

    def create_candidate(
        self,
        *,
        cluster_id: str,
        story_ids: tuple[str, ...],
        readiness_score: int,
        title: str,
    ) -> IssueCandidateRecord:
        candidate = IssueCandidateRecord(
            candidate_id=str(uuid4()),
            status=IssueCandidateStatus.DRAFT,
            cluster_id=cluster_id,
            story_ids=story_ids,
            readiness_score=readiness_score,
            title=title,
        )
        self.candidates.save(candidate)
        return candidate

    def submit_for_review(
        self,
        candidate_id: str,
        *,
        cluster_canonical_types: tuple[str, ...] | None = None,
    ) -> IssueCandidateRecord:
        current = self._get(candidate_id)
        _require_transition(current.status, IssueCandidateStatus.DRAFT)
        gate = evaluate_promotion_gates(
            current,
            self.gate_policy,
            cluster_canonical_types=cluster_canonical_types,
        )
        if not gate.passed:
            raise PromotionStateError("Promotion gates failed: " + ",".join(gate.reasons))

        updated = IssueCandidateRecord(
            candidate_id=current.candidate_id,
            status=IssueCandidateStatus.READY_FOR_REVIEW,
            cluster_id=current.cluster_id,
            story_ids=current.story_ids,
            readiness_score=current.readiness_score,
            title=current.title,
        )
        self.candidates.save(updated)
        return updated

    def start_review(self, candidate_id: str) -> IssueCandidateRecord:
        current = self._get(candidate_id)
        _require_transition(current.status, IssueCandidateStatus.READY_FOR_REVIEW)
        updated = IssueCandidateRecord(
            candidate_id=current.candidate_id,
            status=IssueCandidateStatus.IN_REVIEW,
            cluster_id=current.cluster_id,
            story_ids=current.story_ids,
            readiness_score=current.readiness_score,
            title=current.title,
        )
        self.candidates.save(updated)
        return updated

    def record_review(
        self,
        *,
        candidate_id: str,
        actor: str,
        decision: ReviewDecision,
        rationale: str,
    ) -> IssueCandidateRecord:
        current = self._get(candidate_id)
        _require_transition(current.status, IssueCandidateStatus.IN_REVIEW)

        next_status = (
            IssueCandidateStatus.PROMOTED
            if decision == ReviewDecision.APPROVE
            else IssueCandidateStatus.REJECTED
        )
        updated = IssueCandidateRecord(
            candidate_id=current.candidate_id,
            status=next_status,
            cluster_id=current.cluster_id,
            story_ids=current.story_ids,
            readiness_score=current.readiness_score,
            title=current.title,
        )
        self.candidates.save(updated)
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=candidate_id,
                actor=actor,
                decision=decision,
                rationale=rationale,
                related_cluster_id=current.cluster_id,
                related_story_ids=current.story_ids,
            )
        )
        return updated

    def extend_candidate(
        self,
        candidate_id: str,
        *,
        additional_story_ids: tuple[str, ...],
        new_readiness_score: int,
    ) -> IssueCandidateRecord:
        current = self._get(candidate_id)
        _require_transition(current.status, IssueCandidateStatus.PROMOTED)

        merged_story_ids = tuple(
            sorted(set(current.story_ids).union(set(additional_story_ids)))
        )
        updated = IssueCandidateRecord(
            candidate_id=current.candidate_id,
            status=current.status,
            cluster_id=current.cluster_id,
            story_ids=merged_story_ids,
            readiness_score=new_readiness_score,
            title=current.title,
        )
        self.candidates.save(updated)
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=candidate_id,
                actor="system",
                decision=ReviewDecision.APPROVE,
                rationale="cluster_growth_extend",
                related_cluster_id=current.cluster_id,
                related_story_ids=additional_story_ids,
            )
        )
        return updated

    def merge_candidates(self, primary_id: str, secondary_id: str) -> IssueCandidateRecord:
        primary = self._get(primary_id)
        secondary = self._get(secondary_id)
        if primary.status != IssueCandidateStatus.DRAFT or secondary.status != IssueCandidateStatus.DRAFT:
            raise PromotionStateError("Merge supported only for draft candidates in baseline.")

        merged_stories = tuple(sorted(set(primary.story_ids).union(set(secondary.story_ids))))
        merged = IssueCandidateRecord(
            candidate_id=primary.candidate_id,
            status=IssueCandidateStatus.DRAFT,
            cluster_id=primary.cluster_id,
            story_ids=merged_stories,
            readiness_score=max(primary.readiness_score, secondary.readiness_score),
            title=f"{primary.title} + {secondary.title}",
        )
        self.candidates.save(merged)
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=primary_id,
                actor="system",
                decision=ReviewDecision.APPROVE,
                rationale=f"merged_candidate:{secondary_id}",
                related_cluster_id=merged.cluster_id,
                related_story_ids=merged.story_ids,
            )
        )
        self.candidates.delete(secondary_id)
        return merged

    def split_candidate(self, candidate_id: str) -> tuple[IssueCandidateRecord, IssueCandidateRecord]:
        current = self._get(candidate_id)
        if current.status != IssueCandidateStatus.DRAFT:
            raise PromotionStateError("Split supported only for draft candidates in baseline.")
        if len(current.story_ids) < 2:
            raise PromotionStateError("Need at least two stories to split.")

        left_stories = (current.story_ids[0],)
        right_stories = tuple(current.story_ids[1:])
        left = IssueCandidateRecord(
            candidate_id=str(uuid4()),
            status=IssueCandidateStatus.DRAFT,
            cluster_id=current.cluster_id,
            story_ids=left_stories,
            readiness_score=current.readiness_score,
            title=f"{current.title} (split-a)",
        )
        right = IssueCandidateRecord(
            candidate_id=str(uuid4()),
            status=IssueCandidateStatus.DRAFT,
            cluster_id=current.cluster_id,
            story_ids=right_stories,
            readiness_score=current.readiness_score,
            title=f"{current.title} (split-b)",
        )
        self.candidates.delete(candidate_id)
        self.candidates.save(left)
        self.candidates.save(right)
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=left.candidate_id,
                actor="system",
                decision=ReviewDecision.APPROVE,
                rationale=f"split_from:{candidate_id}",
                related_cluster_id=current.cluster_id,
                related_story_ids=left.story_ids,
            )
        )
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=right.candidate_id,
                actor="system",
                decision=ReviewDecision.APPROVE,
                rationale=f"split_from:{candidate_id}",
                related_cluster_id=current.cluster_id,
                related_story_ids=right.story_ids,
            )
        )
        return left, right

    def reframe_title(self, candidate_id: str, new_title: str) -> IssueCandidateRecord:
        current = self._get(candidate_id)
        if current.status != IssueCandidateStatus.DRAFT:
            raise PromotionStateError("Reframe supported only for draft candidates in baseline.")
        updated = IssueCandidateRecord(
            candidate_id=current.candidate_id,
            status=current.status,
            cluster_id=current.cluster_id,
            story_ids=current.story_ids,
            readiness_score=current.readiness_score,
            title=new_title.strip(),
        )
        self.candidates.save(updated)
        self.audit_log.append(
            ReviewAuditEntry(
                candidate_id=candidate_id,
                actor="moderator",
                decision=ReviewDecision.APPROVE,
                rationale="reframe_title",
                related_cluster_id=current.cluster_id,
                related_story_ids=current.story_ids,
            )
        )
        return updated

    def audit_trail(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        return self.audit_log.list_for_candidate(candidate_id)
