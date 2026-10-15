"""GW-REQ57-02: thin outbound nudge to aibridge sense-brief accept (no LLM in gateway)."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Mapping, Protocol, Sequence

import httpx

from core.config import AppConfig
from core.domain import StoryRecord
from core.projection.columnar_storage import apply_public_generation_keys

logger = logging.getLogger(__name__)

ACCEPT_PATH = "/v1/worker/sense-brief/accept"
INITIAL_GENERATION_VERSION = "v1"


class SenseBriefNudgeTransport(Protocol):
    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: Mapping[str, Any],
        timeout_s: float,
    ) -> httpx.Response:
        """POST JSON; used for HTTP doubles in tests."""


class HttpxSenseBriefNudgeTransport:
    def post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: Mapping[str, Any],
        timeout_s: float,
    ) -> httpx.Response:
        with httpx.Client(timeout=timeout_s) as client:
            return client.post(url, headers=dict(headers), json=dict(body))


@dataclass(frozen=True)
class SenseBriefNudgeSettings:
    enabled: bool
    base_url: str | None
    s2s_token: str | None
    timeout_s: float

    @property
    def accept_url(self) -> str | None:
        if not self.base_url:
            return None
        return f"{self.base_url.rstrip('/')}{ACCEPT_PATH}"


@dataclass(frozen=True)
class SenseBriefNudgeResult:
    generation_version: str
    attempted: bool
    succeeded: bool
    skip_reason: str | None = None
    status_code: int | None = None


def settings_from_config(config: AppConfig) -> SenseBriefNudgeSettings:
    return SenseBriefNudgeSettings(
        enabled=bool(config.aibridge_sense_brief_nudge_enabled),
        base_url=config.aibridge_base_url,
        s2s_token=config.aibridge_worker_sense_brief_s2s_token,
        timeout_s=float(config.request_timeout_s),
    )


def build_corpus_from_stories(stories: Sequence[StoryRecord]) -> dict[str, Any]:
    """Optional corpus from Issue Stories membership (no clustering change)."""
    items: list[dict[str, Any]] = []
    for story in stories:
        entry: dict[str, Any] = {
            "story_id": story.story_id,
            "text": (story.narrative_original_text or "").strip(),
        }
        if story.narrative_title:
            entry["title"] = dict(story.narrative_title)
        if story.narrative_description:
            entry["description"] = dict(story.narrative_description)
        items.append(entry)
    return {"stories": items}


def mark_generation_pending(
    payload: Mapping[str, Any],
    *,
    generation_version: str = INITIAL_GENERATION_VERSION,
) -> dict[str, Any]:
    """Set public generation keys to pending + initial version (AC-01)."""
    out = dict(payload)
    out["generation_status"] = "pending"
    out["generation_version"] = generation_version.strip() or INITIAL_GENERATION_VERSION
    out.pop("poster_url", None)
    out.pop("generation_reason_class", None)
    return apply_public_generation_keys(out)


@dataclass(frozen=True)
class SenseBriefNudgeService:
    settings: SenseBriefNudgeSettings
    transport: SenseBriefNudgeTransport = HttpxSenseBriefNudgeTransport()

    def nudge(
        self,
        *,
        issue_id: str,
        generation_version: str,
        corpus: Mapping[str, Any] | None = None,
    ) -> SenseBriefNudgeResult:
        version = generation_version.strip() or INITIAL_GENERATION_VERSION
        if not self.settings.enabled:
            logger.info(
                "sense_brief_nudge.fail_closed reason=disabled issue_id=%s "
                "generation_version=%s",
                issue_id,
                version,
            )
            return SenseBriefNudgeResult(
                generation_version=version,
                attempted=False,
                succeeded=False,
                skip_reason="disabled",
            )

        url = self.settings.accept_url
        token = (self.settings.s2s_token or "").strip()
        if not url or not token:
            logger.warning(
                "sense_brief_nudge.fail_closed reason=missing_config issue_id=%s "
                "generation_version=%s has_base_url=%s has_token=%s",
                issue_id,
                version,
                bool(url),
                bool(token),
            )
            return SenseBriefNudgeResult(
                generation_version=version,
                attempted=False,
                succeeded=False,
                skip_reason="missing_config",
            )

        body: dict[str, Any] = {
            "issue_id": issue_id.strip(),
            "generation_version": version,
        }
        if corpus is not None:
            body["corpus"] = dict(corpus)

        try:
            response = self.transport.post_json(
                url=url,
                headers={"Authorization": f"Bearer {token}"},
                body=body,
                timeout_s=self.settings.timeout_s,
            )
        except httpx.HTTPError as exc:
            logger.warning(
                "sense_brief_nudge.fail_closed reason=transport issue_id=%s "
                "generation_version=%s error=%s",
                issue_id,
                version,
                exc,
            )
            return SenseBriefNudgeResult(
                generation_version=version,
                attempted=True,
                succeeded=False,
                skip_reason="transport_error",
            )

        ok = 200 <= response.status_code < 300
        if ok:
            logger.info(
                "sense_brief_nudge.accepted issue_id=%s generation_version=%s "
                "status_code=%s",
                issue_id,
                version,
                response.status_code,
            )
        else:
            logger.warning(
                "sense_brief_nudge.fail_closed reason=http_status issue_id=%s "
                "generation_version=%s status_code=%s",
                issue_id,
                version,
                response.status_code,
            )
        return SenseBriefNudgeResult(
            generation_version=version,
            attempted=True,
            succeeded=ok,
            skip_reason=None if ok else "http_status",
            status_code=response.status_code,
        )


def build_nudge_service_from_config(
    config: AppConfig,
    *,
    transport: SenseBriefNudgeTransport | None = None,
) -> SenseBriefNudgeService:
    return SenseBriefNudgeService(
        settings=settings_from_config(config),
        transport=transport or HttpxSenseBriefNudgeTransport(),
    )
