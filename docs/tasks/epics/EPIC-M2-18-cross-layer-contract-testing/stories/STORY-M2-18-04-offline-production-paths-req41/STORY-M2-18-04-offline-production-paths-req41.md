# STORY-M2-18-04: Offline full-stack production paths (REQ-41)

## Meta
- Key: `STORY-M2-18-04`
- Parent Epic: [`../../../EPIC-M2-18-cross-layer-contract-testing.md`](../../../EPIC-M2-18-cross-layer-contract-testing.md)
- Type: Technical Story
- Status: Done (Build)
- Stream: M2 quality / production coverage / offline TestClient
- Decision Ref: [`../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-02..04
- Operative queue: [`../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml`](../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml) — T17–T19
- Depends on: REQ-39 J-zone ([`test_clustering_pipeline_contract.py`](../../../../../tests/test_clustering_pipeline_contract.py)); REQ-28 cron module
- Blocks: —

## Story Goal
Закрыть offline gaps: реальный cron timing через ASGI lifespan, concurrent intake, isolated env-only config loading — без `_OrchestratorStub` там, где требуется production path.

## Scope
- `tests/test_cron_clustering_timing_contract.py` (CT-01..03)
- `tests/test_concurrent_intake_contract.py` (CC-01..02)
- `tests/test_config_env_only_contract.py` (CE-01..03)

## Out of scope
- `tests/smoke/` (STORY-M2-18-03)
- Live Supabase / CI (STORY-M2-18-05)
- Changing `ClusterCronJob` implementation unless test proves bug

## Nested tasks

| Order | Task folder | Gap |
|-------|-------------|-----|
| 17 | [`task-m2-18-04-t17-gap41-02-cron-clustering-timing`](./task-m2-18-04-t17-gap41-02-cron-clustering-timing/README.md) | GAP-41-02 |
| 18 | [`task-m2-18-04-t18-gap41-03-concurrent-intake`](./task-m2-18-04-t18-gap41-03-concurrent-intake/README.md) | GAP-41-03 |
| 19 | [`task-m2-18-04-t19-gap41-04-config-env-only`](./task-m2-18-04-t19-gap41-04-config-env-only/README.md) | GAP-41-04 |

## AC / DoD (story level)
- [x] AC-41-2: CT-01..CT-03 green; CT-01 completes in &lt; 5s
- [x] AC-41-3: CC-01, CC-02 stable (no flaky races)
- [x] AC-41-6: CE-01..CE-03 without `.env` file
- [x] Story gate after T17–T19 — [`story-acceptance-gate-STORY-M2-18-04.md`](./story-acceptance-gate-STORY-M2-18-04.md)

## Traceability: REQ-41 §3 → tasks

| Gap | PS | Task |
|-----|-----|------|
| GAP-41-02 | PS-03, PS-04 | T17 |
| GAP-41-03 | PS-11 | T18 |
| GAP-41-04 | PS-18 | T19 |

## Conflict-scan
- [`test_cluster_cron_job.py`](../../../../../tests/test_cluster_cron_job.py) — keep; T17 complements with real orchestrator + lifespan
- REQ-39 J-01/J-02 — already cover min_size; T17 adds **time-based** cron trigger
