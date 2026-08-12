# STORY-GW-DRAFT-01 — Стеш черновика истории (create + fetch)

## Meta
- **Key:** `STORY-GW-DRAFT-01`
- **Parent Epic:** [`../../../EPIC-M2-21-story-draft-handoff.md`](../../../EPIC-M2-21-story-draft-handoff.md)
- **Type:** implement (новый ресурс + порт-адаптер store)
- **Status:** 🟢 Done
- **Приоритет:** 🔴 HIGH (ядро M-3; без стеша нет handoff GPT→браузер)
- **source:** [`../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md)
- **Decision Ref:** backlog file above; [`interview-story-draft-handoff-2026-07-03`](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-2**); [`mvp-integration-plan-2026-07-02 §2,§4`](../../../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml`](../../../../gateway-active-packages/pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07 (closed); audit follow-up **T08–T09** Done 2026-07-03 (not in pkg YAML)
- **Зависит от:** —
- **Разблокирует:** [GW-DRAFT-02](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)

## Зачем простыми словами
GPT собрал историю, но сам её не публикует. Он **кладёт готовый JSON во временное хранилище** gateway и получает короткий `draft_id`, который передаёт браузеру через редирект. Браузер потом забирает черновик по этому id. Так контент не уходит в URL — передаём **ссылку, а не payload** (паттерн как OAuth authorization code).

## Что наблюдаю сейчас (verified по коду)
- **Story draft routes:** `POST /story-drafts`, `GET /story-drafts/{draft_id}` ([asgi_app.py](../../../../../../src/core/api/asgi_app.py)); handlers `handle_story_draft_create` / `handle_story_draft_get` ([handlers.py](../../../../../../src/core/api/handlers.py)).
- **Порт `StoryDraftRepository`:** [`domain/contracts.py`](../../../../../../src/core/domain/contracts.py) + адаптеры in_memory/sqlite/supabase ([`infrastructure/`](../../../../../../src/core/infrastructure/)).
- **Сервис-авторизация POST:** `require_public_content_service_auth` — только сервисный токен, без user-слоя.
- **GET user-auth:** stub `require_story_draft_user_auth` до GW-DRAFT-02.

## Требование / целевое состояние (D-DRAFT-2)
- **A. `POST /story-drafts`** — принимает тот же контракт `StoryIntakeRequest`, что `/intake/stories`; **auth = только сервисный токен** (реюз `require_public_content_service_auth`, **без** user-слоя). Валидирует контракт, **сохраняет черновик** (issue НЕ создаётся), возвращает `{draft_id}` — короткий opaque id.
- **B. `GET /story-drafts/{draft_id}`** — отдаёт сохранённый черновик для предпросмотра. **auth = пользовательская** (браузерная сессия; конкретный механизм — [GW-DRAFT-02](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md) через identity `/me`). Неизвестный/протухший id → 404.
- **C. Отдельный store `StoryDraftRepository`** (D-DRAFT-2): новый порт в `domain/contracts.py` + 3 адаптера (in_memory/sqlite/supabase) по образцу `StoryRepository`; черновик **≠** issue.
- **D. TTL** — черновик живёт ограниченно (реком. 1–24ч); по истечении → 404. `in_memory` для demo, `supabase` для durable.
- **E. Ошибки** — общий конверт `build_error_envelope` ([envelope.py:59](../../../../../../src/core/api/envelope.py#L59)): невалидный контракт → `VALIDATION_ERROR` (400); нет/битый сервисный токен → `UNAUTHORIZED` (401).

## Out of scope
- Полный user-auth на GET/submit → [GW-DRAFT-02](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- Supersede/removal GAUTH → GW-DRAFT-03/04
- `POST /story-drafts/{id}/submit` → GW-DRAFT-02

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-draft-01-t01-story-draft-repository-port`](./task-gw-draft-01-t01-story-draft-repository-port/README.md) | pkg-000043 |
| 2 | [`task-gw-draft-01-t02-story-draft-store-adapters`](./task-gw-draft-01-t02-story-draft-store-adapters/README.md) | pkg-000043 |
| 3 | [`task-gw-draft-01-t03-post-story-drafts-route`](./task-gw-draft-01-t03-post-story-drafts-route/README.md) | pkg-000043 |
| 4 | [`task-gw-draft-01-t04-get-story-drafts-route`](./task-gw-draft-01-t04-get-story-drafts-route/README.md) | pkg-000043 |
| 5 | [`task-gw-draft-01-t05-story-draft-contract-tests`](./task-gw-draft-01-t05-story-draft-contract-tests/README.md) | pkg-000043 |
| 6 | [`task-gw-draft-01-t06-runtime-docs-story-drafts-api`](./task-gw-draft-01-t06-runtime-docs-story-drafts-api/README.md) | pkg-000043 |
| 7 | [`task-gw-draft-01-t07-story-acceptance-gate`](./task-gw-draft-01-t07-story-acceptance-gate/README.md) | pkg-000043 |
| 8 | [`task-gw-draft-01-t08-di-story-draft-repository-propagation`](./task-gw-draft-01-t08-di-story-draft-repository-propagation/README.md) | audit override (`run_mode=gw_draft_01_audit_followup`) |
| 9 | [`task-gw-draft-01-t09-story-gate-full-unit-suite`](./task-gw-draft-01-t09-story-gate-full-unit-suite/README.md) | audit override (`run_mode=gw_draft_01_audit_followup`) |

## Acceptance Criteria
- [x] `POST /story-drafts` c валидным сервисным токеном сохраняет черновик и возвращает `{draft_id}`; issue при этом **не создаётся**.
- [x] Без/с неверным сервисным токеном → **401 `UNAUTHORIZED`**, fail-closed.
- [x] `GET /story-drafts/{draft_id}` отдаёт ранее сохранённый JSON; неизвестный/протухший id → **404**.
- [x] Невалидный контракт истории → **400** `DOMAIN_ERROR` (как `/intake/stories`).
- [x] TTL соблюдается: по истечении — 404.
- [x] Черновик хранится **отдельным** `StoryDraftRepository`, не смешан со story-store (D-DRAFT-2).

## Runtime-docs дельта
- [`api-reference/openapi.yaml`](../../../../../runtime-docs/api-reference/openapi.yaml) `paths:` — добавить `/story-drafts` (POST) и `/story-drafts/{draft_id}` (GET) по образцу `/intake/stories`.
- [`api-reference/API_REFERENCE.md`](../../../../../runtime-docs/api-reference/API_REFERENCE.md) — раздел стеша.
- [`story-persistence-model.md`](../../../../../runtime-docs/story-persistence-model.md) — модель draft-store + TTL.

## Открытые под-вопросы (реализация)
- Форма `draft_id` (opaque random + TTL); durable-cleanup для supabase-адаптера.
- Нужен ли на `GET` доп. one-time-секрет, или достаточно user-auth из GW-DRAFT-02 (привязка draft→user после логина).

## Швы
Новые роуты — [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py); auth — [`security.py`](../../../../../../src/core/api/security.py); контракт — [`intake/contracts.py`](../../../../../../src/core/intake/contracts.py); порт — [`domain/contracts.py`](../../../../../../src/core/domain/contracts.py); адаптеры/DI — [`infrastructure/`](../../../../../../src/core/infrastructure/); ошибки — [`envelope.py`](../../../../../../src/core/api/envelope.py).

## Зависимости / связь
Потребитель `GET`+submit: [SPA-ID-12](../../../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Поставщик `POST`: [GPT-SUBMIT-01](../../../../../../../GPT%20UI/docs/tasks/backlog-stories/story-submit-handoff/STORY-GPT-SUBMIT-01-redirect-handoff.md).
