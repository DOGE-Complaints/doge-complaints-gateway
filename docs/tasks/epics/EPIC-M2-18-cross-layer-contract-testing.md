# EPIC-M2-18: Cross-Layer Contract Testing (REQ-39) & Production Coverage (REQ-41)

## Epic Meta
- Status: In Progress (REQ-41 wave); REQ-39 stories 18-01/02 Done (Build)
- Priority: High
- Owner: TBD
- Target: Post-REQ-24/33–40 quality wave → production-scenario test guarantee

## Business Goal
1. **REQ-39:** Закрыть структурные gaps на стыках слоёв (HTTP → service → repository → SQL → projection/read) через offline contract-suite зон A–N.
2. **REQ-41:** Довести покрытие продакшн-сценариев PS-01..PS-25 до 100% — real HTTP (`LOCAL_SERVER_URL`), cron timing, concurrency, env-only config, live Supabase CI.

## Problem Statement
226+ unit-тестов не выявили 11 структурных gaps (GAP-07/08/11 и др.): тесты работают с Python-объектами в обход сериализации, bootstrap SQL и runtime SELECT/INSERT не связаны единым инвариантом. После REQ-39 (412 offline) остаются пробелы: in-process TestClient не покрывает uvicorn HTTP stack, cron stub вместо full-stack timing, нет concurrent intake, live Supabase opt-in only.

## Scope
### In Scope (REQ-39 — Done wave)
- 14 SEAM-зон A–N из [`39-cross-layer-contract-testing.md`](../../requirements/39-cross-layer-contract-testing.md)
- Offline contract tests InMemory/SQLite; audit follow-up T06–T14 (REQ-39)
- REQ-41 audit follow-up T22–T23 (override only; не менять `pkg-000021`)

### In Scope (REQ-41 — active wave)
- Layer 6 `tests/smoke/` — `LOCAL_SERVER_URL` + canvas via [`simulation_runner.py`](../../../tests/simulation_runner.py)
- [`41-testing-production-coverage-target-state.md`](../../requirements/41-testing-production-coverage-target-state.md) gaps GAP-41-01..06
- Cron timing, concurrent intake, env-only config (offline TestClient)
- CI `integration-live` + `pytest.mark.live_integration`
- Arch doc PS matrix closure (AC-41-8)

### Out of Scope
- Изменение продуктовой логики без failing test
- Новый HTTP `POST /clustering/trigger` (as-is: `process_all_pending()`)
- Обязательный `LOCAL_SERVER_URL` в default offline CI job
- Редактирование immutable [`pkg-000020`](../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml)

## Source Requirements
- [`39-cross-layer-contract-testing.md`](../../requirements/39-cross-layer-contract-testing.md)
- [`41-testing-production-coverage-target-state.md`](../../requirements/41-testing-production-coverage-target-state.md)

## Dependencies
- REQ-24, REQ-27, REQ-33, REQ-34, REQ-35, REQ-40 — runtime Done
- REQ-39 contract wave (STORY-M2-18-01/02) — Done (Build)
- REQ-28 (cron), REQ-35 (geo filters), REQ-40 (geo propagation) — per REQ-41 §1

## Stories

| Key | Story | Type | Status | Scope |
|-----|-------|------|--------|-------|
| M2-18-01 | [Cross-layer zones J–N (REQ-39)](./EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md) | tests | Done (Build) | Zones J–N + audit T06–T09 |
| M2-18-02 | [Cross-layer zones A–I (REQ-39)](./EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-02-cross-layer-contract-zones-a-i-req39/STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md) | tests | Done (Build) | Zones A–I + audit T14 |
| M2-18-03 | [Local real HTTP smoke (REQ-41)](./EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-03-local-real-http-smoke-req41/STORY-M2-18-03-local-real-http-smoke-req41.md) | tests | Todo | GAP-41-01, GAP-41-06; Layer 6 smoke |
| M2-18-04 | [Offline production paths (REQ-41)](./EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-04-offline-production-paths-req41/STORY-M2-18-04-offline-production-paths-req41.md) | tests | Todo | GAP-41-02..04; cron, concurrency, env-only |
| M2-18-05 | [Live integration CI (REQ-41)](./EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-05-live-integration-ci-req41/STORY-M2-18-05-live-integration-ci-req41.md) | tests+ci | Todo | GAP-41-05; AC-41-8 arch doc |

## Operative queue
- REQ-39 (immutable): [`pkg-000020-20260518-req39-cross-layer-contract-testing.yaml`](../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml)
- REQ-41 (active): [`pkg-000021-20260518-req41-production-test-coverage.yaml`](../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml)
- Pointer: [`gateway-active-package.current.yaml`](../gateway-active-package.current.yaml)

## Epic Acceptance Criteria
### REQ-39 (Done)
- [x] AC-39-2..9 по story gates STORY-M2-18-01/02
- [x] `gateway_resolve_queue.py --verify` → `ok 13 paths` для pkg-000020

### REQ-41 (open)
- [ ] AC-41-1..8 per [`41-testing-production-coverage-target-state.md`](../../requirements/41-testing-production-coverage-target-state.md) §5
- [ ] `gateway_resolve_queue.py --verify` → `ok 7 paths` для pkg-000021
- [ ] Offline suite: `pytest tests/ --ignore=tests/integration -q` green (no regression vs 412+)

## Conflict-scan
| Topic | Resolution |
|-------|------------|
| REQ-39 vs REQ-41 PS-* | REQ-41 closes only gaps §3; PS-02,05–10,12,15–17,20–24 already covered by REQ-39/24/40 |
| `simulation_runner.py` | EPIC-M2-16 implements CLI; REQ-41 smoke **imports** `_scenario_to_payload` — no duplicate epic |
| vs `test_cluster_cron_job.py` | Keep unit tests; T17 adds full-stack timing contract (real orchestrator) |
| pkg-000020 | Immutable; REQ-41 uses pkg-000021 only |
