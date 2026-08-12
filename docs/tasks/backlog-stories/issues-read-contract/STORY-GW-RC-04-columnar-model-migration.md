# STORY-GW-RC-04 — Колоночная модель проекции (удаление `payload_json`)

## Meta
- **Key:** `STORY-GW-RC-04`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000033](../../gateway-active-packages/pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml), T01–T09, gate PASS 2026-06-19, 509 unit + integration green, payload_json удалён во всех 3 бэкендах, контракт неизменен); код-аудит [`audit-gw-rc-04-columnar-model-migration-2026-06-20.md`](../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md) (verified; ⚠️ G1 MEDIUM ops: read-path требует новые columnar-колонки, readiness их не проверяет → строгий порядок «миграция раньше деплоя»; G2 — нет выделенного columnar-теста). SSOT исполнения — pipeline-копия. Раздел «Что наблюдаю сейчас» ниже — до-реализационное состояние.
- **Приоритет:** P4 (Architecture — после блокеров; НЕ блокирует доску)
- **Тип:** ADR-grade (архитектурное решение + миграция)
- **Закрывает:** структурный дубль колонка↔`payload_json` (источник «путаницы» из интервью)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Решения интервью:** [`interview-issues-read-contract-2026-06-19.md`](./interview-issues-read-contract-2026-06-19.md) — D-RC-5
- **Зависит от:** [GW-RC-01](./STORY-GW-RC-01-read-path-column-merge.md), [GW-RC-02](./STORY-GW-RC-02-type-canonical-on-read.md), [GW-RC-03](./STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)

## Зачем простыми словами
Сейчас одни и те же поля (`id/status/created_at`) хранятся дважды — как колонки и внутри `payload_json`. Это источник рассинхрона и путаницы (что считать правдой). Цель — перевести проекцию на колоночную модель и убрать дублирующий JSON-документ, чтобы у каждого факта было одно место.

## Что наблюдаю сейчас (verified по коду)
- `save_projection` пишет и колонки (`issue_id,status,created_at,updated_at,policy_version`), и `payload_json` (= `to_public_dict()`, дубль) ([`db_supabase.py:617`](../../../../src/core/infrastructure/db_supabase.py#L617)).
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

## Подзадачи (черновик)
- **T01** — ADR: финальная схема колонок (scalars + jsonb vs explode i18n); судьба вьюхи.
- **T02** — Миграция схемы `doge_issues`: новые колонки/jsonb.
- **T03** — Write-path: `save_projection` пишет в колонки, без `payload_json`.
- **T04** — Read-path + `read_filters`: сборка и фильтры по колонкам/jsonb.
- **T05** — 3 бэкенда (Supabase/SQLite/InMemory) согласованы.
- **T06** — Вьюха `spa_issues_dashboard_view` переписана.
- **T07** — Data-миграция payload_json → колонки; затем DROP `payload_json`.
- **T08** — Тесты (контракт неизменен) + бэкфилл-скрипт.

## Acceptance Criteria
- [ ] ADR зафиксировал представление i18n/geo (jsonb vs explode) и судьбу вьюхи.
- [ ] Внешняя форма ответа issue идентична до/после (контракт-тесты зелёные).
- [ ] `payload_json` удалён; данные перенесены без потерь.
- [ ] Фильтры/сортировка работают по колонкам/jsonb; 3 бэкенда согласованы.
- [ ] Тест-суит без регрессий.

## Открытые вопросы
- i18n: `jsonb`-колонки `title/summary/description/institution` vs explode `_et/_ru/_en`?
- `geo`: jsonb vs набор admin-колонок (часть уже есть в `ProjectionInput`)?
- `spa_issues_dashboard_view` — нужна ли вообще после колоночной модели?
