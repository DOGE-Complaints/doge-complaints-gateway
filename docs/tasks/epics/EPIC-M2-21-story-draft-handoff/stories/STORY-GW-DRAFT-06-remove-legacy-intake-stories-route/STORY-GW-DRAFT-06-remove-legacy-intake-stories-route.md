# STORY-GW-DRAFT-06 — Удаление legacy `POST /intake/stories`

## Meta
- **Key:** `STORY-GW-DRAFT-06-remove-legacy-intake-stories-route`
- **Parent Epic:** [`../../../EPIC-M2-21-story-draft-handoff.md`](../../../EPIC-M2-21-story-draft-handoff.md)
- **Type:** refactor (route removal + runner + docs + tests)
- **Status:** 🟢 Done (P3 gate PASS pkg-000050) — gate 2026-07-11T10:15:42Z
- **Приоритет:** P2 — после [GW-DRAFT-05](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **source:** [`../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Decision Ref:** backlog file above; depends [GW-DRAFT-05](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md); operator decision P1: runner **stash-only** (201 + `draft_id`; submit/cluster E2E → [GW-SEED-03](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md))
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000050-20260711-gw-draft-06-remove-legacy-intake-stories-route.yaml`](../../../../gateway-active-packages/pkg-000050-20260711-gw-draft-06-remove-legacy-intake-stories-route.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **Закрывает:** legacy HTTP-путь GPT-direct intake; выравнивание с browser-submit моделью
- **Зависит от:** [GW-DRAFT-05](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) (чистые контракты stash vs intake bridge)
- **Разблокирует:** runner stash на `/story-drafts` (Done); E2E materialization submit/cluster → [GW-SEED-03](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md); упрощение OpenAPI/security SSOT

## Зачем простыми словами
Рабочий продуктовый путь: GPT стешит черновик (`POST /story-drafts`), браузер сабмитит (`POST /story-drafts/{id}/submit`). Старый `POST /intake/stories` — наследие «GPT сам сабмитит»; он путает контракты, документацию и демо-загрузчик. Нужно убрать **публичный HTTP-роут**, оставив внутренний `handle_story_intake` для submit-bridge.

## Что наблюдаю сейчас (verified по коду)

| Элемент | As-is |
|---------|-------|
| Legacy route | [`asgi_app.py:501`](../../../../../../src/core/api/asgi_app.py) `POST /intake/stories` с `require_public_content_service_auth` |
| Рабочий GPT path | [`asgi_app.py:521`](../../../../../../src/core/api/asgi_app.py) `POST /story-drafts`; submit [`:552`](../../../../../../src/core/api/asgi_app.py) |
| Demo loader | [`simulation_runner.py:207`](../../../../../../tests/simulation_runner.py) → `{gateway_url}/intake/stories` |
| Internal intake | [`handlers.py`](../../../../../../src/core/api/handlers.py) `handle_story_intake` — используется submit path после DRAFT-02 |
| PUBLIC_ROUTES map | [`asgi_app.py:62`](../../../../../../src/core/api/asgi_app.py) `/intake/stories` в policy map |

## Требование / целевое состояние

- Удалить `@app.post("/intake/stories")` и связанный публичный handler wiring из [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py).
- Убрать `/intake/stories` из `PUBLIC_ROUTES` / route policy maps.
- Перевести [`tests/simulation_runner.py`](../../../../../../tests/simulation_runner.py) на `POST /story-drafts` (stash без submitter после DRAFT-05).
- Обновить runtime OpenAPI + [`API_REFERENCE.md`](../../../../../runtime-docs/api-reference/API_REFERENCE.md): единственный GPT write = story-drafts.
- `StoryIntakeRequest` / `parse_story_intake_request` / `handle_story_intake` **остаются** — вызываются только из submit-bridge (`intake_request_from_stash_and_submitter`), не с публичного HTTP.

## Граница и контракт

- **In scope:** `src/core/api/asgi_app.py`, runner, тесты контракта intake route, openapi/docs.
- **Out of scope:** удаление domain types `StoryIntakeRequest` (нужен для internal create_story).
- **Out of scope:** pipeline pkg/audit history — не переписывать (D-DRAFT-6).
- `POST /tallinn/issues` — не трогать (operator manual path).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-draft-06-t01-remove-intake-route-and-policy-map`](./task-gw-draft-06-t01-remove-intake-route-and-policy-map/README.md) | pkg-000050 |
| 2 | [`task-gw-draft-06-t02-runtime-docs-remove-public-intake-path`](./task-gw-draft-06-t02-runtime-docs-remove-public-intake-path/README.md) | pkg-000050 |
| 3 | [`task-gw-draft-06-t03-simulation-runner-story-drafts-stash`](./task-gw-draft-06-t03-simulation-runner-story-drafts-stash/README.md) | pkg-000050 |
| 4 | [`task-gw-draft-06-t04-retire-dedicated-intake-http-tests`](./task-gw-draft-06-t04-retire-dedicated-intake-http-tests/README.md) | pkg-000050 |
| 5 | [`task-gw-draft-06-t05-migrate-pipeline-tests-and-conftest`](./task-gw-draft-06-t05-migrate-pipeline-tests-and-conftest/README.md) | pkg-000050 |
| 6 | [`task-gw-draft-06-t06-story-acceptance-gate`](./task-gw-draft-06-t06-story-acceptance-gate/README.md) | pkg-000050 |
| 7 | [`task-gw-draft-06-t07-audit-r1-story-status-sync`](./task-gw-draft-06-t07-audit-r1-story-status-sync/README.md) | audit override |
| 8 | [`task-gw-draft-06-t08-audit-g2-stale-intake-comment-cleanup`](./task-gw-draft-06-t08-audit-g2-stale-intake-comment-cleanup/README.md) | audit override |
| 9 | [`task-gw-draft-06-t09-audit-g1-retarget-seed-forward-ref`](./task-gw-draft-06-t09-audit-g1-retarget-seed-forward-ref/README.md) | audit override |

## Acceptance Criteria

- [ ] `rg 'POST /intake/stories|"/intake/stories"' src/` → **0** matches (публичный route удалён)
- [ ] `simulation_runner.py` использует `/story-drafts`, не `/intake/stories`
- [ ] `handle_story_intake` вызывается только из submit/internal path (не из удалённого route)
- [ ] OpenAPI не описывает публичный `POST /intake/stories`
- [ ] Контракт-тесты GW-DRAFT-01/02 + full pytest green

## Открытые вопросы

- Нужен ли временный 410 Gone redirect на `/intake/stories` для внешних клиентов? → **default: нет** (GPT уже на story-drafts).
- Runner после stash: создавать stories через отдельный submit flow или только stash для demo? → **P1 decision:** stash-only в T03; submit/cluster E2E → [GW-SEED-03](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md).

## Швы

- Routes: [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py)
- Handlers: [`handlers.py`](../../../../../../src/core/api/handlers.py) `handle_story_intake`, `handle_story_draft_create/submit`
- Contracts: [`intake/contracts.py`](../../../../../../src/core/intake/contracts.py) (после DRAFT-05)
- Runner: [`tests/simulation_runner.py`](../../../../../../tests/simulation_runner.py)
- Cross-ref: [GW-DRAFT-05](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md), [GW-PUBLIC-01](../../../../backlog-stories/issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md) (contrast tests — story-drafts, не intake)
