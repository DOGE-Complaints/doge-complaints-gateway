# STORY-GW-CAB-02 — Current draft discovery (`GET /story-drafts/current`)

## Meta
- **Key:** `STORY-GW-CAB-02-current-draft-discovery`
- **Пакет:** [`cabinet-api/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — implemented via pipeline pkg-000053 (see SSOT below)
- **Приоритет:** 🟠 MED — разблокирует SPA CAB-04 State C (Resume draft)
- **Тип:** feature (new user-scoped read endpoint + draft↔owner association)
- **Tier:** **2 → разблокирован** (draft↔user решён: gateway-ассоциация при первом чтении)
- **Источник:** [`STORY-SPA-CAB-api-requirements.md` §0 + §2.1 + §4](../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Разблокирует:** SPA `CAB-04` State C (кнопка Resume pending draft)
- **Зависит от:** browser-Bearer→`/me` (GW-DRAFT-02, есть); `StoryDraftRepository` (GW-DRAFT-01, есть)

**SSOT (pipeline):** [`STORY-GW-CAB-02-current-draft-discovery.md`](../../epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-02-current-draft-discovery/STORY-GW-CAB-02-current-draft-discovery.md) — решения D-CAB02-1..3 + queue pkg-000053 T01–T06.

## Зачем простыми словами
Если у юзера есть незавершённый черновик (GPT застешил, человек ещё не засабмитил) — кабинет показывает «Resume draft». Для этого нужно узнать `draft_id` текущего юзера. Черновик кладёт GPT под сервис-токеном **без автора**, но браузер **читает** его под своей Supabase-сессией — вот здесь gateway и записывает связь `draft_id→человек`.

## MVP-контракт (§0, contract-first)
```
GET /story-drafts/current   (browser Bearer)
200 → { "data": { "draft_id": str, "last_edited_at": str } }   // либо { "data": null }, если нет pending-черновика
```

## Решения интервью (D-CAB02, 2026-07-14)
- **D-CAB02-1 (draft↔user):** **gateway-ассоциация при первом чтении (first-wins).** На `GET /story-drafts/{id}` под user-сессией gateway пишет связь `draft_id→sub` (`draft_owner`; `set_owner` = INSERT … DO NOTHING / ignore-duplicates / setdefault). `GET /story-drafts/current` находит pending-черновик по `sub`. Даёт **кросс-девайс** resume.
- **D-CAB02-2 (`last_edited_at`):** поле `updated_at` на `StoryDraftRecord`, инициализируется `= created_at` на стеше; эндпоинт отдаёт его как `last_edited_at`.
- **D-CAB02-3 («current»):** **последний непросроченный по `created_at`** (`expires_at > now`, `ORDER BY created_at DESC LIMIT 1`).

## Что наблюдаю сейчас (verified по коду)
Эта pass-1 постановка **свернута**: факты по реализации и решения D-CAB02-1..3 ведутся в pipeline SSOT (см. ссылку выше).

## Границы
- **In scope (MVP):** обнаружение pending-draft текущего юзера + draft↔owner ассоциация.
- **Вне scope:** редактирование черновика; сам submit (GW-DRAFT-02); удаление истёкших (существующий TTL).
- **Приватность / security:** `draft_owner` — **first-wins** на успешном GET; `draft_id` — секретный opaque capability-токен (первый читатель = владелец для `/current` в happy-path). Ownership-gate на GET **не** выполняется by design.

> **Security model — story drafts (MVP).** Доступ = capability: `draft_id` — неугадываемый 128-битный токен (`secrets.token_urlsafe(16)`). Валидный user-Bearer + знание `draft_id` = право на чтение и сабмит; отдельная проверка владельца на GET/submit **не выполняется by design**. Ассоциация `draft_owner` на успешном GET — **first-wins** (`set_owner`: INSERT … DO NOTHING / ignore-duplicates / setdefault); `GET /story-drafts/current` scoped по первому записанному владельцу. Модель достаточна, пока `draft_id` не утекает (логи, реферер, пересланные ссылки). Strict ownership-gate — post-MVP, вне скоупа.
>
> SSOT: [DOC-TASK-DRAFT-OWNERSHIP-01](./DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md).

## Примечание
Если нужно понять текущий runtime/контракт/тесты — см. pipeline story SSOT и audit:
- `docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md`
