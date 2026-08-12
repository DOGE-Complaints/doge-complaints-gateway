# Backward-compat decision — GW-DRAFT-05 T02

- **Status:** DECIDED
- **Date:** 2026-07-11T07:52:43Z

## Question (from backlog)

Черновики в БД с placeholder `__stash_pending_author__` — миграция или tolerant read на submit?

## Options

| Option | Pros | Cons |
|--------|------|------|
| Tolerant read on submit | No DB migration; existing drafts still submit | Temporary compat code path |
| One-time migration / TTL expiry | Clean domain; no compat branch | Ops work; may lose stale drafts |

## Decision

**Tolerant read on submit** — `parse_stored_draft_stash_request()` strips legacy placeholder submitter before `parse_story_draft_stash_request()`. New stashes store `StoryDraftStashRequest.as_dict()` without submitter. Compat path expires naturally via `STORY_DRAFT_TTL_SECONDS`.

## Evidence

- Implementation: `src/core/intake/contracts.py` — `_normalize_stored_draft_payload`, `parse_stored_draft_stash_request`
- Handler: `handle_story_draft_submit` uses bridge + `handle_story_intake(..., user_introspection=None)`
- Tests: `tests/test_gw_draft_02_story_draft_submit_contract.py` — 8 passed (2026-07-11 P3)
