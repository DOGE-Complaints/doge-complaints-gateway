"""GW-REQ57-04: manual regenerate (service-auth) — bump version → pending → nudge."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from core.application.issue_create import DERIVATION_POLICY_VERSION
from core.application.sense_brief_nudge import (
    INITIAL_GENERATION_VERSION,
    SenseBriefNudgeResult,
    SenseBriefNudgeService,
)
from core.projection.columnar_storage import apply_public_generation_keys

logger = logging.getLogger(__name__)

_V_RE = re.compile(r"^v(\d+)$", re.IGNORECASE)
_REGEN_SUFFIX_RE = re.compile(r"^(.*)\.regen(\d+)$", re.IGNORECASE)


class IssueProjectionReadWrite(Protocol):
    def save_projection(
        self,
        *,
        issue_id: str,
        status: str,
        payload: dict[str, object],
        policy_version: str,
    ) -> None: ...

    def get_projection(self, issue_id: str) -> dict[str, object] | None: ...


class SenseBriefRegenerateError(ValueError):
    """Invalid regenerate request or missing Issue."""


def bump_generation_version(current: str | None) -> str:
    """Return a new distinct generation_version (peer idempotency key)."""
    cur = (current or "").strip() or INITIAL_GENERATION_VERSION
    match = _V_RE.match(cur)
    if match:
        return f"v{int(match.group(1)) + 1}"
    suffix = _REGEN_SUFFIX_RE.match(cur)
    if suffix:
        return f"{suffix.group(1)}.regen{int(suffix.group(2)) + 1}"
    return f"{cur}.regen2"


def mark_regenerate_pending(
    payload: Mapping[str, Any],
    *,
    generation_version: str,
) -> dict[str, Any]:
    """Set pending + new version; keep brief title/summary until new bind.

    Public ``poster_url`` is omitted while not ready (operator lock via
    ``apply_public_generation_keys``).
    """
    out = dict(payload)
    out["generation_status"] = "pending"
    out["generation_version"] = generation_version.strip() or bump_generation_version(
        None
    )
    out.pop("generation_reason_class", None)
    # Keep title/summary (brief wins until new bind overwrites).
    return apply_public_generation_keys(out)


@dataclass(frozen=True)
class SenseBriefRegenerateResult:
    issue_id: str
    generation_version: str
    projection: dict[str, Any]
    nudge: SenseBriefNudgeResult


@dataclass(frozen=True)
class SenseBriefRegenerateService:
    store: IssueProjectionReadWrite
    nudge_service: SenseBriefNudgeService

    def regenerate(self, *, issue_id: str) -> SenseBriefRegenerateResult:
        iid = issue_id.strip()
        if not iid:
            raise SenseBriefRegenerateError("issue_id is required.")
        existing = self.store.get_projection(iid)
        if existing is None:
            raise SenseBriefRegenerateError(f"Unknown issue_id: {iid}.")

        previous = str(existing.get("generation_version") or "").strip()
        new_version = bump_generation_version(previous)
        if new_version == previous:
            new_version = f"{previous}.regen2"

        row_status = str(existing.get("status") or "PUBLISHED")
        pending_payload = mark_regenerate_pending(
            existing, generation_version=new_version
        )
        self.store.save_projection(
            issue_id=iid,
            status=row_status,
            payload=pending_payload,
            policy_version=DERIVATION_POLICY_VERSION,
        )
        saved = self.store.get_projection(iid)
        assert saved is not None

        nudge = self.nudge_service.nudge(
            issue_id=iid,
            generation_version=new_version,
        )
        logger.info(
            "sense_brief_regenerate.applied issue_id=%s previous_version=%s "
            "generation_version=%s nudge_succeeded=%s",
            iid,
            previous or None,
            new_version,
            nudge.succeeded,
        )
        return SenseBriefRegenerateResult(
            issue_id=iid,
            generation_version=new_version,
            projection=dict(saved),
            nudge=nudge,
        )
