# STORY-GW-RC-03 — Гарантия контракта (тест) + гигиена legacy-данных

## Meta
- **Key:** `STORY-GW-RC-03`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P3 (Medium)
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-03-contract-guarantee-and-legacy-data.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Закрывает:** GAP-5 (`institution`), GAP-6 (`geo`), GAP-7 (`original_locale`), GAP-8 (provenance txids) + защита от рецидива
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Decision Ref:** backlog file above; [`interview-issues-read-contract-2026-06-19.md`](../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) — D-RC-4, D-RC-3
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000032-20260529-gw-rc-03-contract-guarantee-and-legacy-data.yaml`](../../../../gateway-active-packages/pkg-000032-20260529-gw-rc-03-contract-guarantee-and-legacy-data.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05
- **Зависит от:** [GW-RC-01](../STORY-GW-RC-01-read-path-column-merge/STORY-GW-RC-01-read-path-column-merge.md), [GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read/STORY-GW-RC-02-type-canonical-on-read.md)
- **Разблокирует:** GW-RC-04 (backlog package)

## Зачем простыми словами
Две задачи. (1) **Защита от рецидива:** сейчас невалидный ответ бэка тихо приводит к пустой доске, без ошибки — это скрыло баг надолго. Нужен тест, который гарантирует форму ответа на стороне бэка. (2) **Остаточные поля:** `institution/geo/original_locale/провенанс-хэши` нужны для фильтров и деталей; для новых issue они уже едут, но у старых записей их нет — решить, чинить ли данные.

## Что наблюдаю сейчас (verified по коду)
- Поля `institution/geo/original_locale/arweave_txid/image_txid/image_hash` формируются в `to_public_dict()` ([`dto.py:37-50`](../../../../../../../src/core/projection/dto.py#L37-L50)) и **read-path их уже возвращает** (он отдаёт payload). То есть для НОВЫХ issue они присутствуют — это **data-only gap** (legacy payload их не содержит), не дефект read-path.
- Контракт ответа на бэке **не гарантируется тестом для неполного payload** — существующий `test_req24` проверяет полный intake-путь, но не «кривой» payload.
- Фронт не прогоняет `assertIssue` на gateway-пути → невалидный ответ = тихая пустая доска ([отчёт §«контракт не энфорсится»]).

## Требование / целевое состояние (D-RC-4, D-RC-3)
1. **Контракт-гарантия (тест):** регресс-тест «seed строки `issue_id`+`status` + payload **без** id/status и со строчным type → `GET` list/get возвращает `id`, `status ∈ {…}`, `type` в каноне». Зеркалит [`test_req24_tallinn_issues_read_api.py:160`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py#L160).
2. **Гигиена legacy-данных (опционально):** аудит 5 записей; решить — оставить (поля появятся при следующем ре-проджектинге) или прогнать бэкфилл сейчас. `institution/geo/original_locale/provenance` доезжают из payload, поэтому это «появятся при ре-проджектинге», не блокер.

## Граница и контракт
- Гарантируем форму ответа на бэке; FE-side `assertIssue` — зона фронта (упомянуть в handoff, не делать здесь).
- Реальная запись недостающих полей в legacy — только если решено в открытом вопросе.

## Product decisions (fixed, P1 materialization)
- **Contract test (D-RC-4):** seed `issue_id`+`status` columns + payload **без** `id`/`status` + lowercase `type` → `GET` list/get возвращает `id`, `status ∈ {…}`, `type` в каноне; зеркалит [`test_req24_tallinn_issues_read_api.py:160`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py#L160) (intake seed pattern, не полный intake path).
- **Legacy fields (D-RC-3):** `institution`/`geo`/`original_locale`/`arweave_txid`/`image_txid`/`image_hash` — **data-only**; read-path уже отдаёт из payload ([`dto.py:37-50`](../../../../../../../src/core/projection/dto.py#L37-L50)).
- **T03 gate:** бэкфилл через re-project — **опционален**; решение фиксируется в T02 audit artifact; default defer = «появятся при ре-проджектинге» (interview §4).

## Out of scope
- FE-side `assertIssue` / SPA contract tests (handoff only in T04)
- Удаление `payload_json` / колоночная миграция (GW-RC-04)
- Runtime code changes beyond tests (T01) and optional data backfill (T03)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-03-t01-contract-regression-test-incomplete-payload`](./task-gw-rc-03-t01-contract-regression-test-incomplete-payload/README.md) | pkg-000032 |
| 2 | [`task-gw-rc-03-t02-legacy-sql-audit-five-live-records`](./task-gw-rc-03-t02-legacy-sql-audit-five-live-records/README.md) | pkg-000032 |
| 3 | [`task-gw-rc-03-t03-optional-legacy-backfill-reproject`](./task-gw-rc-03-t03-optional-legacy-backfill-reproject/README.md) | pkg-000032 (gated) |
| 4 | [`task-gw-rc-03-t04-backend-handoff-fe-contract-guarantee`](./task-gw-rc-03-t04-backend-handoff-fe-contract-guarantee/README.md) | pkg-000032 |
| 5 | [`task-gw-rc-03-t05-story-acceptance-gate`](./task-gw-rc-03-t05-story-acceptance-gate/README.md) | pkg-000032 |
| 6 | [`task-gw-rc-03-t06-tighten-valid-statuses-to-governed-enum`](./task-gw-rc-03-t06-tighten-valid-statuses-to-governed-enum/README.md) | audit override (`run_mode=gw_rc_03_audit_followup`) |

## Audit gap map (post-audit 2026-06-19)

| Gap | Task | Status |
|-----|------|--------|
| G1 status-set strictness | T06 | Done |
| G2 legacy data defer | — | accepted (T02) |

## Acceptance Criteria
- [x] Регресс-тест: неполный payload → ответ содержит `id`, `status`, канон `type`.
- [x] Проведён аудит legacy-записей; принято и зафиксировано решение по бэкфиллу.
- [x] (Если решено) legacy-issue получили недостающие поля. — **N/A** (T02 defer)
- [x] Тест-суит без регрессий.

## Открытые вопросы
- ~~`geo/institution/original_locale/provenance` для legacy~~ — закрыто T02: decision **defer** (D-RC-3).
