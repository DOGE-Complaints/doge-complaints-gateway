# STORY-M2-18-03: Local real HTTP smoke (REQ-41)

## Meta
- Key: `STORY-M2-18-03`
- Parent Epic: [`../../../EPIC-M2-18-cross-layer-contract-testing.md`](../../../EPIC-M2-18-cross-layer-contract-testing.md)
- Type: Technical Story
- Status: Done (Build)
- Stream: M2 quality / production coverage / Layer 6
- Decision Ref: [`../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-01, GAP-41-06; PS-01, PS-19
- Operative queue: [`../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml`](../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml) — T15–T16
- Depends on: STORY-M2-18-01/02 (REQ-39); [`tests/simulation_runner.py`](../../../../../tests/simulation_runner.py) (EPIC-M2-16)
- Blocks: —

## Story Goal
Добавить opt-in smoke suite против **реального** HTTP-стека (uvicorn + TCP), используя canvas-сценарии и `httpx` sync/async clients; offline CI не ломается (`pytest.skip` без `LOCAL_SERVER_URL`).

## Scope
- `tests/smoke/test_local_server_smoke.py` (LS-01..06)
- `tests/smoke/test_local_server_async_read.py` (AC-01..03)
- `tests/smoke/conftest.py` — URL fixture, health reachability guard

## Out of scope
- Запуск uvicorn в pytest (оператор стартует сервер вручную, REQ-41 §7)
- Полный прогон 130 сценариев (остаётся CLI `simulation_runner.py`)
- Изменение prod routing/middleware без failing test

## Nested tasks

| Order | Task folder | Gap |
|-------|-------------|-----|
| 15 | [`task-m2-18-03-t15-gap41-01-local-server-smoke`](./task-m2-18-03-t15-gap41-01-local-server-smoke/README.md) | GAP-41-01 |
| 16 | [`task-m2-18-03-t16-gap41-06-local-server-async-read`](./task-m2-18-03-t16-gap41-06-local-server-async-read/README.md) | GAP-41-06 |

### Audit follow-up (REQ-41, 2026-05-18)

| Order | Task folder | Gap |
|-------|-------------|-----|
| 22 | [`task-m2-18-03-t22-audit-gap41-01-pytest-asyncio-dev-install`](./task-m2-18-03-t22-audit-gap41-01-pytest-asyncio-dev-install/README.md) | GAP-AUDIT-REQ41-01 |

- Source: [`audit-req41-production-coverage-target-state-2026-05-18.md`](../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md) §9
- Override: `run_mode=story18_audit_req41_followup` in [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)
- Audit follow-up closed (T22, 2026-05-19)

## AC / DoD (story level)
- [x] AC-41-1: LS-01..LS-06 pass with running uvicorn on `LOCAL_SERVER_URL`
- [x] AC-41-4: AC-01..AC-03 async read tests pass with same server
- [x] All smoke tests skip cleanly when `LOCAL_SERVER_URL` unset or server unreachable
- [x] Story gate after T15–T16 — [`story-acceptance-gate-STORY-M2-18-03.md`](./story-acceptance-gate-STORY-M2-18-03.md)

## Traceability: REQ-41 §3 → tasks

| Gap | PS | Task |
|-----|-----|------|
| GAP-41-01 | PS-01, PS-19 | T15 |
| GAP-41-06 | PS-07..10 (async read) | T16 |

## Conflict-scan
- REQ-39 Zone N (`test_e2e_sandbox_full_pipeline.py`) — TestClient only; this story adds real HTTP layer
- Do not duplicate intake payload builders — import from `tests.simulation_runner`
