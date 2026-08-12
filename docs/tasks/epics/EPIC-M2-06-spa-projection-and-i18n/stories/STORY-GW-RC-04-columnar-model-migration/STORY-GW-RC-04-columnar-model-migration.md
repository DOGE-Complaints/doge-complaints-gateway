# STORY-GW-RC-04 — Колоночная модель проекции (удаление `payload_json`)

## Meta
- **Key:** `STORY-GW-RC-04`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** ADR-grade (архитектурное решение + миграция)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P4 (Architecture — после блокеров; НЕ блокирует доску)
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-04-columnar-model-migration.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-04-columnar-model-migration.md)
- **Закрывает:** структурный дубль колонка↔`payload_json` (источник «путаницы» из интервью)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Decision Ref:** backlog file above; [`interview-issues-read-contract-2026-06-19.md`](../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) — D-RC-5
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml`](../../../../gateway-active-packages/pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **9** тасков T01–T09
- **Зависит от:** [GW-RC-01](../STORY-GW-RC-01-read-path-column-merge/STORY-GW-RC-01-read-path-column-merge.md), [GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read/STORY-GW-RC-02-type-canonical-on-read.md), [GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data/STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)

## Зачем простыми словами
Сейчас одни и те же поля (`id/status/created_at`) хранятся дважды — как колонки и внутри `payload_json`. Это источник рассинхрона и путаницы (что считать правдой). Цель — перевести проекцию на колоночную модель и убрать дублирующий JSON-документ, чтобы у каждого факта было одно место.

## Что наблюдаю сейчас (verified по коду)
- `save_projection` пишет и колонки (`issue_id,status,created_at,updated_at,policy_version`), и `payload_json` (= `to_public_dict()`, дубль) ([`db_supabase.py:617`](../../../../../../../src/core/infrastructure/db_supabase.py#L617)).
- `payload_json` используется в **10 файлах**: `db_supabase.py`, `db_sqlite.py`, `repositories.py`, `read_filters.py`, `supabase/bootstrap/000_full_init.sql`, init-миграция, **вьюха `spa_issues_dashboard_view`** (`20260427_1615_*`), `tests/test_db_backed_pipeline_e2e.py`, `tests/test_supabase_issue_projection_store_contract.py`, `scripts/reproject_issue_i18n.py`.
- Вложенные поля payload: i18n-карты `title/summary/description/institution` ({et,ru,en}), массивы `labels/original_locale`, объект `geo` — **не сводятся к плоским скалярным колонкам**.

## Зафиксированное ограничение (важно)
«Только колонки» **недостижимо** для вложенных структур: i18n/geo/labels потребуют либо `jsonb`-колонок, либо explode на `_et/_ru/_en`. То есть результат — **скаляры в колонках + `jsonb` для структур**; дубль `id/status/created_at` уходит, но JSON частично остаётся как типизированные jsonb-колонки (а не один общий blob).

## Требование / целевое состояние (D-RC-5)
- Перевести все поля контракта в колонки (скаляры + jsonb для i18n/geo/labels), убрать общий `payload_json`.
- Переписать: write-path (`save_projection`), read-path (сборка ответа из колонок), `read_filters` (фильтры по колонкам/jsonb вместо payload), 3 бэкенда (Supabase/SQLite/InMemory).
- Решить судьбу вьюхи `spa_issues_dashboard_view` (переписать на колонки/jsonb).
- Миграция данных существующих строк из `payload_json` в колонки; затем удаление колонки `payload_json`.
- Зеркальные правки бэкфилл-скрипта и контракт-тестов.

## Граница и контракт
- Внешний контракт API (форма ответа issue) **не меняется** — только внутреннее хранение.
- Идёт строго ПОСЛЕ RC-01..03 (доска уже работает; это не блокер).

## Product decisions (fixed at T01 ADR)
- **ADR:** [`task-gw-rc-04-t01-adr-column-schema-and-view-decision/adr-column-schema-d-rc-5.md`](./task-gw-rc-04-t01-adr-column-schema-and-view-decision/adr-column-schema-d-rc-5.md) — jsonb i18n/geo; keep `issues_dashboard` on columnar fields.
- **API contract:** unchanged external issue shape (parent «Граница и контракт»).

## Out of scope
- Изменение SPA / BoardPage кода
- FE-side contract tests (gateway guarantees storage + API shape only)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-04-t01-adr-column-schema-and-view-decision`](./task-gw-rc-04-t01-adr-column-schema-and-view-decision/README.md) | pkg-000033 |
| 2 | [`task-gw-rc-04-t02-schema-migration-doge-issues-columns`](./task-gw-rc-04-t02-schema-migration-doge-issues-columns/README.md) | pkg-000033 (gated: T01 ADR) |
| 3 | [`task-gw-rc-04-t03-write-path-save-projection-columnar`](./task-gw-rc-04-t03-write-path-save-projection-columnar/README.md) | pkg-000033 |
| 4 | [`task-gw-rc-04-t04-read-path-and-filters-columnar`](./task-gw-rc-04-t04-read-path-and-filters-columnar/README.md) | pkg-000033 |
| 5 | [`task-gw-rc-04-t05-three-backend-parity-supabase-sqlite-inmemory`](./task-gw-rc-04-t05-three-backend-parity-supabase-sqlite-inmemory/README.md) | pkg-000033 |
| 6 | [`task-gw-rc-04-t06-issues-dashboard-view-columnar`](./task-gw-rc-04-t06-issues-dashboard-view-columnar/README.md) | pkg-000033 |
| 7 | [`task-gw-rc-04-t07-data-migration-drop-payload-json`](./task-gw-rc-04-t07-data-migration-drop-payload-json/README.md) | pkg-000033 |
| 8 | [`task-gw-rc-04-t08-contract-tests-and-reproject-script`](./task-gw-rc-04-t08-contract-tests-and-reproject-script/README.md) | pkg-000033 |
| 9 | [`task-gw-rc-04-t09-story-acceptance-gate`](./task-gw-rc-04-t09-story-acceptance-gate/README.md) | pkg-000033 |
| 10 | [`task-gw-rc-04-t10-readiness-doge-issues-columnar-columns`](./task-gw-rc-04-t10-readiness-doge-issues-columnar-columns/README.md) | audit override (`run_mode=gw_rc_04_audit_followup`) |
| 11 | [`task-gw-rc-04-t11-columnar-round-trip-legacy-fallback-tests`](./task-gw-rc-04-t11-columnar-round-trip-legacy-fallback-tests/README.md) | audit override (`run_mode=gw_rc_04_audit_followup`) |

## Acceptance Criteria
- [x] ADR зафиксировал представление i18n/geo (jsonb vs explode) и судьбу вьюхи.
- [x] Внешняя форма ответа issue идентична до/после (контракт-тесты зелёные).
- [x] `payload_json` удалён; данные перенесены без потерь.
- [x] Фильтры/сортировка работают по колонкам/jsonb; 3 бэкенда согласованы.
- [x] Тест-суит без регрессий.

## Открытые вопросы (closed T01 ADR)
- i18n: **jsonb columns** (not explode).
- geo: **geo_json** jsonb (not admin scalar columns on doge_issues).
- `issues_dashboard`: **kept**, rewritten on columnar fields.
