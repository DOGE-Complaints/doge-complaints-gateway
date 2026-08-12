# EPIC-M2-02: Story Intake and Story Store

## Epic Meta
- Status: In Progress
- Priority: Critical
- Owner: TBD
- Target: Sprint 1-2

## Business Goal
Зафиксировать story как первичный актив продукта и обеспечить intake без forced collapse в issue.

## Problem Statement
Legacy intake ориентирован на complaint-flow и не обеспечивает корректный story-first lifecycle.

## Scope
### In Scope
- story intake contracts;
- story persistence (immutable narrative + mutable derived layers);
- readiness states;
- origin linkage (intake source tracking);
- **фиксация авторства:** сохранение `submitter.external_user_id` (opaque, формат не фиксируется) и при необходимости `identity_issuer`, полученных из OAuth-потока на стороне GPT/IdP — без потери на пути intake → store → evidence;
- idempotent intake command.

### Out of Scope
- кластеризация;
- issue projection;
- evidence pack.

## Stakeholders
- Product Lead
- Data/Backend team
- QA team

## Dependencies
- EPIC-M2-01 completed
- REQ-33 (STORY-M2-02-07), REQ-34 (`story_signals`); REQ-42 — [`42-gpt-signals-story-intake-extension.md`](../requirements/42-gpt-signals-story-intake-extension.md); REQ-43 — [`43-institution-json-story-column.md`](../requirements/43-institution-json-story-column.md); REQ-44 — [`44-api-reference-field-provenance-clarity.md`](../requirements/44-api-reference-field-provenance-clarity.md); REQ-46 — [`46-demo-services-enablement-and-response-transparency.md`](../requirements/46-demo-services-enablement-and-response-transparency.md)

## Success Metrics
- 100% историй сохраняются как отдельные объекты;
- отсутствует forced merge на intake этапе;
- intake errors классифицируются и наблюдаемы.

## Epic Acceptance Criteria
- intake endpoint принимает narrative package по новому контракту (включая блок `submitter` при политике с логином);
- story layer хранит original narrative отдельно от интерпретаций;
- внешний идентификатор автора сохраняется в персистентной модели и доступен для lineage;
- readiness lifecycle покрыт unit/integration тестами;
- mapping legacy->story documented.

## Risks and Mitigation
- Риск: неполные истории блокируют intake.  
  Mitigation: partial-ready статусы и мягкая валидация на intake.

## Definition of Done
- intake и store стабильно работают;
- данные готовы для profile enrichment;
- документация по контракту опубликована.

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-02-01 | [Story intake request/response contract](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-01-story-intake-request-response-contract.md) | Done (Committed) |
| STORY-M2-02-02 | [Story repository lifecycle and authorship linkage](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-02-story-repository-lifecycle-and-authorship-linkage.md) | Done (Committed) |
| STORY-M2-02-03 | [Intake idempotency key handling](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md) | Done (Committed) |
| STORY-M2-02-04 | [Intake observability and error taxonomy](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-04-intake-observability-and-error-taxonomy.md) | Done (Committed) |
| STORY-M2-02-05 | [Supabase bootstrap schema parity](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-05/STORY-M2-02-05-supabase-bootstrap-schema-parity.md) | Implemented (Waiting Acceptance) |
| STORY-M2-02-06 | [Data model registry §16 follow-up](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-06/STORY-M2-02-06-data-model-registry-section-16-followup.md) | Implemented (Waiting Acceptance/Commits) + final tails T07–T10 (Todo; `run_mode=story02_06_sec16_final_tails`) |
| STORY-M2-02-07 | [Multilingual intake contract v2 (REQ-33)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/STORY-M2-02-07-multilingual-intake-contract-v2.md) | Done (Awaiting Commits) |
| STORY-M2-02-08 | [GPT signals intake → story_signals (REQ-42)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-08-gpt-signals-intake-persistence-req42/STORY-M2-02-08-gpt-signals-intake-persistence-req42.md) | Done (Awaiting Commits) |
| STORY-M2-02-09 | [institution_json story column + intake (REQ-43)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/STORY-M2-02-09-institution-json-story-column-req43.md) | Done (Awaiting Commits) |
| STORY-M2-02-10 | [API_REFERENCE field provenance clarity (REQ-44)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-10-api-reference-field-provenance-clarity-req44/STORY-M2-02-10-api-reference-field-provenance-clarity-req44.md) | Done (Awaiting Commits) |
| STORY-M2-02-11 | [Runtime OpenAPI status enum alignment (GAP-YAML-04)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-11-runtime-openapi-status-enum-alignment/STORY-M2-02-11-runtime-openapi-status-enum-alignment.md) | Todo (P5 scaffold ready 2026-05-26; override-run only) |
| STORY-M2-02-12 | [Demo services enablement and intake transparency (REQ-46)](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md) | Done (Awaiting Commits); audit follow-up T08–T10 Todo |

## Operative queue (REQ-46)
- [`pkg-000026-20260528-req46-demo-services-intake-transparency.yaml`](../gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml) — STORY-M2-02-12 T01–T07 (immutable after P1); active via [`gateway-active-package.current.yaml`](../gateway-active-package.current.yaml); T07 gated by SQL null check (REQ §2.4). Audit follow-up T08–T10 — override `run_mode=story02_12_audit_req46_followup` only ([`audit-req46-demo-services-intake-transparency-2026-06-02.md`](../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md)).

## Operative queue (GAP-YAML-04 — override-run only)
- [`pkg-000025-20260526-gap-yaml-04-status-enum.yaml`](../gateway-active-packages/pkg-000025-20260526-gap-yaml-04-status-enum.yaml) — STORY-M2-02-11 T01 (immutable after P5); **не активирован в `gateway-active-package.current.yaml`** — запуск через метку `run_mode=gap_yaml_04_status_enum_followup` в [`Gateway_builder.plan.md`](../../../../.cursor/plans/Gateway_builder.plan.md); decision_ref [`handoff-gateway-runtime-yaml-status-enum.md`](../../../../GPT%20UI/docs/analysis/handoff-gateway-runtime-yaml-status-enum.md) (cross-project handoff, `gpt` builder GIM-131 2026-05-26).

## Operative queue (REQ-44)
- [`pkg-000024-20260525-req44-api-reference-field-provenance.yaml`](../gateway-active-packages/pkg-000024-20260525-req44-api-reference-field-provenance.yaml) — STORY-M2-02-10 T01–T02 (immutable after P1)

## Operative queue (REQ-43)
- [`pkg-000023-20260523-req43-institution-json-story-column.yaml`](../gateway-active-packages/pkg-000023-20260523-req43-institution-json-story-column.yaml) — STORY-M2-02-09 T01–T06 (immutable after P1)

## Operative queue (REQ-42)
- [`pkg-000022-20260522-req42-gpt-signals-story-intake.yaml`](../gateway-active-packages/pkg-000022-20260522-req42-gpt-signals-story-intake.yaml) — STORY-M2-02-08 T01–T04 (immutable)
