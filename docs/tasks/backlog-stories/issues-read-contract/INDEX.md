# Issues read-contract restoration — backend story package · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/issues-read-contract/`
**Тип:** backlog (продуктовая проработка; не активный build-пакет).
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — все факты по фактическому коду, пути указаны.

## ✅ ИТОГ ПАКЕТА RC-01→06 (2026-06-21) + reopen RC-07 (2026-06-22)
RC-01..07 реализованы и verified. **CF-B (2026-06-22 → operationally closed 2026-07-10):** hosted board restored (9 cards); **исходная причина undetermined** (prod self-resolved — audit §G1/T06, «deploy drift/`columnar_storage`» ретрагирован как мисатрибуция); [`STORY-GW-RC-07`](./STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) gate PASS pkg-000047; unblocks SEED-03 hosted.

- **CF-B audit:** [`audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md`](../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §3
- **SSOT исполнения:** [`bullrun-launch-index.md`](../bullrun-launch-index.md) §GW-RC-07; active [`pkg-000047`](../gateway-active-packages/pkg-000047-20260710-gw-rc-07-hosted-tallinn-issues-internal-error.yaml)

## Связи (traceability)
- **Стартовый документ (баг-репорт фронта, Jun-19):** [`spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md) — пустой дашборд при GFL-DRIVEN, 8 field-gaps. (Остаётся в FE-зоне как FE-origin; co-located разбор — в CLOSURE/investigation выше.)
- **Интервью PM/CTO (решения D-RC):** [`interview-issues-read-contract-2026-06-19.md`](./interview-issues-read-contract-2026-06-19.md).

## Контекст одной фразой
`GET /tallinn/issues` отдаёт issue **без `id`/`status`** → фронт не может разложить карточки по колонкам → пустая доска. Корень: read-path возвращает только `payload_json` и выкидывает колонки `issue_id/status/created_at`; плюс 5 live-записей имеют неполный payload (нет id/status, `type` lowercase).

## Коды статусов (S)
⚪ Todo · 🟡 In Progress · 🔵 Implemented (Waiting Acceptance) · 🟢 Done (Committed)

## Стори пакета

| S | Key | Story | Приоритет | Закрывает (gap отчёта) | Зависит от |
|---|-----|-------|-----------|------------------------|------------|
| 🔵 | GW-RC-01 | [Read-path: merge колонок id/status/created_at (column-as-truth)](./STORY-GW-RC-01-read-path-column-merge.md) | P1 Blocker | GAP-1, GAP-2, GAP-4 | — | Done |
| 🔵 | GW-RC-02 | [Канонизация `type` на чтении + legacy type](./STORY-GW-RC-02-type-canonical-on-read.md) | P2 High | GAP-3 | GW-RC-01 | Done |
| 🔵 | GW-RC-03 | [Гарантия контракта (тест) + гигиена legacy-данных](./STORY-GW-RC-03-contract-guarantee-and-legacy-data.md) | P3 Medium | GAP-5/6/7/8 + защита | GW-RC-01, GW-RC-02 | Done |
| 🔵 | GW-RC-04 | [Колоночная модель проекции (удаление payload_json)](./STORY-GW-RC-04-columnar-model-migration.md) | P4 Architecture | дубль колонка↔JSON | GW-RC-01..03 | Done |
| 🔵 | GW-RC-05 | [Канонизация status (write board-vocab + read-канон + контракт-тест)](./STORY-GW-RC-05-status-vocabulary-canonicalization.md) | P1 Blocker | **reopened GAP-2** (код) | GW-RC-01, GW-RC-02 | Done |
| 🔵 | GW-RC-06 | [Гигиена hosted-данных: status-миграция + пустой контент S1](./STORY-GW-RC-06-hosted-status-data-hygiene.md) | P2 | reopened GAP-2 (данные) + S1 | GW-RC-05 | Done |
| 🔵 | GW-RC-07 | [Hosted `/tallinn/issues` INTERNAL_ERROR (CF-B)](./STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) → [pipeline](../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) | P1 Blocker | CF-B regression | RC-01..06 | Done (Awaiting Commits) |
| 🔵 | GW-PUBLIC-01 | [Регресс-гарантия публичности issues (M-5)](./STORY-GW-PUBLIC-01-public-issues-regression.md) → [pipeline](../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-PUBLIC-01-public-issues-regression/STORY-GW-PUBLIC-01-public-issues-regression.md) | P2 gate | M-5 read без auth | — | Done (Awaiting Commits) |

> **RC-01→07:** RC-07 gate PASS 2026-07-10 (hosted board restored, 9 cards; June CF-B causa undetermined — audit §G1/T06).

**Progress:** 8/8 Done (100%)

## Решения интервью (D-RC, 2026-06-19) — кратко
- **D-RC-1:** полный контракт, но фазами (RC-01→RC-04).
- **D-RC-2:** источник истины — **колонка** (override JSON); фильтр статуса по колонке.
- **D-RC-3:** read-path устойчив к неполному payload → доска работает без миграции данных; бэкфилл опционален.
- **D-RC-4:** контракт-тест + гарантия формы ответа.
- **D-RC-5:** полная колоночная миграция (drop `payload_json`) — стори RC-04 в этом пакете, после блокеров; «только колонки» недостижимо для i18n/geo → скаляры + `jsonb`.

## Ключевой verified-факт пакета
Проекция хранит `id/status/created_at` **дважды**: как колонки `doge_issues` (по ним БД фильтрует/сортирует/upsert) и внутри `payload_json` (`to_public_dict()`). Read-path сейчас отдаёт только JSON и игнорирует колонки ([`read_filters.py:234`](../../../../src/core/projection/read_filters.py#L234), [`db_supabase.py:617-715`](../../../../src/core/infrastructure/db_supabase.py#L617-L715)). `payload_json` используется в 10 файлах + вьюхе `spa_issues_dashboard_view`.
