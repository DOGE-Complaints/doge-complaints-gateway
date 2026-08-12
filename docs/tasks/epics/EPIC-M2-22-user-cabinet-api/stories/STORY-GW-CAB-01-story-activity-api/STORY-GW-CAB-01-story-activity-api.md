# STORY-GW-CAB-01 — Story Activity API (`GET /story-activity`)

## Meta
- **Key:** `STORY-GW-CAB-01-story-activity-api`
- **Parent Epic:** [`../../../EPIC-M2-22-user-cabinet-api.md`](../../../EPIC-M2-22-user-cabinet-api.md)
- **Type:** feature (new user-scoped read endpoint)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — разблокирует SPA CAB-04 States A/B/E (сейчас на stub)
- **Tier:** **1** — реализуемо на существующих данных (`StoryRecord.submitter_external_user_id`)
- **source:** [`../../../../backlog-stories/cabinet-api/STORY-GW-CAB-01-story-activity-api.md`](../../../../backlog-stories/cabinet-api/STORY-GW-CAB-01-story-activity-api.md)
- **Источник:** [`STORY-SPA-CAB-api-requirements.md` §0 + §2.2 + §4](../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Разблокирует:** SPA `CAB-04` (Story Activity block)
- **Зависит от:** browser-Bearer→`/me` паттерн (GW-DRAFT-02, есть)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000052-20260713-gw-cab-01-story-activity-api.yaml`](../../../../gateway-active-packages/pkg-000052-20260713-gw-cab-01-story-activity-api.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06

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
| Элемент | Реальность |
|---------|-----------|
| Автор на истории | `StoryRecord.submitter_external_user_id` + `submitter_identity_issuer` **хранятся** ([contracts.py:48-49](../../../../../../src/core/domain/contracts.py#L48); sqlite [db_sqlite.py:183](../../../../../../src/core/infrastructure/db_sqlite.py#L183), supabase [db_supabase.py:65](../../../../../../src/core/infrastructure/db_supabase.py#L65)) |
| Query по автору | **нет** — `StoryRepository` даёт `list_stories()` (все) / `get_story(id)` ([contracts.py:70-87](../../../../../../src/core/domain/contracts.py#L70)); `list_by_submitter` отсутствует |
| Статус истории | `StoryLifecycleStatus` = `accepted/partial_ready/ready_for_profile/clustered` ([contracts.py:20](../../../../../../src/core/domain/contracts.py#L20)) — **нет** `published/under_review` |
| Статус issue-проекции | `DOGEIssueStatus` = `DRAFT/PUBLISHED` ([enums.py:6](../../../../../../src/core/projection/enums.py#L6)) — тоже **нет** `under_review` |
| Auth-паттерн | browser Bearer → `/me` → author: `IdentityMeClient` + `require_story_draft_read_user` (GW-DRAFT-02) — переиспользуем |

## Открытые вопросы (решить в T01)
1. **Источник «status»:** статус истории (`StoryLifecycleStatus`) или issue-проекции (`DRAFT/PUBLISHED`)? Кабинет показывает историю или её issue?
2. **Маппинг на UI-enum:** `published/under_review` ← из чего? (напр. `PUBLISHED→published`, всё остальное `→under_review`? согласовать с SPA CAB-04).
3. **Определение метрик:** `submitted` = все мои истории? `published`/`under_review` = разбивка по статусу? считаем истории или issue?
4. **Реализация scoping:** новый repo-метод `list_by_submitter(sub)` (эффективно на БД) vs фильтрация `list_stories()` в приложении.

## Scope
- **In scope (MVP):** user-scoped read «мои истории + метрики»; author из `/me`.

## Вне scope
- запись; пагинация (если понадобится — pass-2); issue-детали.

## Acceptance Criteria
- **AC-1:** GET /story-activity (browser Bearer) → 200 SuccessEnvelope с data.metrics + data.stories по MVP-контракту
- **AC-2:** Author scoping: gateway форвардит Bearer в identity /me → sub → фильтр историй по автору
- **AC-3:** In scope: user-scoped read «мои истории + метрики»; author из /me
- **AC-4:** Вне scope: запись; пагинация; issue-детали

## Решения (T01 — 2026-07-13)
- **D-CAB01-1 (status source):** cabinet row status = **issue projection** `DOGEIssueStatus` via `issue_story_links` → `get_projection(issue_id)`; stories без issue link → `under_review`
- **D-CAB01-2 (UI enum):** `PUBLISHED→published`; все остальные governed/legacy statuses (включая `DRAFT` alias) → `under_review` (SPA §0 line 23: `PUBLISHED/DRAFT ↔ published/under_review`)
- **D-CAB01-3 (metrics):** `submitted` = count all stories for `sub`; `published` / `under_review` = split by mapped row status (count **stories**, not issues)
- **D-CAB01-4 (scoping impl):** `StoryRepository.list_stories_by_submitter(submitter_external_user_id)` — DB-level filter sqlite + supabase
