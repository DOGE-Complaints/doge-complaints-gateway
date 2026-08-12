# STORY-GW-CAB-02 — Current draft discovery (`GET /story-drafts/current`)

## Meta
- **Key:** `STORY-GW-CAB-02-current-draft-discovery`
- **Parent Epic:** [`../../../EPIC-M2-22-user-cabinet-api.md`](../../../EPIC-M2-22-user-cabinet-api.md)
- **Type:** feature (new user-scoped read endpoint + draft↔owner association)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — разблокирует SPA CAB-04 State C (Resume draft)
- **Tier:** **2 → разблокирован** (draft↔user решён: gateway-ассоциация при первом чтении)
- **source:** [`../../../../backlog-stories/cabinet-api/STORY-GW-CAB-02-current-draft-discovery.md`](../../../../backlog-stories/cabinet-api/STORY-GW-CAB-02-current-draft-discovery.md)
- **Источник:** [`STORY-SPA-CAB-api-requirements.md` §0 + §2.1 + §4](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Разблокирует:** SPA `CAB-04` State C (кнопка Resume pending draft)
- **Зависит от:** browser-Bearer→`/me` (GW-DRAFT-02, есть); `StoryDraftRepository` (GW-DRAFT-01, есть)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000053-20260714-gw-cab-02-current-draft-discovery.yaml`](../../../../gateway-active-packages/pkg-000053-20260714-gw-cab-02-current-draft-discovery.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **decision_ref:** backlog + SPA §0/§2.1

## Зачем простыми словами
Если у юзера есть незавершённый черновик (GPT застешил, человек ещё не засабмитил) — кабинет показывает «Resume draft». Для этого нужно узнать `draft_id` текущего юзера. Черновик кладёт GPT под сервис-токеном **без автора**, но браузер **читает** его под своей Supabase-сессией — вот здесь gateway и записывает связь `draft_id→человек`.

## MVP-контракт (§0, contract-first)
```
GET /story-drafts/current   (browser Bearer)
200 → { "data": { "draft_id": str, "last_edited_at": str } }   // либо { "data": null }, если нет pending-черновика
```

## Решения интервью (D-CAB02, 2026-07-14)
- **D-CAB02-1 (draft↔user):** **gateway-ассоциация при первом чтении (first-wins).** На `GET /story-drafts/{id}` под user-сессией gateway пишет связь `draft_id→sub` (`draft_owner`; `set_owner` = INSERT … DO NOTHING / ignore-duplicates / setdefault). `GET /story-drafts/current` находит pending-черновик по `sub`. Даёт **кросс-девайс** resume. (Отклонены: client-side storage — только same-device; исключение из MVP.)
- **D-CAB02-2 (`last_edited_at`):** **ввести трекинг правок** — поле `updated_at` на `StoryDraftRecord`, инициализируется `= created_at` на стеше, bump при будущих правках черновика; эндпоинт отдаёт его как `last_edited_at`. (Пока пути правки нет → `updated_at == created_at`; инфраструктура готова к редактированию.)
- **D-CAB02-3 («current»):** **последний непросроченный по `created_at`** (`expires_at > now`, `ORDER BY created_at DESC LIMIT 1`).

## Что наблюдаю сейчас (verified по коду)
| Элемент | Реальность |
|---------|-----------|
| Запись черновика | `StoryDraftRecord` = `{draft_id, payload, created_at, expires_at}` — **автора и `updated_at` НЕТ** ([contracts.py:110-117](../../../../../../src/core/domain/contracts.py#L110)) |
| Чтение под сессией | `GET /story-drafts/{draft_id}` за `_STORY_DRAFT_READ_DEPS` (browser Bearer→`/me`) ([asgi_app.py:514](../../../../../../src/core/api/asgi_app.py#L514)); `handle_story_draft_get` сейчас **не** получает `sub` |
| draft↔owner | связи **нет** — таблицы/порта `draft_owner` не существует |
| TTL | one-shot, `expires_at` (`STORY_DRAFT_TTL_SECONDS`, default 86400); `delete_draft` после submit |

## Требование / целевое состояние (D-CAB02-1/2/3)

### A. Домен
1. `StoryDraftRecord` + поле **`updated_at: datetime`** (D-CAB02-2), `= created_at` на стеше.
2. Новый порт **`DraftOwnerRepository`** (Protocol): `set_owner(draft_id, sub)` (**first-wins** / idempotent insert, не overwrite), `get_current_draft(sub) -> StoryDraftRecord | None` (join draft_owner×story_drafts, `expires_at > now`, latest by `created_at`).

### B. Инфраструктура
3. Адаптеры `DraftOwnerRepository`: in-memory / sqlite / supabase + миграция таблицы `draft_owner(draft_id PK, submitter_external_user_id, created_at)`.
4. Миграция `story_drafts`: столбец `updated_at` (backfill `= created_at`).

### C. Ассоциация (change-propagation)
5. `handle_story_draft_get` принимает `submitter_external_user_id` (из `request.state.user_introspection.sub`) → `draft_owner.set_owner(draft_id, sub)` при успешном чтении (best-effort, не ломает чтение при сбое записи).
6. Route `GET /story-drafts/{draft_id}` ([asgi_app.py:514](../../../../../../src/core/api/asgi_app.py#L514)) — прокинуть `sub` в handler.

### D. Новый эндпоинт
7. Route **`GET /story-drafts/current`** за `_STORY_DRAFT_READ_DEPS` → `handle_story_draft_current(sub)` → `get_current_draft(sub)` → `{draft_id, last_edited_at: updated_at.isoformat()}` или `{data: null}`.
8. OpenAPI: описать `/story-drafts/current` (+ nullable data).

## Границы
- **In scope:** обнаружение pending-draft текущего юзера + draft↔owner ассоциация.
- **Вне scope:** редактирование черновика (updated_at готов, но UI/route правки — не здесь); сам submit (GW-DRAFT-02); удаление истёкших (существующий TTL).
- **Приватность / security:** `draft_owner` — **first-wins** на успешном GET; `draft_id` — секретный opaque capability-токен (первый читатель = владелец для `/current` в happy-path). Ownership-gate на GET **не** выполняется by design.

> **Security model — story drafts (MVP).** Доступ = capability: `draft_id` — неугадываемый 128-битный токен (`secrets.token_urlsafe(16)`). Валидный user-Bearer + знание `draft_id` = право на чтение и сабмит; отдельная проверка владельца на GET/submit **не выполняется by design**. Ассоциация `draft_owner` на успешном GET — **first-wins** (`set_owner`: INSERT … DO NOTHING / ignore-duplicates / setdefault); `GET /story-drafts/current` scoped по первому записанному владельцу. Модель достаточна, пока `draft_id` не утекает (логи, реферер, пересланные ссылки). Strict ownership-gate — post-MVP, вне скоупа.
>
> SSOT: [`DOC-TASK-DRAFT-OWNERSHIP-01`](../../../../backlog-stories/cabinet-api/DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md).

## Швы
- Домен: [`domain/contracts.py`](../../../../../../src/core/domain/contracts.py) (`StoryDraftRecord`, новый `DraftOwnerRepository`)
- Инфра: [`infrastructure/`](../../../../../../src/core/infrastructure/) (`repositories.py`/`db_sqlite.py`/`db_supabase.py`/`providers.py`) + миграции
- Handlers/route: [`api/handlers.py`](../../../../../../src/core/api/handlers.py) (`handle_story_draft_get` + новый `handle_story_draft_current`), [`api/asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (route `/story-drafts/current`, прокид `sub` в `/story-drafts/{id}`)
- OpenAPI: [`openapi.yaml`](../../../../runtime-docs/api-reference/openapi.yaml)

## Acceptance Criteria
- [x] `GET /story-drafts/current` под browser-Bearer возвращает `{draft_id,last_edited_at}` последнего непросроченного черновика юзера (D-CAB02-3) или `{data: null}`
- [x] Ассоциация `draft_id→sub` пишется на `GET /story-drafts/{id}` под сессией; **кросс-девайс** (другой браузер того же юзера находит черновик)
- [x] Изоляция: юзер не видит чужой pending-черновик (owner-scoped) — доказано тестом
- [x] Просроченный (`expires_at<=now`) и уже засабмиченный (`delete_draft`) черновик в `current` не попадают
- [x] `last_edited_at` = `updated_at` (сейчас `= created_at`); поле готово к будущему трекингу правок
- [x] Full offline suite (`-m "not live_integration"`) green
