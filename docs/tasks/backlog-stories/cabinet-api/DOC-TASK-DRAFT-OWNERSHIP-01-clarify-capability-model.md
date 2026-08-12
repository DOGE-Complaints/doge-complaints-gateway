# DOC-TASK-DRAFT-OWNERSHIP-01 — Зафиксировать модель доступа к черновикам (capability-token) в документации

- **Тип:** Documentation task (не product story — правки только в доках, код и поведение не трогаем).
- **Пакет:** cabinet-api (владелец решения D-CAB02 про draft↔owner на чтении).
- **Статус:** ✅ Done (2026-07-23)
- **Источник:** [audit-mvp-scope-hard-2026-07-21.md](../../../analysis/audit-mvp-scope-hard-2026-07-21.md) §F2.
- **Приоритет:** P2 (security-семантика без явного решения → неоднозначность).
- **Коррекция факта (analysis.mdc):** исходный audit F2 ошибочно писал last-writer-wins; код `set_owner` = **first-wins** (`ON CONFLICT DO NOTHING` / `ignore-duplicates` / `setdefault`). Ниже — verified модель.

## Проблема (verified)

Фактическое поведение доступа к черновикам долго не было описано как осознанная модель:

- `GET /story-drafts/{draft_id}` возвращает `record.payload` **любому** предъявителю валидного user-токена, знающему `draft_id` — **проверки владельца на чтении нет** ([`handlers.py:585-610`](../../../../src/core/api/handlers.py#L585)).
- `POST /story-drafts/{draft_id}/submit` также не сверяет caller с `draft_owner` — author = `/me` ([`handlers.py:724-751`](../../../../src/core/api/handlers.py#L724)).
- На успешном GET вызывается `set_owner(draft_id, submitter)` по правилу **first-wins** ([`db_sqlite.py:792`](../../../../src/core/infrastructure/db_sqlite.py#L792), [`db_supabase.py:697`](../../../../src/core/infrastructure/db_supabase.py#L697), [`repositories.py:161`](../../../../src/core/infrastructure/repositories.py#L161)) — первый читатель остаётся владельцем для `GET /story-drafts/current`; повторный GET другого user **не** перетирает строку.
- `draft_id = secrets.token_urlsafe(16)` — 128-битный неугадываемый токен ([`handlers.py:536`](../../../../src/core/api/handlers.py#L536)).

**Риск при утечке `draft_id`:** чужой read/submit payload (capability), а не hijack `draft_owner` повторным GET.

## Решение (задокументировано, без изменения кода)

Доступ = **capability-based** (знание `draft_id` + валидный user-Bearer); ownership-gate на GET/submit **не выполняется by design**. Ассоциация `/current` = **first-wins**. Strict ownership — post-MVP.

## Где и как править (scope — выполнено)

1. CAB-02 backlog + pipeline — first-wins + Security note.
2. cabinet-api INDEX — принятое решение (ссылка на этот doc-task).
3. DRAFT-01 / DRAFT-02 — Security note + SSOT-ссылка.
4. OpenAPI / API_REFERENCE — capability + first-wins на GET/current/submit.
5. Dashboard F2 / audit F2 — закрыты с корректной формулировкой first-wins.

### Единый «Security note» (canonical)

> **Security model — story drafts (MVP).** Доступ = capability: `draft_id` — неугадываемый 128-битный токен (`secrets.token_urlsafe(16)`). Валидный user-Bearer + знание `draft_id` = право на чтение и сабмит; отдельная проверка владельца на GET/submit **не выполняется by design**. Ассоциация `draft_owner` на успешном GET — **first-wins** (`set_owner`: INSERT … DO NOTHING / ignore-duplicates / setdefault); `GET /story-drafts/current` scoped по первому записанному владельцу. Модель достаточна, пока `draft_id` не утекает (логи, реферер, пересланные ссылки). Strict ownership-gate — post-MVP, вне скоупа.

SSOT: этот файл.

## Явно НЕ входит

- Любые изменения кода/поведения (ownership-gate, смена first-wins) — product story.
- Решение об ужесточении модели — фиксируем только текущую как осознанную.

## Definition of Done

- [x] Нет утверждений last-writer-wins про `set_owner`/drafts, расходящихся с кодом.
- [x] Единый «Security note» (first-wins + capability) в CAB-02, DRAFT-01/02 и API reference; SSOT — этот файл.
- [x] Отсутствие ownership-гейта на GET/submit описано как **by design**.
- [x] cabinet-api INDEX фиксирует принятое решение (не «открытый долг»).
- [x] Dashboard / audit F2 → закрыты.
