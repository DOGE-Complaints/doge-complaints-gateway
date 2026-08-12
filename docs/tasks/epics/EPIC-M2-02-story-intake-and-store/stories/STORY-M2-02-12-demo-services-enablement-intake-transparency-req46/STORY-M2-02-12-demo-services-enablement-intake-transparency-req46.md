# STORY-M2-02-12: Demo services enablement and intake transparency (REQ-46)

## Meta
- Key: `STORY-M2-02-12`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Awaiting Commits) — T07 superseded by override T11–T13 (title hint purge wave)
- Audit Ref: [`../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md)
- Stream: M2 Intake / demo geo stub / response transparency
- Decision Ref: [`../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../requirements/46-demo-services-enablement-and-response-transparency.md)
- Depends on: STORY-M2-02-07 (REQ-33), STORY-M2-02-08 (REQ-42), STORY-M2-09-07 (REQ-37 logging baseline)
- Operative queue: [`../../../../gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml`](../../../../gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml)
- Paired requirement (ops): REQ-47 — out of gateway pkg scope

## Why this epic (reuse justification)
1. REQ-46 меняет intake contract, `services.py`, `handlers.py`, OpenAPI intake response — домен [`EPIC-M2-02`](../../../EPIC-M2-02-story-intake-and-store.md) (intake + store).
2. REQ-42/43/44 уже размещены как STORY-M2-02-08…10 в том же эпике.
3. **Не EPIC-M2-08:** эпик geo Done; REQ-46 — demo stub для intake pipeline, не production geocoding (REQ §5).
4. **Не EPIC-M2-13:** старый gap-backlog GAP-001..007, не REQ-46.

## Story Goal
Расширить demo geo stub (EN/ET/RU + районы Таллинна), сделать HTTP 202 intake прозрачным через `data.intake_notes`, усилить observability (geo miss INFO, gpt_signals drop WARNING), опционально убрать dead `narrative_title_hint*` columns после SQL gate.

## Scope
- T01–T06 по вложенным README (geo → services → contract → handler → docs → tests).
- T07 — условный schema cleanup (только при SQL gate = 0).

## Out of scope (REQ-46 §5)
- REQ-47: Railway env, GPT scripts (`location_query`, `origin_source`).
- Real geocoding API (OpenCage/Nominatim production).
- `narrative_summary_json` generation (GPT-side).
- Изменение lifecycle `status` enum/semantics.

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-02-12-t01-estonia-geo-lookup-stub-providers`](./task-m2-02-12-t01-estonia-geo-lookup-stub-providers/README.md) | pkg-000026 |
| 2 | [`task-m2-02-12-t02-story-intake-result-services-logging`](./task-m2-02-12-t02-story-intake-result-services-logging/README.md) | pkg-000026 |
| 3 | [`task-m2-02-12-t03-intake-notes-contract-response-builder`](./task-m2-02-12-t03-intake-notes-contract-response-builder/README.md) | pkg-000026 |
| 4 | [`task-m2-02-12-t04-handlers-wire-intake-notes-flags`](./task-m2-02-12-t04-handlers-wire-intake-notes-flags/README.md) | pkg-000026 |
| 5 | [`task-m2-02-12-t05-openapi-api-reference-intake-notes`](./task-m2-02-12-t05-openapi-api-reference-intake-notes/README.md) | pkg-000026 |
| 6 | [`task-m2-02-12-t06-intake-transparency-acceptance-tests`](./task-m2-02-12-t06-intake-transparency-acceptance-tests/README.md) | pkg-000026 |
| 7 | [`task-m2-02-12-t07-narrative-title-hint-cleanup-gated`](./task-m2-02-12-t07-narrative-title-hint-cleanup-gated/README.md) | pkg-000026 (superseded → T11–T13) |
| 8 | [`task-m2-02-12-t08-audit-gap46-01-idempotency-gpt-signals-replay-flag`](./task-m2-02-12-t08-audit-gap46-01-idempotency-gpt-signals-replay-flag/README.md) | audit override |
| 9 | [`task-m2-02-12-t09-audit-gap46-02-gpt-signals-persist-exception-test`](./task-m2-02-12-t09-audit-gap46-02-gpt-signals-persist-exception-test/README.md) | audit override |
| 10 | [`task-m2-02-12-t10-audit-gap46-03-geo-lookup-order-collision-tests`](./task-m2-02-12-t10-audit-gap46-03-geo-lookup-order-collision-tests/README.md) | audit override |
| 11 | [`task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration`](./task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration/README.md) | title hint purge override |
| 12 | [`task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer`](./task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer/README.md) | title hint purge override |
| 13 | [`task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity`](./task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity/README.md) | title hint purge override |

## Audit follow-up (2026-06-02)

Hard audit [`audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md): T01–T06 verified; G1–G3 closed via T08–T10 (2026-06-02). Override `run_mode=story02_12_audit_req46_followup` — complete. T07 gate COUNT=192 (test-only) → override `run_mode=story02_12_req46_title_hint_purge_and_cleanup` (T11–T13).

## Story AC / DoD (from REQ-46 §4)
- [ ] Geo: `Таллин` / `Kalamaja` / `Tartu` / `Нарва` → корректные `geo_admin_*` (см. REQ §4 Geo expansion).
- [ ] Logging: `intake.geo_not_resolved` INFO при непустом `location_query` + miss; WARNING `intake.gpt_signals_drop` при `story_signal_store is None`.
- [ ] Response: `data.intake_notes.geo_resolved` и `gpt_signals_persisted` в 202; OpenAPI + API_REFERENCE обновлены.
- [ ] Tests: suite без регрессий; dedicated acceptance module green.
- [ ] T07 (optional): title_hint columns dropped только если SQL gate = 0.
- [ ] `builder_resolve_queue.py --project gateway --verify` → `ok 7 paths` (pkg-000026).

## Traceability: REQ-46 -> tasks
- REQ-46 §2.1 -> T01
- REQ-46 §2.2, §2.3B -> T02
- REQ-46 §2.3A -> T03
- REQ-46 §2.3C -> T04
- REQ-46 §2.3D -> T05
- REQ-46 §4 (geo, logging, intake_notes) -> T06
- REQ-46 §2.4 -> T07 (gated)
- audit G1 -> T08; audit G2 -> T09; audit G3 -> T10
