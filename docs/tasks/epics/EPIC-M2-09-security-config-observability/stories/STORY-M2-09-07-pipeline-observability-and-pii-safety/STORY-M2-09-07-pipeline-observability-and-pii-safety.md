# STORY-M2-09-07: Pipeline observability and PII safety (REQ-37)

## Meta
- Key: `STORY-M2-09-07`
- Parent Epic: [`../../../EPIC-M2-09-security-config-observability.md`](../../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Observability / per-story debug JSONL / PII redaction
- Decision Ref: [`../../../../../requirements/37-pipeline-observability-and-pii-safety.md`](../../../../../requirements/37-pipeline-observability-and-pii-safety.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-05, G-06
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000016-20260516-req37-pipeline-observability-pii-safety.yaml`](../../../../gateway-active-packages/pkg-000016-20260516-req37-pipeline-observability-pii-safety.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06 (immutable)
- Depends on: STORY-M2-09-03 (structured logging baseline)
- Supersedes (product path): per-story debug file format from G-05 — JSONL `{LOG_DEBUG_DIR}/{story_id}.jsonl` replaces interim `StoryDebugFileHandler` path (`stories/{date}/{trace}-{story}.log`) and DEBUG-only gating
- Out of scope: Reopening immutable `pkg-000010`; rewriting STORY-M2-09-05/06 task README trees; changing `pkg-000015` REQ-36 queue

## Story Goal
Ввести `StoryDebugLogger` (5 pipeline stages, JSON Lines), `LOG_DEBUG_DIR` независимо от `LOG_LEVEL`, и централизованный `redact_pii()` для narrative полей в логах и debug-файлах.

## Scope
- Runtime: `api/logging.py`, `logging_setup.py`, `application/services.py`, `geo/service.py`, `profile/enrichment.py`, `cluster_orchestrator.py`, `issue_create.py` (promotion gate events at caller)
- Config: `example.env` comment for `LOG_DEBUG_DIR` (`schema.py` — verify-only, field exists)
- Tests: `tests/test_req37_pipeline_observability_pii.py`

## Out of scope
- REQ-36 alpha scoring; REQ-35 geo filter
- Full rewrite of `req-trace-debug-observability.md` (STORY-M2-09-05 remains parallel wave)
- Immutable `pkg-000010`, `pkg-000015`

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-09-07-t01-redact-pii-api-logging`](./task-m2-09-07-t01-redact-pii-api-logging/README.md) | pkg-000016 |
| 2 | [`task-m2-09-07-t02-story-debug-logger-jsonl`](./task-m2-09-07-t02-story-debug-logger-jsonl/README.md) | pkg-000016 |
| 3 | [`task-m2-09-07-t03-services-intake-debug-logger`](./task-m2-09-07-t03-services-intake-debug-logger/README.md) | pkg-000016 |
| 4 | [`task-m2-09-07-t04-geo-signals-debug-stages`](./task-m2-09-07-t04-geo-signals-debug-stages/README.md) | pkg-000016 |
| 5 | [`task-m2-09-07-t05-cluster-promotion-debug-stages`](./task-m2-09-07-t05-cluster-promotion-debug-stages/README.md) | pkg-000016 |
| 6 | [`task-m2-09-07-t06-tests-req37-acceptance`](./task-m2-09-07-t06-tests-req37-acceptance/README.md) | pkg-000016 |

## AC / DoD (story level)
- [x] `LOG_DEBUG_DIR=./debug_logs` → `{story_id}.jsonl` created per story
- [x] JSONL contains all 5 stages: intake, geo, signals, cluster, promotion
- [x] `LOG_DEBUG_DIR` unset → no files, no errors
- [x] `redact_pii(text, True)` → `[REDACTED]`; `False` → full text
- [x] `privacy.contains_pii=True` → `original_text` not in logs in cleartext
- [x] `LOG_DEBUG_DIR` works when `LOG_LEVEL=INFO`
- [x] `gateway_resolve_queue.py --verify` → `ok 6 paths` for pkg-000016

**Gate:** [`story-acceptance-gate-STORY-M2-09-07.md`](./story-acceptance-gate-STORY-M2-09-07.md) — PASS (2026-05-17)

## Traceability: REQ-37 → tasks

| REQ-37 | Task |
|--------|------|
| §2.2 `redact_pii()` | T01 |
| §2.1 `StoryDebugLogger` + `LOG_DEBUG_DIR` | T02 |
| §2.1 intake stage + PII in services | T03 |
| §2.1 geo + signals stages | T04 |
| §2.1 cluster + promotion stages | T05 |
| §5 acceptance criteria | T06 |

## Conflict-scan

| Existing | Action |
|----------|--------|
| STORY-M2-09-05 T07 (GAP-TRACE-08) | Product path superseded by REQ-37; keep 09-05 wave immutable; note in index only |
| `StoryDebugFileHandler` in `logging_setup.py` | T02 refactor/replace toward `StoryDebugLogger` per REQ-37 |
| `LOG_DEBUG_DIR` in `schema.py` | Already present — T02 verify-only + `example.env` |
| `promotion/gates.py` pure functions | T05 logs at orchestrator/issue_create callers, not inside gates |
