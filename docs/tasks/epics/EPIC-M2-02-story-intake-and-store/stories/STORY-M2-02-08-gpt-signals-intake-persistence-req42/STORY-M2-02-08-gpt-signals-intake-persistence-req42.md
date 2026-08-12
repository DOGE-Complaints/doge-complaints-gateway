# STORY-M2-02-08: GPT signals intake → story_signals (REQ-42)

## Meta
- Key: `STORY-M2-02-08`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Intake / GPT classifier signals
- Decision Ref: [`../../../../../requirements/42-gpt-signals-story-intake-extension.md`](../../../../../requirements/42-gpt-signals-story-intake-extension.md)
- Depends on: STORY-M2-02-07 (REQ-33 intake v2); REQ-34 (`story_signals` table); GPT UI REQ-23 wire ([`GPT UI/docs/analysis/tasks/bullrun-launch-index.md`](../../../../../../GPT UI/docs/analysis/tasks/bullrun-launch-index.md) EPIC-M1-10 Done)
- Operative queue: [`../../../../gateway-active-packages/pkg-000022-20260522-req42-gpt-signals-story-intake.yaml`](../../../../gateway-active-packages/pkg-000022-20260522-req42-gpt-signals-story-intake.yaml)
- Skill declared: `python-pro`

## Story Goal
Принять опциональный intake-блок `gpt_signals` (`severity`, `impact_estimation`, `problem_status`) и персистировать в `story_signals` с `extraction_policy = "gpt.story_classifier.v1"`, без изменения `StoryRecord`.

## Product decisions (fixed)
- Использовать существующий `StorySignalStore.save_signals()` — не новый `save_story_signals()` ([`src/core/domain/contracts.py`](../../../../../src/core/domain/contracts.py)).
- Пост-save best-effort persist; ошибка записи signals не ломает HTTP 202 ([`42-gpt-signals-story-intake-extension.md`](../../../../../requirements/42-gpt-signals-story-intake-extension.md) §3.2).
- Константа политики рядом с `STORY_EMBEDDING_POLICY_VERSION` в [`src/core/application/services.py`](../../../../../src/core/application/services.py).

## Scope
- T01–T04 по вложенным README (contract → service DI → tests → runtime docs).

## Out of scope (REQ-42 §6)
- Индексация/поиск по gpt_signals.
- Кластеризация по severity/impact.
- `gpt.story_classifier.v2`.
- Изменения в `GPT UI/` (отдельный продукт; wire уже в REQ-23).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-02-08-t01-intake-contract-gpt-signals`](./task-m2-02-08-t01-intake-contract-gpt-signals/README.md) | pkg-000022 |
| 2 | [`task-m2-02-08-t02-story-intake-service-signals-persist`](./task-m2-02-08-t02-story-intake-service-signals-persist/README.md) | pkg-000022 |
| 3 | [`task-m2-02-08-t03-gpt-signals-intake-acceptance-tests`](./task-m2-02-08-t03-gpt-signals-intake-acceptance-tests/README.md) | pkg-000022 |
| 4 | [`task-m2-02-08-t04-runtime-openapi-api-reference`](./task-m2-02-08-t04-runtime-openapi-api-reference/README.md) | pkg-000022 |

## AC / DoD (story level)
- [x] REQ-42 §5: intake с `gpt_signals` → HTTP 202; row в `story_signals` с policy `gpt.story_classifier.v1`.
- [x] Без `gpt_signals` → HTTP 202, запись для этой policy не создаётся.
- [x] Невалидный enum → HTTP 400.
- [x] Ошибка persist signals не блокирует успешный intake.
- [x] `builder_resolve_queue.py --project gateway --verify` → `ok 4 paths` (pkg-000022).
- [x] Story gate: [`story-acceptance-gate-STORY-M2-02-08.md`](./story-acceptance-gate-STORY-M2-02-08.md) — PASS (2026-05-22).
