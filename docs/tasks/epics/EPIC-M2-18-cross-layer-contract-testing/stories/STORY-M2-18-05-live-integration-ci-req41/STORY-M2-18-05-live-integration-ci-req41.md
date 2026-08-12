# STORY-M2-18-05: Live Supabase CI + architecture closure (REQ-41)

## Meta
- Key: `STORY-M2-18-05`
- Parent Epic: [`../../../EPIC-M2-18-cross-layer-contract-testing.md`](../../../EPIC-M2-18-cross-layer-contract-testing.md)
- Type: Technical Story
- Status: Done (Build)
- Stream: M2 quality / live integration / CI / docs
- Decision Ref: [`../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-05; AC-41-5, AC-41-8
- Operative queue: [`../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml`](../../../../gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml) — T20–T21
- Depends on: existing `tests/integration/supabase/*`; operator GitHub Secrets
- Blocks: Epic REQ-41 closure

## Story Goal
Сделать live Supabase integration **обязательной** на merge в `main` (CI stage `integration-live`) и закрыть документацию PS-* matrix (Layer 6 status, README-index REQ-41).

## Scope
- `pytest.mark.live_integration` + pyproject markers
- `.github/workflows/integration-live.yml` (new — no workflow in repo today)
- Mark/wire existing live tests under `tests/integration/supabase/`
- Update [`13-testing-and-quality-architecture.md`](../../../../../solution%20architecture/13-testing-and-quality-architecture.md) §6; [`README-index.md`](../../../../../requirements/README-index.md) REQ-41 entry

## Out of scope
- Changing Supabase DDL in prod without separate REQ
- Mandatory `LOCAL_SERVER_URL` in CI (smoke remains opt-in)
- `pkg-000020` edits

## Nested tasks

| Order | Task folder | Gap / AC |
|-------|-------------|----------|
| 20 | [`task-m2-18-05-t20-gap41-05-live-integration-ci`](./task-m2-18-05-t20-gap41-05-live-integration-ci/README.md) | GAP-41-05 |
| 21 | [`task-m2-18-05-t21-ac41-8-testing-architecture-doc`](./task-m2-18-05-t21-ac41-8-testing-architecture-doc/README.md) | AC-41-8 |

### Audit follow-up (REQ-41, 2026-05-18)

| Order | Task folder | Gap |
|-------|-------------|-----|
| 23 | [`task-m2-18-05-t23-audit-gap41-02-supabase-secret-naming-docs`](./task-m2-18-05-t23-audit-gap41-02-supabase-secret-naming-docs/README.md) | GAP-AUDIT-REQ41-02 |

- Source: [`audit-req41-production-coverage-target-state-2026-05-18.md`](../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md) §7, §9
- Override: `run_mode=story18_audit_req41_followup` in [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)
- Audit follow-up closed (T23, 2026-05-19)

## AC / DoD (story level)
- [x] AC-41-5: CI stage `integration-live` on `main`; secrets documented
- [x] AC-41-8: arch doc PS matrix reflects target state; README-index lists REQ-41
- [x] Story gate after T20–T21 — [`story-acceptance-gate-STORY-M2-18-05.md`](./story-acceptance-gate-STORY-M2-18-05.md)

## Traceability

| Item | Task |
|------|------|
| GAP-41-05 (PS-13, PS-14, PS-25) | T20 |
| AC-41-8 | T21 |

## Conflict-scan
- Live tests already skip without `SUPABASE_TEST_URL` — T20 adds marker + CI gate, not rewrite test logic
- Operator must configure GitHub Secrets before CI goes green
