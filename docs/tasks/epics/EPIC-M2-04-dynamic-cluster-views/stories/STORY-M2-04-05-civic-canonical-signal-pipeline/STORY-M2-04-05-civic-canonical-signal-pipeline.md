# STORY-M2-04-05: Civic canonical signal pipeline (REQ-34)

## Meta
- Key: `STORY-M2-04-05`
- Parent Epic: [`../../../EPIC-M2-04-dynamic-cluster-views.md`](../../../EPIC-M2-04-dynamic-cluster-views.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Clustering / signal extraction
- Decision Ref: [`../../../../../requirements/34-civic-clustering-canonical-signal-pipeline.md`](../../../../../requirements/34-civic-clustering-canonical-signal-pipeline.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-04, G-09; audit follow-up [`../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md`](../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md)
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000013-20260515-req34-civic-canonical-signal.yaml`](../../../../gateway-active-packages/pkg-000013-20260515-req34-civic-canonical-signal.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **T01–T07** (immutable)
- Audit follow-up (override only): T08–T09 — `run_mode=story04_05_audit_req34_followup` in [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md); **не** добавлять в `pkg-000013`
- Depends on: REQ-33 / STORY-M2-02-07 (`narrative_canonical_type`, `narrative_canonical_labels` on `StoryRecord`)
- Supersedes (behavior): STORY-M2-04-01 legacy six-lens keyword baseline — follow-up wave, story row stays Done
- Out of scope: REQ-36 full `alpha_score()` / `cluster/alpha.py` / `CLUSTER_TIE_BREAKER=alpha` in engine; REQ-35 `CLUSTER_GEO_FILTER`

## Story Goal
Удалить legacy keyword lenses и narrative signal modes; активировать только civic линзы и canonical extraction; починить игнор `canonical_type`; формировать `issue_type` / `labels` из GPT canonical полей; добавить promotion readiness gate по `canonical_type`.

## Scope
- Runtime: `cluster/*`, `profile/enrichment.py`, `projection/extraction_policy.py`, `promotion/gates.py`, `application/cluster_orchestrator.py`, `config/schema.py`, `example.env`
- Tests: civic-only clustering, ET/RU fixtures with `canonical_labels` (no EN keyword dependency)

## Out of scope
- `alpha_score()` module and dominant-story tie-break via REQ-36 (T04 uses documented interim `select_dominant_story` until REQ-36)
- SPA i18n display of labels
- `docs/analysis/*` edits as deliverable

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-04-05-t01-remove-legacy-cluster-lenses`](./task-m2-04-05-t01-remove-legacy-cluster-lenses/README.md) | pkg-000013 |
| 2 | [`task-m2-04-05-t02-canonical-signal-extraction-only`](./task-m2-04-05-t02-canonical-signal-extraction-only/README.md) | pkg-000013 |
| 3 | [`task-m2-04-05-t03-env-civic-lenses-and-signal-source`](./task-m2-04-05-t03-env-civic-lenses-and-signal-source/README.md) | pkg-000013 |
| 4 | [`task-m2-04-05-t04-canonical-issue-type-and-labels`](./task-m2-04-05-t04-canonical-issue-type-and-labels/README.md) | pkg-000013 |
| 5 | [`task-m2-04-05-t05-promotion-canonical-type-gate`](./task-m2-04-05-t05-promotion-canonical-type-gate/README.md) | pkg-000013 |
| 6 | [`task-m2-04-05-t06-orchestrator-canonical-projection-wire`](./task-m2-04-05-t06-orchestrator-canonical-projection-wire/README.md) | pkg-000013 |
| 7 | [`task-m2-04-05-t07-tests-civic-lenses-et-ru`](./task-m2-04-05-t07-tests-civic-lenses-et-ru/README.md) | pkg-000013 |
| 8 | [`task-m2-04-05-t08-gap34-01-env-remove-legacy-lens-block`](./task-m2-04-05-t08-gap34-01-env-remove-legacy-lens-block/README.md) | audit override |
| 9 | [`task-m2-04-05-t09-gap34-02-remove-keyword-extraction-policy-dead-export`](./task-m2-04-05-t09-gap34-02-remove-keyword-extraction-policy-dead-export/README.md) | audit override |

## AC / DoD (story level)
- [x] REQ-34 §4: `ClusterLens` без legacy значений; `infer_signals_from_narrative()` отсутствует
- [x] `get_signals_for_story(story)` без `signal_source`; `canonical_type` в signal dict (не discarded)
- [x] `CLUSTER_ACTIVE_LENSES` в `example.env` — только civic six; `CLUSTER_SIGNAL_SOURCE=canonical` only
- [x] `Issue.type` из dominant story `narrative_canonical_type` (mapped to `DOGEIssueType`); `labels` = union `canonical_labels`
- [x] Кластер без `canonical_type in {complaint, system_bug}` → promotion gate reject
- [x] Тесты green на ET/RU narratives с `canonical_labels`
- [x] `gateway_resolve_queue.py --verify` → `ok 7 paths` for pkg-000013
- [x] Audit GAP-34-01: operator `.env` civic-only (no legacy CLUSTER_* duplicate block)
- [x] Audit GAP-34-02: `KEYWORD_EXTRACTION_POLICY` removed from cluster public API

## Traceability: REQ-34 §4 → tasks

| REQ AC | Task |
|--------|------|
| Legacy lenses removed | T01 |
| `infer_signals_from_narrative` absent | T02 |
| `get_signals_for_story` no `signal_source` | T02, T06 |
| `canonical_type` in signal dict | T02 |
| Civic lenses in env | T03 |
| Issue type / labels canonical | T04, T06 |
| Promotion gate observation-only reject | T05 |
| ET/RU tests | T07 |
| AC-8 `.env` civic-only (file, not only effective) | T08 |
| No `KEYWORD_EXTRACTION_POLICY` export | T09 |

## Traceability: audit gaps → tasks

| Audit gap | Task |
|-----------|------|
| GAP-34-01 legacy `.env` block | T08 |
| GAP-34-02 dead `KEYWORD_EXTRACTION_POLICY` | T09 |

## Conflict-scan
| Existing | Action |
|----------|--------|
| STORY-M2-04-01 Done (6 lenses) | Follow-up; do not reopen without operator decision |
| STORY-M2-01-05 T02 CLUSTER_* alignment | Re-verify after T03 civic list |
| REQ-36 alpha_score | Dependency; interim dominant in T04 |
| gap-interview §G-09 cites `issue_create.py` | Implement in `projection/extraction_policy.py` (verified code location) |
