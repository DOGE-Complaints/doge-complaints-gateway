# STORY-GW-DRAFT-06 — Удаление legacy `POST /intake/stories`

## Meta
- **Key:** `STORY-GW-DRAFT-06-remove-legacy-intake-stories-route`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md)
- **Status:** 🟢 Done (P3 gate PASS pkg-000050) — gate 2026-07-11T10:15:42Z
- **Приоритет:** P2 — после [GW-DRAFT-05](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Тип:** refactor (route removal + runner + docs + tests)
- **Закрывает:** legacy HTTP-путь GPT-direct intake; выравнивание с browser-submit моделью
- **Зависит от:** [GW-DRAFT-05](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) (чистые контракты stash vs intake bridge)
- **Разблокирует:** runner stash на `/story-drafts` (Done); E2E materialization submit/cluster → [GW-SEED-03](../demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md); упрощение OpenAPI/security SSOT

## Зачем простыми словами
Рабочий продуктовый путь: GPT стешит черновик (`POST /story-drafts`), браузер сабмитит (`POST /story-drafts/{id}/submit`). Старый `POST /intake/stories` — наследие «GPT сам сабмитит»; он путает контракты, документацию и демо-загрузчик. Нужно убрать **публичный HTTP-роут**, оставив внутренний `handle_story_intake` для submit-bridge.

## Что наблюдаю сейчас (verified по коду)

| Элемент | As-is |
|---------|-------|
| Legacy route | [`asgi_app.py:501`](../../../../src/core/api/asgi_app.py) `POST /intake/stories` с `require_public_content_service_auth` |
| Рабочий GPT path | [`asgi_app.py:521`](../../../../src/core/api/asgi_app.py) `POST /story-drafts`; submit [`:552`](../../../../src/core/api/asgi_app.py) |
| Demo loader | [`simulation_runner.py:207`](../../../../tests/simulation_runner.py) → `{gateway_url}/intake/stories` |
| Internal intake | [`handlers.py`](../../../../src/core/api/handlers.py) `handle_story_intake` — используется submit path после DRAFT-02 |
| PUBLIC_ROUTES map | [`asgi_app.py:62`](../../../../src/core/api/asgi_app.py) `/intake/stories` в policy map |

## Требование / целевое состояние

- Удалить `@app.post("/intake/stories")` и связанный публичный handler wiring из [`asgi_app.py`](../../../../src/core/api/asgi_app.py).
- Убрать `/intake/stories` из `PUBLIC_ROUTES` / route policy maps.
- Перевести [`tests/simulation_runner.py`](../../../../tests/simulation_runner.py) на `POST /story-drafts` (stash без submitter после DRAFT-05).
- Обновить runtime OpenAPI + [`API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md): единственный GPT write = story-drafts.
- `StoryIntakeRequest` / `parse_story_intake_request` / `handle_story_intake` **остаются** — вызываются только из submit-bridge (`intake_request_from_stash_and_submitter`), не с публичного HTTP.

## Граница и контракт

- **In scope:** `src/core/api/asgi_app.py`, runner, тесты контракта intake route, openapi/docs.
- **Out of scope:** удаление domain types `StoryIntakeRequest` (нужен для internal create_story).
- **Out of scope:** pipeline pkg/audit history — не переписывать (D-DRAFT-6).
- `POST /tallinn/issues` — не трогать (operator manual path).

## Подзадачи

| ID | Задача |
|----|--------|
| **T01** | Change-propagation: grep `/intake/stories`, `handle_story_intake` public callers; удалить route + policy entry в [`asgi_app.py`](../../../../src/core/api/asgi_app.py) |
| **T02** | Runtime docs: [`openapi.yaml`](../../../runtime-docs/api-reference/openapi.yaml), [`API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md), [`security-env-api-access.md`](../../../runtime-docs/security-env-api-access.md) — убрать публичный intake path |
| **T03** | [`simulation_runner.py`](../../../../tests/simulation_runner.py) → `POST /story-drafts`; обновить [`simulation-runner-manual.md`](../../../runtime-docs/testing/simulation-runner-manual.md) |
| **T04** | Тесты: удалить/переписать contract tests на `POST /intake/stories`; grep `intake/stories` в `tests/` = 0 для HTTP path |
| **T05** | Story acceptance gate: full unit suite green; hosted smoke stash без legacy route |

## Acceptance Criteria

- [ ] `rg 'POST /intake/stories|"/intake/stories"' src/` → **0** matches (публичный route удалён)
- [ ] `simulation_runner.py` использует `/story-drafts`, не `/intake/stories`
- [ ] `handle_story_intake` вызывается только из submit/internal path (не из удалённого route)
- [ ] OpenAPI не описывает публичный `POST /intake/stories`
- [ ] Контракт-тесты GW-DRAFT-01/02 + full pytest green

## Открытые вопросы

- Нужен ли временный 410 Gone redirect на `/intake/stories` для внешних клиентов? → **default: нет** (GPT уже на story-drafts).
- Runner после stash: создавать stories через отдельный submit flow или только stash для demo? → **P1 decision (T03):** stash-only; submit/cluster E2E → [GW-SEED-03](../demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md).

## Швы

- Routes: [`asgi_app.py`](../../../../src/core/api/asgi_app.py)
- Handlers: [`handlers.py`](../../../../src/core/api/handlers.py) `handle_story_intake`, `handle_story_draft_create/submit`
- Contracts: [`intake/contracts.py`](../../../../src/core/intake/contracts.py) (после DRAFT-05)
- Runner: [`tests/simulation_runner.py`](../../../../tests/simulation_runner.py)
- Cross-ref: [GW-DRAFT-05](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md), [GW-PUBLIC-01](../issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md) (contrast tests — story-drafts, не intake)
