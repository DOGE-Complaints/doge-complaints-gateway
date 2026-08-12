# STORY-GW-CAB-01 — Story Activity API (`GET /story-activity`)

## Meta
- **Key:** `STORY-GW-CAB-01-story-activity-api`
- **Пакет:** [`cabinet-api/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — implemented via pipeline pkg-000052 (see SSOT below)
- **Приоритет:** 🟠 MED — разблокирует SPA CAB-04 States A/B/E (сейчас на stub)
- **Тип:** feature (new user-scoped read endpoint)
- **Tier:** **1** — реализуемо на существующих данных (`StoryRecord.submitter_external_user_id`)
- **Источник:** [`STORY-SPA-CAB-api-requirements.md` §0 + §2.2 + §4](../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Разблокирует:** SPA `CAB-04` (Story Activity block)
- **Зависит от:** browser-Bearer→`/me` паттерн (GW-DRAFT-02, есть)

**SSOT (pipeline):** [`STORY-GW-CAB-01-story-activity-api.md`](../../epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-01-story-activity-api/STORY-GW-CAB-01-story-activity-api.md) — решения D-CAB01-1..4 + queue pkg-000052 T01–T06.

## Зачем простыми словами
В кабинете юзер видит **свои** истории: список (id / статус / дата) и метрики (сколько submitted / published / under review). Сейчас такого API нет: `GET /tallinn/issues` публичный и без per-user фильтра. Нужен новый эндпоинт «моя активность», где автор берётся из сессии (`/me`), а не из запроса.

## MVP-контракт (§0, contract-first)
```
GET /story-activity        (browser Bearer)
200 → { "data": {
  "metrics": { "submitted": int, "published": int, "under_review": int },
  "stories": [ { "story_id": str, "status": "published"|"under_review", "created_at": str } ]
} }
```
Author scoping: gateway форвардит Bearer в identity `/me` → `sub` → фильтр историй по автору.

## Что наблюдаю сейчас (verified по коду)
Эта pass-1 постановка **свернута**: факты по реализации и решения D-CAB01-1..4 ведутся в pipeline SSOT (см. ссылку выше).

## Границы
- **In scope (MVP):** user-scoped read «мои истории + метрики»; author из `/me`.
- **Вне scope:** запись; пагинация (если понадобится — pass-2); issue-детали.

## Примечание
Если нужно понять текущий runtime/контракт/тесты — см. pipeline story SSOT и audit:
- `docs/analysis/audit-gw-cab-01-story-activity-api-2026-07-13.md`
