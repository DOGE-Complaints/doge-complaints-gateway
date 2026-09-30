"""GW-REQ11-06 — wipe helpers (confirm gate + ordered delete plans).

Tables locked to REQUIRED_READINESS_TABLES + verified threads names only.
Never deletes Identity auth.users / admin.
"""

from __future__ import annotations

import os
from typing import Final

# Verbatim frozenset from src/core/infrastructure/db_supabase.py REQUIRED_READINESS_TABLES.
# Keep in sync; unit test asserts equality against import when src is on path.
REQUIRED_READINESS_TABLES: Final[frozenset[str]] = frozenset(
    {
        "stories",
        "idempotency_keys",
        "story_embeddings",
        "doge_issues",
        "doge_issue_embeddings",
        "issue_candidates",
        "review_audit_log",
        "issue_story_links",
        "story_signals",
        "cluster_memberships",
        "story_drafts",
        "story_labels",
    }
)

# FK-safe child→parent order (sqlite/supabase evidence: labels/embeddings/idempotency
# FK stories; issue embeddings FK issues; links before parents).
GATEWAY_DELETE_ORDER: Final[tuple[str, ...]] = (
    "story_labels",
    "story_embeddings",
    "idempotency_keys",
    "story_signals",
    "cluster_memberships",
    "issue_story_links",
    "doge_issue_embeddings",
    "review_audit_log",
    "issue_candidates",
    "doge_issues",
    "story_drafts",
    "stories",
)

# PostgREST not-null filter column per table (PK / always-present column).
GATEWAY_DELETE_FILTER_COLUMN: Final[dict[str, str]] = {
    "story_labels": "story_id",
    "story_embeddings": "story_id",
    "idempotency_keys": "story_id",
    "story_signals": "story_id",
    "cluster_memberships": "story_id",
    "issue_story_links": "story_id",
    "doge_issue_embeddings": "issue_id",
    "review_audit_log": "candidate_id",
    "issue_candidates": "candidate_id",
    "doge_issues": "issue_id",
    "story_drafts": "draft_id",
    "stories": "story_id",
}

# Verified doge-threads mappers (child→parent).
THREADS_DELETE_ORDER: Final[tuple[str, ...]] = (
    "thread_reaction_marks",
    "thread_comments",
    "thread_threads",
)

THREADS_DELETE_FILTER_COLUMN: Final[dict[str, str]] = {
    # Verified columns from doge-threads mappers (no invent PKs).
    "thread_reaction_marks": "actor_id",
    "thread_comments": "comment_id",
    "thread_threads": "entity_id",
}

FORBIDDEN_TABLE_SUBSTRINGS: Final[tuple[str, ...]] = (
    "auth.users",
    "auth_users",
    "identity",
)


def assert_gateway_order_covers_readiness() -> None:
    ordered = set(GATEWAY_DELETE_ORDER)
    if ordered != set(REQUIRED_READINESS_TABLES):
        missing = set(REQUIRED_READINESS_TABLES) - ordered
        extra = ordered - set(REQUIRED_READINESS_TABLES)
        raise AssertionError(
            f"GATEWAY_DELETE_ORDER mismatch readiness: missing={missing} extra={extra}"
        )
    for table in GATEWAY_DELETE_ORDER:
        if table not in GATEWAY_DELETE_FILTER_COLUMN:
            raise AssertionError(f"missing filter column for {table}")


def wipe_confirmed(*, cli_confirm: bool, env: dict[str, str] | None = None) -> bool:
    """True when --confirm-wipe OR LIFE_SIM_WIPE_CONFIRMED=1."""
    environ = env if env is not None else os.environ
    if cli_confirm:
        return True
    return environ.get("LIFE_SIM_WIPE_CONFIRMED", "").strip() == "1"


def plan_contains_forbidden(tables: list[str] | tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for table in tables:
        lower = table.lower()
        for bad in FORBIDDEN_TABLE_SUBSTRINGS:
            if bad in lower:
                hits.append(table)
                break
    return hits


def full_wipe_plan() -> list[tuple[str, str, str]]:
    """Return list of (scope, table, filter_column) in delete order."""
    assert_gateway_order_covers_readiness()
    plan: list[tuple[str, str, str]] = []
    for table in GATEWAY_DELETE_ORDER:
        plan.append(("gateway", table, GATEWAY_DELETE_FILTER_COLUMN[table]))
    for table in THREADS_DELETE_ORDER:
        plan.append(("threads", table, THREADS_DELETE_FILTER_COLUMN[table]))
    forbidden = plan_contains_forbidden([t for _, t, _ in plan])
    if forbidden:
        raise AssertionError(f"forbidden tables in plan: {forbidden}")
    return plan
