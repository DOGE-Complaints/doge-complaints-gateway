# STORY-M2-18-02: Cross-layer contract zones A–I (REQ-39)

## Meta
- Key: `STORY-M2-18-02`
- Parent Epic: [`../../../EPIC-M2-18-cross-layer-contract-testing.md`](../../../EPIC-M2-18-cross-layer-contract-testing.md)
- Type: Technical Story
- Status: Done (Build); audit follow-up closed (T14)
- Stream: M2 quality / intake-DB-DI contract testing
- Decision Ref: [`../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../requirements/39-cross-layer-contract-testing.md) §1–9 (zones A–I)
- Operative queue: [`../../../../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml`](../../../../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml) — tasks T06–T13
- Depends on: STORY-M2-18-01 recommended first (N depends on J+K+L); EPIC-M2-02 bootstrap stories (partial coverage exists)
- Blocks: Epic M2-18 closure

## Story Goal
Закрыть legacy SEAM-зоны A–I: bootstrap SQL ↔ Python fields, PostgREST coercion, intake mapping, repository parity, API/service facade, logging, auxiliary stores, config/DI — плюс REQ-39 documentation hygiene.

## Scope
- Extend: `test_supabase_bootstrap_schema.py`, `test_config_loading.py`
- New: `test_supabase_deserialization_contracts.py`, `test_story_intake_field_persistence.py`, `test_story_repository_contract.py`, `test_api_service_contract.py`, `test_logging_setup.py`, `test_store_contract_parity.py`
- T13: README-index, stale `req-cross-layer-contract-testing.md` refs → `39-cross-layer-contract-testing.md`

## Out of scope
- Zones J–N (STORY-M2-18-01)
- Replacing `test_stories_schema_cross_layer_invariant.py` — T08 extends seam C, does not duplicate MVP invariant

## Nested tasks

| Order | Task folder | Zone |
|-------|-------------|------|
| 6 | [`task-m2-18-02-t06-zone-ag-bootstrap-schema-contracts`](./task-m2-18-02-t06-zone-ag-bootstrap-schema-contracts/README.md) | A, G |
| 7 | [`task-m2-18-02-t07-zone-b-supabase-deserialization-contracts`](./task-m2-18-02-t07-zone-b-supabase-deserialization-contracts/README.md) | B |
| 8 | [`task-m2-18-02-t08-zone-c-story-intake-field-persistence`](./task-m2-18-02-t08-zone-c-story-intake-field-persistence/README.md) | C |
| 9 | [`task-m2-18-02-t09-zone-d-story-repository-contract`](./task-m2-18-02-t09-zone-d-story-repository-contract/README.md) | D |
| 10 | [`task-m2-18-02-t10-zone-e-api-service-contract`](./task-m2-18-02-t10-zone-e-api-service-contract/README.md) | E |
| 11 | [`task-m2-18-02-t11-zone-f-logging-setup-contract`](./task-m2-18-02-t11-zone-f-logging-setup-contract/README.md) | F |
| 12 | [`task-m2-18-02-t12-zone-h-store-contract-parity`](./task-m2-18-02-t12-zone-h-store-contract-parity/README.md) | H |
| 13 | [`task-m2-18-02-t13-zone-i-config-loading-and-req39-hygiene`](./task-m2-18-02-t13-zone-i-config-loading-and-req39-hygiene/README.md) | I + hygiene |
| 14 | [`task-m2-18-02-t14-audit-gap39-g01-named-test`](./task-m2-18-02-t14-audit-gap39-g01-named-test/README.md) | audit G |

## Audit follow-up (2026-05-18)

- Source: [`audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-G01
- Execution order in override wave: after STORY-M2-18-01 T06 (see `Gateway_builder.plan.md`)

## AC / DoD (story level)
- [x] AC-39-2: Zones A–I specs implemented per REQ-39 §1–9
- [x] AC-39-8: Closure table in §«Системный инвариант» reflected in story gate
- [x] AC-39-9: Full offline run `pytest tests/ --ignore=tests/integration -q` green (394 passed)
- [x] AC-39-1 hygiene: no stale `req-cross-layer-contract-testing.md` references; README-index lists REQ-39
- [x] Story gate: [`story-acceptance-gate-STORY-M2-18-02.md`](./story-acceptance-gate-STORY-M2-18-02.md) — PASS

## Traceability: REQ-39 §16 rows 6–13 → tasks

| REQ row | Zones | Task |
|---------|-------|------|
| 6 | A, G | T06 |
| 7 | B | T07 |
| 8 | C | T08 |
| 9 | D | T09 |
| 10 | E | T10 |
| 11 | F | T11 |
| 12 | H | T12 |
| 13 | I | T13 |

## Traceability: audit §8 → T14

| Audit gap | Task |
|-----------|------|
| GAP-39-G01 | T14 |
