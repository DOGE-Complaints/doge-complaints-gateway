#!/usr/bin/env python3
"""One-off backfill: re-project existing issues so payload_json carries dominant-story i18n
and original_locale metadata (GW-L10N-01 + GW-L10N-02).

Run after deploying GW-L10N-01 (T01/T02) and GW-L10N-02 (T01/T02). Uses DATABASE_URL / Supabase env from the runtime.

Operator manual:
  docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md

Examples:
  cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --dry-run
  cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --issue-id <uuid>
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.application.factory import ServiceFactory  # noqa: E402
from core.application.issue_create import (  # noqa: E402
    DERIVATION_POLICY_VERSION,
    IssueProjectionReadWriteStore,
    IssueStoryLinkStore,
    StoryPromotionProjectionBridge,
    _promoted_title_from_i18n,
)
from core.domain import StoryRepository  # noqa: E402
from core.infrastructure.db_sqlite import SqliteIssueStoryLinkStore  # noqa: E402
from core.infrastructure.db_supabase import SupabaseIssueStoryLinkStore  # noqa: E402
from core.infrastructure.providers import provide_service_factory  # noqa: E402
from core.infrastructure.service_factory import DefaultServiceFactory  # noqa: E402
from core.projection import IssueProjectionService  # noqa: E402


@dataclass(frozen=True)
class _ReprojectWiring:
    projection_store: IssueProjectionReadWriteStore
    link_store: IssueStoryLinkStore
    story_repository: StoryRepository


class _ReprojectFactory(Protocol):
    issue_projection_store: IssueProjectionReadWriteStore | None
    issue_story_link_store: IssueStoryLinkStore | None
    story_repository: StoryRepository


def _resolve_wiring(factory: ServiceFactory) -> _ReprojectWiring:
    if not isinstance(factory, DefaultServiceFactory):
        raise SystemExit("Backfill script requires DefaultServiceFactory wiring.")
    wired = cast(_ReprojectFactory, factory)
    projection_store = wired.issue_projection_store
    link_store = wired.issue_story_link_store
    if projection_store is None or link_store is None:
        raise SystemExit("Persistence stores are not configured.")
    return _ReprojectWiring(
        projection_store=projection_store,
        link_store=link_store,
        story_repository=wired.story_repository,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Re-project doge_issues payload_json from linked stories (GW-L10N-01/02 backfill)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned updates without writing payload_json.",
    )
    parser.add_argument(
        "--issue-id",
        action="append",
        dest="issue_ids",
        metavar="ISSUE_ID",
        help="Limit to one or more issue IDs (repeatable). Default: all linked issues.",
    )
    return parser.parse_args()


def _load_issue_story_map(
    link_store: IssueStoryLinkStore,
) -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    if isinstance(link_store, SqliteIssueStoryLinkStore):
        rows = link_store.db.connection.execute(
            "SELECT issue_id, story_id FROM issue_story_links ORDER BY issue_id, story_id"
        ).fetchall()
        for issue_id, story_id in rows:
            grouped[str(issue_id)].append(str(story_id))
    elif isinstance(link_store, SupabaseIssueStoryLinkStore):
        rows = link_store.db._request(
            method="GET",
            path="/rest/v1/issue_story_links",
            params={"select": "issue_id,story_id"},
        )
        for row in rows:
            grouped[str(row["issue_id"])].append(str(row["story_id"]))
    else:
        raise SystemExit(
            "issue_story_link_store is in-memory; configure sqlite or supabase persistence."
        )
    return {issue_id: tuple(story_ids) for issue_id, story_ids in grouped.items()}


def _promoted_title_from_payload(payload: dict[str, object]) -> str:
    title = payload.get("title")
    if isinstance(title, dict):
        try:
            return _promoted_title_from_i18n(title)
        except ValueError:
            pass
    return str(payload.get("id", "Issue"))


def _issue_status(
    projection_store: IssueProjectionReadWriteStore,
    issue_id: str,
    payload: dict[str, object],
) -> str:
    status = payload.get("status")
    if isinstance(status, str) and status.strip():
        return status.strip()
    row = projection_store.get_projection(issue_id)
    if row is not None:
        row_status = row.get("status")
        if isinstance(row_status, str) and row_status.strip():
            return row_status.strip()
    return "PUBLISHED"


def run_reproject(
    *,
    projection_store: IssueProjectionReadWriteStore,
    link_store: IssueStoryLinkStore,
    story_repository: StoryRepository,
    dry_run: bool = False,
    issue_ids: frozenset[str] | None = None,
) -> tuple[int, int]:
    """Re-project linked issues; returns (updated_count, skipped_count)."""
    issue_story_map = _load_issue_story_map(link_store)
    if issue_ids is not None:
        issue_story_map = {
            issue_id: story_ids_tuple
            for issue_id, story_ids_tuple in issue_story_map.items()
            if issue_id in issue_ids
        }

    bridge = StoryPromotionProjectionBridge(story_repository=story_repository)
    projection_service = IssueProjectionService()
    updated = 0
    skipped = 0

    for issue_id, story_ids in sorted(issue_story_map.items()):
        existing = projection_store.get_projection(issue_id)
        if existing is None:
            skipped += 1
            continue
        promoted_title = _promoted_title_from_payload(existing)
        try:
            projection_input = bridge.build_projection_input(
                issue_id=issue_id,
                promoted_title=promoted_title,
                story_ids=story_ids,
            )
        except ValueError:
            skipped += 1
            continue

        projection = projection_service.project(projection_input)
        new_payload = projection.to_public_dict()
        if "type" in existing:
            new_payload["type"] = existing["type"]

        if dry_run:
            updated += 1
            continue

        projection_store.save_projection(
            issue_id=issue_id,
            status=_issue_status(projection_store, issue_id, existing),
            payload=new_payload,
            policy_version=DERIVATION_POLICY_VERSION,
        )
        updated += 1

    return updated, skipped


def main() -> int:
    args = _parse_args()
    wiring = _resolve_wiring(provide_service_factory())

    selected_ids: frozenset[str] | None = None
    if args.issue_ids:
        selected_ids = frozenset(
            issue_id.strip() for issue_id in args.issue_ids if issue_id.strip()
        )
        linked = set(_load_issue_story_map(wiring.link_store))
        for issue_id in sorted(selected_ids - linked):
            print(f"skip: no issue_story_links for {issue_id}", file=sys.stderr)

    updated, skipped = run_reproject(
        projection_store=wiring.projection_store,
        link_store=wiring.link_store,
        story_repository=wiring.story_repository,
        dry_run=args.dry_run,
        issue_ids=selected_ids,
    )

    mode = "dry-run" if args.dry_run else "write"
    print(f"done ({mode}): updated={updated} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
