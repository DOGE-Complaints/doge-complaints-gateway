# STORY-M2-02-09: institution_json — story column + intake (REQ-43)

## Meta
- Key: `STORY-M2-02-09`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Intake / story persistence / issue projection
- Decision Ref: [`../../../../../requirements/43-institution-json-story-column.md`](../../../../../requirements/43-institution-json-story-column.md)
- Depends on: STORY-M2-02-07 (REQ-33 intake v2); REQ-40 (dominant-story projection pattern); STORY-M2-02-08 (REQ-42, non-blocking)
- Operative queue: [`../../../../gateway-active-packages/pkg-000023-20260523-req43-institution-json-story-column.yaml`](../../../../gateway-active-packages/pkg-000023-20260523-req43-institution-json-story-column.yaml)
- Skill declared: `python-pro`

## Story Goal
Принять опциональное `narrative.institution` `{et, ru, en}`, персистировать в `stories.institution_json`, и прокинуть в `doge_issues.payload_json.institution` как i18n-объект при promotion.

## Product decisions (fixed)
- Intake validation: `parse_optional_i18n_dict("institution", ...)` — как `summary` ([`src/core/domain/narrative_i18n.py`](../../../../../src/core/domain/narrative_i18n.py)).
- Dominant story для institution в кластере: `select_dominant_story()` ([`src/core/projection/extraction_policy.py`](../../../../../src/core/projection/extraction_policy.py) L26–32), не `readiness_score` на `StoryRecord`.
- `payload_json.institution` — **объект** `{et, ru, en}` (оператор); обновить `DOGEIssue` / `ProjectionInput` / `read_filters` (T04).
- In-memory persistence: [`repositories.py`](../../../../../src/core/infrastructure/repositories.py) `InMemoryStoryRepository` — не `db_inmemory.py` (REQ §3.4 устарел).
- GPT UI wire — вне gateway pkg (REQ-22).

## Scope
- T01–T06 по вложенным README (contract → domain → stores → projection → tests → docs).

## Out of scope (REQ-43 §6)
- SPA UI для institution.
- Canonical institution registry / классификация.
- Full-text индекс по `institution_json`.
- `GPT UI/instructions/api-orchestrator.md`.

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-02-09-t01-intake-contract-narrative-institution`](./task-m2-02-09-t01-intake-contract-narrative-institution/README.md) | pkg-000023 |
| 2 | [`task-m2-02-09-t02-story-record-and-intake-mapping`](./task-m2-02-09-t02-story-record-and-intake-mapping/README.md) | pkg-000023 |
| 3 | [`task-m2-02-09-t03-story-store-institution-json-persistence`](./task-m2-02-09-t03-story-store-institution-json-persistence/README.md) | pkg-000023 |
| 4 | [`task-m2-02-09-t04-issue-projection-institution-propagation`](./task-m2-02-09-t04-issue-projection-institution-propagation/README.md) | pkg-000023 |
| 5 | [`task-m2-02-09-t05-institution-intake-acceptance-tests`](./task-m2-02-09-t05-institution-intake-acceptance-tests/README.md) | pkg-000023 |
| 6 | [`task-m2-02-09-t06-runtime-docs-openapi-persistence-model`](./task-m2-02-09-t06-runtime-docs-openapi-persistence-model/README.md) | pkg-000023 |

## AC / DoD (story level)
- [ ] REQ-43 §5: intake с `narrative.institution` → HTTP 202; `institution_json` в stories.
- [ ] Без `narrative.institution` → HTTP 202, `institution_json IS NULL`.
- [ ] Неполный i18n institution → HTTP 400.
- [ ] `payload_json.institution` = `{et, ru, en}` из dominant story при issue create.
- [ ] `builder_resolve_queue.py --project gateway --verify` → `ok 6 paths` (pkg-000023).
- [ ] Story gate: [`story-acceptance-gate-STORY-M2-02-09.md`](./story-acceptance-gate-STORY-M2-02-09.md) — PASS после P3.
