# STORY-M2-04-06: Alpha scoring and story quality gate (REQ-36)

## Meta
- Key: `STORY-M2-04-06`
- Parent Epic: [`../../../EPIC-M2-04-dynamic-cluster-views.md`](../../../EPIC-M2-04-dynamic-cluster-views.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Clustering / dominant story selection / promotion quality
- Decision Ref: [`../../../../../requirements/36-alpha-scoring-and-story-quality-gate.md`](../../../../../requirements/36-alpha-scoring-and-story-quality-gate.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-03
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000015-20260516-req36-alpha-scoring-story-quality-gate.yaml`](../../../../gateway-active-packages/pkg-000015-20260516-req36-alpha-scoring-story-quality-gate.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05 (immutable)
- Depends on: STORY-M2-04-05 (canonical fields on `StoryRecord`, interim `select_dominant_story`); REQ-33 / STORY-M2-02-07 (`submitter_identity_issuer` required — verify-only for REQ-36 §2.1)
- Supersedes (behavior): interim dominant picker in [`projection/extraction_policy.py`](../../../../../src/core/projection/extraction_policy.py) only; do not reopen REQ-34 promotion gate implementation
- Out of scope: REQ-35 geo scope/filter; `oldest_first` / `systemic_priority` tie-breaker modes (roadmap only per REQ-36 §2.4)

## Story Goal
Ввести детерминированный `alpha_score(story)` (0–100), заменить interim `select_dominant_story` на выбор по alpha с tie-break по `created_at`, зафиксировать контракт `CLUSTER_TIE_BREAKER=alpha`, подтвердить promotion gate по actionable `canonical_type` (уже из REQ-34).

## Scope
- Runtime: `cluster/alpha.py` (new), `projection/extraction_policy.py`, `config/schema.py`, `example.env`, `cluster/engine.py` (tie_breaker field contract)
- Tests: `tests/test_alpha_score.py`, REQ-36 acceptance matrix, promotion gate regression

## Out of scope
- eID intake gate (`identity_issuer`) — closed in REQ-33; story only documents verify-only
- Re-implementing `promotion/gates.py` logic (REQ-34 T05); T04 = verification
- Engine cluster-key geo filter (REQ-35)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-04-06-t01-cluster-alpha-score-module`](./task-m2-04-06-t01-cluster-alpha-score-module/README.md) | pkg-000015 |
| 2 | [`task-m2-04-06-t02-select-dominant-story-alpha`](./task-m2-04-06-t02-select-dominant-story-alpha/README.md) | pkg-000015 |
| 3 | [`task-m2-04-06-t03-cluster-tie-breaker-config-engine`](./task-m2-04-06-t03-cluster-tie-breaker-config-engine/README.md) | pkg-000015 |
| 4 | [`task-m2-04-06-t04-promotion-gate-req36-verification`](./task-m2-04-06-t04-promotion-gate-req36-verification/README.md) | pkg-000015 |
| 5 | [`task-m2-04-06-t05-tests-req36-acceptance`](./task-m2-04-06-t05-tests-req36-acceptance/README.md) | pkg-000015 |

## AC / DoD (story level)
- [x] `alpha_score(story)` возвращает float 0–100
- [x] История с canonical fields + rich narrative → score > 60; без canonical → score < 20
- [x] `alpha_score` geo-агностичная история: измерение 3 = 0 (geo=None)
- [x] Dominant story в кластере = max `alpha_score`; tie → oldest `created_at`
- [x] Кластер без `complaint`/`system_bug` в canonical_type → promotion skip (`no_actionable_canonical_type`)
- [x] `CLUSTER_TIE_BREAKER=alpha` в конфиге; non-alpha → `ConfigError`
- [x] `gateway_resolve_queue.py --verify` → `ok 5 paths` for pkg-000015

Gate: [`story-acceptance-gate-STORY-M2-04-06.md`](./story-acceptance-gate-STORY-M2-04-06.md) — PASS. Run: [`run-summary-20260516-req36-alpha-scoring-gateway-builder-complete.md`](../../../run-reports/run-summary-20260516-req36-alpha-scoring-gateway-builder-complete.md).

## Traceability: REQ-36 → tasks

| REQ-36 | Task |
|--------|------|
| §2.2 `alpha_score()` module | T01 |
| §2.3 tie-break `created_at` + dominant selection | T02 |
| §2.4 `CLUSTER_TIE_BREAKER=alpha` | T03 |
| §2.5 canonical_type promotion gate | T04 (verify), T05 (AC) |
| §5 acceptance criteria | T05 |
| §2.1 eID gate (REQ-33) | — verify in STORY only |

## Conflict-scan
| Existing | Action |
|----------|--------|
| STORY-M2-04-05 T05 promotion gate | Do not duplicate; T04 verifies REQ-36 §2.5 AC |
| STORY-M2-04-05 T04 interim `select_dominant_story` | T02 replaces heuristic with `alpha_score` |
| REQ-35 geo filter | No changes to `CLUSTER_GEO_*` in this story |
| `ClusteringEngine.tie_breaker` unused in methods | T03 documents product path vs engine field; wire or explicit scope note |
