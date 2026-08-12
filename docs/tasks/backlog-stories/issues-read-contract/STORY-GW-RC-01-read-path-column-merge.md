# STORY-GW-RC-01 — Read-path: merge колонок `id`/`status`/`created_at` (column-as-truth)

## Meta
- **Key:** `STORY-GW-RC-01`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000030](../../gateway-active-packages/pkg-000030-20260619-gw-rc-01-read-path-column-merge.yaml), T01–T06, gate PASS 2026-06-19, 489 unit + integration green, GAP-1/2/4 closed); код-аудит [`audit-gw-rc-01-read-path-column-merge-2026-06-19.md`](../../../analysis/audit-gw-rc-01-read-path-column-merge-2026-06-19.md). SSOT исполнения — pipeline-копия. Раздел «Что наблюдаю сейчас» ниже — до-реализационное состояние (исторический контекст).
- **Приоритет:** P1 (Blocker — пустой дашборд)
- **Закрывает:** GAP-1 (`id`), GAP-2 (`status` — корневая причина), GAP-4 (`created_at`)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Решения интервью:** [`interview-issues-read-contract-2026-06-19.md`](./interview-issues-read-contract-2026-06-19.md) — D-RC-1, D-RC-2, D-RC-3
- **Зависит от:** —
- **Разблокирует:** [GW-RC-02](./STORY-GW-RC-02-type-canonical-on-read.md), [GW-RC-03](./STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)

## Зачем простыми словами
Доска показывает 0 карточек, хотя API возвращает 5 issue. Причина: у каждой issue в ответе **нет `id` и `status`**, а фронт раскладывает карточки по колонкам строго по `status`. `status`/`id`/`created_at` есть в таблице как **колонки**, но read-path их выкидывает и отдаёт только JSON-документ. Надо вернуть колонки в ответ.

## Что наблюдаю сейчас (verified по коду)
- `filter_projection_rows` имеет `(_row_status, payload, created_at)`, но возвращает `dict(payload)` — колонки теряются ([`read_filters.py:209-235`](../../../../src/core/projection/read_filters.py#L209-L235)).
- Фильтр статуса идёт по `payload.get("status")`, не по колонке ([`read_filters.py:210-213`](../../../../src/core/projection/read_filters.py#L210-L213)).
- `list_projections` SELECT без `issue_id`; `get_projection` SELECT только `payload_json` ([`db_supabase.py:617-715`](../../../../src/core/infrastructure/db_supabase.py#L617-L715)).
- Зеркала: `db_sqlite.py`, `repositories.py` (InMemory).

## Требование / целевое состояние (D-RC-2, D-RC-3)
- В каждом объекте ответа `GET /tallinn/issues` и `GET /tallinn/issues/{id}` присутствуют `id`, `status`, `created_at`, взятые **из колонок** (column-as-truth: колонка перетирает значение из payload).
- Фильтр `status` — по колонке `row_status`, не по `payload.status`.
- **Устойчивость:** даже если `payload_json` неполный (нет id/status) — ответ валиден за счёт колонок. Доска работает на текущих 5 записях **без миграции данных**.
- Поведение для всех бэкендов: Supabase, SQLite, InMemory.

## Граница и контракт
- Форма полей не меняется (`id: string`, `status ∈ {NEW,IN_REVIEW,PUBLISHED}`, `created_at: ISO`).
- `type` и legacy-данные — вне этой стори (RC-02/RC-03).
- `payload_json` остаётся (его удаление — RC-04).

## Подзадачи (черновик)
- **T01** — `db_supabase.list_projections`: добавить `issue_id` в SELECT; передавать `(issue_id, status, payload, created_at)` в фильтр.
- **T02** — `read_filters.filter_projection_rows`: принять `issue_id`; собирать ответ как `out = dict(payload); out["id"]=issue_id; out["status"]=row_status; out["created_at"]=created_at`; фильтр статуса по `row_status`.
- **T03** — `db_supabase.get_projection`: SELECT `issue_id,status,payload_json,created_at`; merge как выше.
- **T04** — Зеркально SQLite (`db_sqlite.py`) и InMemory (`repositories.py`).
- **T05** — Acceptance-тесты (см. AC), все бэкенды.

## Acceptance Criteria
- [ ] `GET /tallinn/issues` и `/{id}`: каждый issue имеет `id`, `status`, `created_at` из колонок.
- [ ] При неполном `payload_json` (без id/status) ответ всё равно содержит `id`/`status` из колонок.
- [ ] Фильтр `?status=` работает по колонке (а не по payload).
- [ ] Поведение идентично на Supabase/SQLite/InMemory.
- [ ] Тест-суит без регрессий; добавлен тест «seed неполного payload → есть id/status».

## Открытые вопросы
- Подтвердить, что `created_at` всегда в колонке для всех записей (если нет — оставить опциональным в ответе).
