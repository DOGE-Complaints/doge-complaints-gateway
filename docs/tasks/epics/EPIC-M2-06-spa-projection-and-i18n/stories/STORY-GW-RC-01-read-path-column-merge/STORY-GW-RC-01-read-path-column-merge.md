# STORY-GW-RC-01 — Read-path: merge колонок `id`/`status`/`created_at` (column-as-truth)

## Meta
- **Key:** `STORY-GW-RC-01`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 (Blocker — пустой дашборд)
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-01-read-path-column-merge.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-01-read-path-column-merge.md)
- **Закрывает:** GAP-1 (`id`), GAP-2 (`status` — корневая причина), GAP-4 (`created_at`)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Decision Ref:** backlog file above; [`interview-issues-read-contract-2026-06-19.md`](../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) — D-RC-1, D-RC-2, D-RC-3
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000030-20260619-gw-rc-01-read-path-column-merge.yaml`](../../../../gateway-active-packages/pkg-000030-20260619-gw-rc-01-read-path-column-merge.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06; audit follow-up **T07** вне pkg (`run_mode=gw_rc_01_audit_followup`)
- **Зависит от:** —
- **Разблокирует:** GW-RC-02, GW-RC-03 (backlog package)

## Зачем простыми словами
Доска показывает 0 карточек, хотя API возвращает 5 issue. Причина: у каждой issue в ответе **нет `id` и `status`**, а фронт раскладывает карточки по колонкам строго по `status`. `status`/`id`/`created_at` есть в таблице как **колонки**, но read-path их выкидывает и отдаёт только JSON-документ. Надо вернуть колонки в ответ.

## Что наблюдаю сейчас (verified по коду)
- `filter_projection_rows` имеет `(_row_status, payload, created_at)`, но возвращает `dict(payload)` — колонки теряются ([`read_filters.py:209-235`](../../../../../../../src/core/projection/read_filters.py#L209-L235)).
- Фильтр статуса идёт по `payload.get("status")`, не по колонке ([`read_filters.py:210-213`](../../../../../../../src/core/projection/read_filters.py#L210-L213)).
- `list_projections` SELECT без `issue_id`; `get_projection` SELECT только `payload_json` ([`db_supabase.py:617-715`](../../../../../../../src/core/infrastructure/db_supabase.py#L617-L715)).
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

## Product decisions (fixed, P1 materialization)
- **Merge rule:** `out = dict(payload); out["id"] = issue_id; out["status"] = row_status; out["created_at"] = created_at` — column overrides JSON (D-RC-2).
- **Status filter:** `?status=` применяется к колонке `row_status`, не к `payload.status`.
- **`created_at` mandatory:** column-as-truth; поле **всегда** присутствует в ответе (ISO из колонки; InMemory fallback → `updated_at` если колонка пуста). Audit G3 → T07.

## Out of scope
- Канонизация `type` на чтении (GW-RC-02)
- Гарантия контракта / гигиена legacy-данных (GW-RC-03)
- Удаление `payload_json` / колоночная миграция (GW-RC-04)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-01-t01-read-filters-column-merge`](./task-gw-rc-01-t01-read-filters-column-merge/README.md) | pkg-000030 |
| 2 | [`task-gw-rc-01-t02-supabase-list-get-select-merge`](./task-gw-rc-01-t02-supabase-list-get-select-merge/README.md) | pkg-000030 |
| 3 | [`task-gw-rc-01-t03-sqlite-list-get-parity`](./task-gw-rc-01-t03-sqlite-list-get-parity/README.md) | pkg-000030 |
| 4 | [`task-gw-rc-01-t04-inmemory-list-get-parity`](./task-gw-rc-01-t04-inmemory-list-get-parity/README.md) | pkg-000030 |
| 5 | [`task-gw-rc-01-t05-acceptance-tests-incomplete-payload`](./task-gw-rc-01-t05-acceptance-tests-incomplete-payload/README.md) | pkg-000030 |
| 6 | [`task-gw-rc-01-t06-story-acceptance-gate`](./task-gw-rc-01-t06-story-acceptance-gate/README.md) | pkg-000030 |
| 7 | [`task-gw-rc-01-t07-mandatory-created-at-on-read`](./task-gw-rc-01-t07-mandatory-created-at-on-read/README.md) | audit override (`run_mode=gw_rc_01_audit_followup`) |

## Audit gap map (post-audit 2026-06-19)

| Gap | Task | Status |
|-----|------|--------|
| G3 — `created_at` может отсутствовать в ответе | T07 | Done (2026-06-19) |
| G1 type → RC-02 | — | backlog |
| G2 legacy fields → RC-03 | — | backlog |

## Acceptance Criteria
- [ ] `GET /tallinn/issues` и `/{id}`: каждый issue имеет `id`, `status`, `created_at` из колонок.
- [ ] При неполном `payload_json` (без id/status) ответ всё равно содержит `id`/`status` из колонок.
- [ ] Фильтр `?status=` работает по колонке (а не по payload).
- [ ] Поведение идентично на Supabase/SQLite/InMemory.
- [ ] Тест-суит без регрессий; добавлен тест «seed неполного payload → есть id/status».

## Открытые вопросы
- ~~Подтвердить, что `created_at` всегда в колонке~~ — закрыто: mandatory column-as-truth (T07 audit follow-up).
