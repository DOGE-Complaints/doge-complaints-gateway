"""GW-REQ57-01: apply aibridge bind-in payloads onto Issue projection."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from core.application.issue_create import DERIVATION_POLICY_VERSION
from core.projection.columnar_storage import apply_public_generation_keys

logger = logging.getLogger(__name__)

_FAIL_CLOSED_TITLE = {
    "et": "[Brief unavailable]",
    "ru": "[Brief unavailable]",
    "en": "[Brief unavailable]",
}
_FAIL_CLOSED_SUMMARY = {
    "et": "Sense brief failed.",
    "ru": "Sense brief failed.",
    "en": "Sense brief failed.",
}

_KNOWN_REASON_CLASSES = frozenset(
    {
        "accept_unauthorized",
        "corpus_insufficient",
        "brief_generation_failed",
        "image_generation_failed",
        "storage_upload_failed",
        "bind_rejected",
        "internal_error",
    }
)


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


class SenseBriefBindError(ValueError):
    """Invalid bind payload or missing Issue."""


def _plain_title(raw: object) -> str:
    if not isinstance(raw, str):
        raise SenseBriefBindError("apply.title must be a string.")
    title = " ".join(raw.split()).strip()
    if not title:
        raise SenseBriefBindError("apply.title must be non-empty plain text.")
    if len(title) > 80:
        raise SenseBriefBindError("apply.title must be ≤80 characters.")
    return title


def _i18n_summary(raw: object) -> dict[str, str]:
    if not isinstance(raw, dict) or not raw:
        raise SenseBriefBindError("apply.summary must be a non-empty i18n object.")
    out: dict[str, str] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise SenseBriefBindError("apply.summary values must be strings.")
        text = value.strip()
        if text:
            out[key] = text
    if not out:
        raise SenseBriefBindError("apply.summary must include at least one locale.")
    return out


def preserve_brief_wins_fields(
    *,
    new_payload: Mapping[str, Any],
    existing: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """After ready, dominant Story must not overwrite brief title/summary (AC-06)."""
    out = dict(new_payload)
    if existing is None:
        return out
    if existing.get("generation_status") != "ready":
        return out
    title = existing.get("title")
    summary = existing.get("summary")
    if isinstance(title, dict):
        out["title"] = dict(title)
    if isinstance(summary, dict):
        out["summary"] = dict(summary)
    for key in (
        "generation_status",
        "generation_version",
        "poster_url",
    ):
        if key in existing and existing[key] is not None:
            out[key] = existing[key]
    return apply_public_generation_keys(out)


@dataclass(frozen=True)
class IssueSenseBriefBindService:
    store: IssueProjectionReadWrite

    def apply_bind(self, body: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(body, Mapping):
            raise SenseBriefBindError("Bind body must be an object.")
        issue_id = str(body.get("issue_id") or "").strip()
        if not issue_id:
            raise SenseBriefBindError("issue_id is required.")
        generation_version = str(body.get("generation_version") or "").strip()
        if not generation_version:
            raise SenseBriefBindError("generation_version is required.")
        outcome = str(body.get("outcome") or "").strip()
        if outcome not in ("success", "failure"):
            raise SenseBriefBindError("outcome must be success or failure.")

        existing = self.store.get_projection(issue_id)
        if existing is None:
            raise SenseBriefBindError(f"Unknown issue_id: {issue_id}.")

        payload = dict(existing)
        row_status = str(payload.get("status") or "PUBLISHED")
        reason_to_persist: str | None = None

        if outcome == "success":
            apply_raw = body.get("apply")
            if not isinstance(apply_raw, Mapping):
                raise SenseBriefBindError("success bind requires apply object.")
            poster_url = str(body.get("poster_url") or "").strip()
            if not poster_url.startswith("https://"):
                raise SenseBriefBindError("poster_url must be public https://.")
            title = _plain_title(apply_raw.get("title"))
            summary = _i18n_summary(apply_raw.get("summary"))
            payload["title"] = {"et": title, "ru": title, "en": title}
            merged_summary = {"et": title, "ru": title, "en": title}
            merged_summary.update(summary)
            payload["summary"] = merged_summary
            payload["generation_status"] = "ready"
            payload["generation_version"] = generation_version
            payload["poster_url"] = poster_url
            payload.pop("generation_reason_class", None)
        else:
            if body.get("apply") is not None or body.get("brief") is not None:
                raise SenseBriefBindError("failure bind must not include apply or brief.")
            reason_class = str(body.get("reason_class") or "").strip()
            if not reason_class:
                raise SenseBriefBindError("failure bind requires reason_class.")
            if reason_class not in _KNOWN_REASON_CLASSES:
                logger.warning(
                    "sense_brief_bind.unknown_reason_class issue_id=%s reason_class=%s",
                    issue_id,
                    reason_class,
                )
            logger.info(
                "sense_brief_bind.failure issue_id=%s generation_version=%s reason_class=%s",
                issue_id,
                generation_version,
                reason_class,
            )
            payload["title"] = dict(_FAIL_CLOSED_TITLE)
            payload["summary"] = dict(_FAIL_CLOSED_SUMMARY)
            payload["generation_status"] = "failed"
            payload["generation_version"] = generation_version
            payload.pop("poster_url", None)
            reason_to_persist = reason_class

        public_payload = apply_public_generation_keys(payload)
        if reason_to_persist is not None:
            public_payload["generation_reason_class"] = reason_to_persist

        self.store.save_projection(
            issue_id=issue_id,
            status=row_status,
            payload=public_payload,
            policy_version=DERIVATION_POLICY_VERSION,
        )
        saved = self.store.get_projection(issue_id)
        assert saved is not None
        return saved
