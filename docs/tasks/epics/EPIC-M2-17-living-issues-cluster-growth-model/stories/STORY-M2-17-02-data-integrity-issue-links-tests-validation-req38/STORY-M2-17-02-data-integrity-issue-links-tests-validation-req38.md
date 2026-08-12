# STORY-M2-17-02: Data integrity — issue story links, tests, validation (REQ-38)

## Meta
- Key: `STORY-M2-17-02`
- Parent Epic: [`../../../EPIC-M2-17-living-issues-cluster-growth-model.md`](../../../EPIC-M2-17-living-issues-cluster-growth-model.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Living issues / data integrity / linkage persistence / projection validation
- Decision Ref: [`../../../../../requirements/38-data-integrity-issue-links-tests-validation.md`](../../../../../requirements/38-data-integrity-issue-links-tests-validation.md); [`../../../../../analysis/audit-req38-data-integrity-issue-links-tests-validation-2026-05-17.md`](../../../../../analysis/audit-req38-data-integrity-issue-links-tests-validation-2026-05-17.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-10, G-11, G-12
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000017-20260517-req38-data-integrity-issue-links.yaml`](../../../../gateway-active-packages/pkg-000017-20260517-req38-data-integrity-issue-links.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05 (immutable)
- Depends on: STORY-M2-17-01 (extend primitives, issue-story link dedup — Done)
- Out of scope: Reopening immutable `pkg-000016`; changing STORY-M2-17-01 task README trees (T09–T12 parallel wave)

## Story Goal
Закрыть REQ-38: e2e тест extend flow через `process_story()`, индекс и lookup для `issue_story_links`, валидация Arweave txid в projection layer.

## Scope
- Tests: `tests/test_living_issues_extend_existing.py`, `tests/test_req38_data_integrity.py`
- DDL: `supabase/bootstrap/000_full_init.sql`, migration `issue_story_links_story` index
- Runtime: `infrastructure/db_supabase.py` (`find_promoted_by_cluster_id` JOIN semantics), `projection/validation.py`
- Product decision (G-11): N:M persistence через `IssueStoryLinkStore.save_issue_story_links()` — не дублировать в `ClusterMembershipStore.save_membership()` (Variant A, audit 2026-05-17)

## Out of scope
- REQ-37 observability; REQ-36 alpha scoring
- GAP-29 T09–T12 under STORY-M2-17-01 (parallel, unchanged)
- Immutable `pkg-000016`

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-17-02-t01-living-issues-extend-e2e-test`](./task-m2-17-02-t01-living-issues-extend-e2e-test/README.md) | pkg-000017 |
| 2 | [`task-m2-17-02-t02-issue-story-links-story-index`](./task-m2-17-02-t02-issue-story-links-story-index/README.md) | pkg-000017 |
| 3 | [`task-m2-17-02-t03-supabase-linkage-lookup-semantics`](./task-m2-17-02-t03-supabase-linkage-lookup-semantics/README.md) | pkg-000017 |
| 4 | [`task-m2-17-02-t04-arweave-txid-validation`](./task-m2-17-02-t04-arweave-txid-validation/README.md) | pkg-000017 |
| 5 | [`task-m2-17-02-t05-req38-acceptance-tests`](./task-m2-17-02-t05-req38-acceptance-tests/README.md) | pkg-000017 |

## AC / DoD (story level)
- [x] `tests/test_living_issues_extend_existing.py` exists; extend via `process_story()` with `story_count=3` and labels union (G-10)
- [x] `idx_issue_story_links_story` in bootstrap + migration (G-11)
- [x] `find_promoted_by_cluster_id()` uses `issue_story_links` where applicable; linkage tests pass (G-11, Variant A)
- [x] `validate_arweave_txid()` in `projection/validation.py` with REQ-38 §3 AC (G-12)
- [x] `gateway_resolve_queue.py --verify` → `ok 5 paths` for pkg-000017

**Gate:** [`story-acceptance-gate-STORY-M2-17-02.md`](./story-acceptance-gate-STORY-M2-17-02.md) — PASS (2026-05-17)

## Traceability: REQ-38 → tasks

| REQ-38 | Task |
|--------|------|
| §1 G-10 extend e2e test | T01 |
| §2 G-11 DDL index | T02 |
| §2 G-11 lookup / linkage semantics | T03 |
| §3 G-12 Arweave txid | T04 |
| §5 acceptance criteria | T05 |

## Conflict-scan

| Existing | Action |
|----------|--------|
| STORY-M2-17-01 T09–T12 (GAP-29) | Parallel; do not modify task README |
| TASK-LI-LINKS-DEDUP-01 (Done) | Dedup contract unchanged; T03 adds lookup/index only |
| `test_e2e_living_issue_two_batches_*` | Remains; T01 adds dedicated REQ-38 file |
| REQ-38 §2.2 literal `save_membership` → `issue_story_links` | Variant A: clarify AC; T03 implements lookup + tests for `save_issue_story_links` path |
| `pkg-000016` / STORY-M2-09-07 | Immutable / Done — do not touch |
