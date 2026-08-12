# Интервью PM/CTO — восстановление read-контракта issue (пустой дашборд GFL-DRIVEN)

**Дата:** 2026-06-19
**Роль интервьюируемого:** CPO + CTO.
**Метод:** `.cursor/rules/analysis.mdc` — решения зафиксированы поверх verified-фактов кода.
**Стартовый документ (источник):** [`spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md).
**Пакет стори (итог):** [`docs/tasks/backlog-stories/issues-read-contract/`](./INDEX.md).

---

## 1. Verified-факты (перепроверено по коду перед интервью)

- **Read-path теряет колонки.** `filter_projection_rows` получает кортеж `(_row_status, payload, created_at)`, но возвращает только `dict(payload)` — колонки `issue_id`/`status`/`created_at` отбрасываются; фильтр статуса идёт по `payload.get("status")`, не по колонке. → [`read_filters.py:209-235`](../../../../src/core/projection/read_filters.py#L209-L235).
- **`list_projections`** селектит `status,payload_json,created_at` (без `issue_id`). **`get_projection`** селектит **только `payload_json`**. → [`db_supabase.py:617-715`](../../../../src/core/infrastructure/db_supabase.py#L617-L715).
- **Запись дублирует поля.** `save_projection` пишет строку `doge_issues` с колонками `issue_id,status,created_at,updated_at,policy_version` **и** `payload_json` (это `to_public_dict()`, где те же `id/status/created_at` лежат повторно). → [`db_supabase.py:617`](../../../../src/core/infrastructure/db_supabase.py#L617), [`dto.py:25-50`](../../../../src/core/projection/dto.py#L25-L50).
- **`type` канон — uppercase.** `DOGEIssueType.IMPROVEMENT = "IMPROVEMENT"` ([`enums.py:17`](../../../../src/core/projection/enums.py#L17)). Live-значение `"improvement"` (lowercase) — **legacy-данные**, не текущий код.
- **payload_json — широкий blast radius:** используется в 10 файлах — `db_supabase.py`, `db_sqlite.py`, `repositories.py`, `read_filters.py`, `000_full_init.sql`, init-миграция, **вьюха `spa_issues_dashboard_view`**, 2 теста, `reproject_issue_i18n.py`. Вложенные поля (i18n-карты, `geo`, массивы `labels/original_locale`) не сводятся к плоским колонкам без jsonb.
- **Невалидный ответ не падает.** `GatewayIssueRepository.getIssues` отдаёт `data.issues` без `assertIssue` → отсутствие `status` тихо даёт пустую доску, без ошибки (это и скрывало баг).

**Двухслойная корневая причина:** (1) код read-path выкидывает колонки; (2) 5 live-записей имеют неполный `payload_json` (нет id/status, type lowercase).

---

## 2. Решения интервью (D-RC)

### D-RC-1 — Scope: полный контракт, но фазами
Чиним read-path так, чтобы вернуть **все** поля контракта, но стори разбиты по приоритету: сначала блокеры (доска оживает), затем тип/легаси, затем гарантия контракта, затем архитектурная миграция. → стори RC-01…RC-04.

### D-RC-2 — Источник истины = КОЛОНКА (override)
При расхождении колонка↔JSON в ответе берём `id/status/created_at` **из колонок**, перетирая значение в payload; фильтр статуса — по колонке `row_status`.
**Почему:** колонки — то, по чему БД фильтрует/сортирует/делает upsert, и будущий `PATCH status` будет менять именно колонку. Column-as-truth исключает рассинхрон-баги. → RC-01.

### D-RC-3 — Legacy-данные: read-path устойчив, данные чинить опционально
Read-path сам достраивает контракт из колонок и нормализует `type` на чтении, поэтому доска работает **сразу на текущих 5 записях без миграции БД**. Бэкфилл/аудит legacy — отдельная необязательная гигиена. → RC-01 (устойчивость) + RC-03 (опц. данные).

### D-RC-4 — Защита от рецидива: контракт-тест + гарантия формы
Отдельная задача: регресс-тест «seed неполного payload → GET возвращает `id/status/type` в каноне» (зеркалит существующий `test_req24`). Гарантируем форму ответа на уровне бэка, чтобы фронт мог доверять. → RC-03.

### D-RC-5 — Архитектура: полная колоночная миграция (удаление `payload_json`) — стори В ЭТОМ пакете
После блокер-стори: перевести **все** поля в колонки (скаляры + `jsonb` для i18n/geo/labels — полностью «без JSON» невозможно), переписать write/read/фильтры/вьюху/3 бэкенда, удалить `payload_json`.
**Зафиксированное ограничение:** «только колонки» недостижимо для вложенных структур — это будет «скаляры + jsonb», т.е. дубль уходит, но JSON частично остаётся как jsonb. Идёт ПОСЛЕ RC-01..03 (не блокирует доску тяжёлой перестройкой). → RC-04 (ADR-grade).

---

## 3. Карта решений → стори

| Решение | Стори | Приоритет |
|---|---|---|
| D-RC-1, D-RC-2, D-RC-3 (read-path колонки, column-as-truth, устойчивость) | [RC-01](./STORY-GW-RC-01-read-path-column-merge.md) | P1 Blocker |
| D-RC-1, D-RC-3 (type канон на чтении + legacy `type`) | [RC-02](./STORY-GW-RC-02-type-canonical-on-read.md) | P2 High |
| D-RC-4 (контракт-тест/гарантия) + остаточные legacy-поля (institution/geo/original_locale/provenance — data-only) | [RC-03](./STORY-GW-RC-03-contract-guarantee-and-legacy-data.md) | P3 Medium |
| D-RC-5 (колоночная модель, drop payload_json) | [RC-04](./STORY-GW-RC-04-columnar-model-migration.md) | P4 Architecture |

---

## 4. Открытые вопросы, оставленные стори-уровню
- RC-03: для legacy-полей `geo/institution/original_locale/provenance` — это **data-only** (read-path их уже отдаёт из payload). Решить, нужен ли реальный бэкфилл сейчас или достаточно зафиксировать как «появятся при ре-проджектинге».
- RC-04: финальный выбор представления i18n/geo — `jsonb`-колонки vs explode на `_et/_ru/_en`; и судьба вьюхи `spa_issues_dashboard_view`.
