# STORY-GW-RC-03 — Гарантия контракта (тест) + гигиена legacy-данных

## Meta
- **Key:** `STORY-GW-RC-03`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000032](../../gateway-active-packages/pkg-000032-20260529-gw-rc-03-contract-guarantee-and-legacy-data.yaml), T01–T05 gate PASS 2026-05-29; T03 N/A defer; `508 passed` unit, GAP-5/6/7/8 + D-RC-4 closed). Код-аудит [`audit-gw-rc-03-contract-guarantee-legacy-data-2026-06-19.md`](../../../analysis/audit-gw-rc-03-contract-guarantee-legacy-data-2026-06-19.md) (verified; ⚠️ R2: дата приёмки 2026-05-29 раньше зависимостей RC-01/02 2026-06-19 — фабрикация). SSOT исполнения — pipeline-копия.
- **Приоритет:** P3 (Medium)
- **Закрывает:** GAP-5 (`institution`), GAP-6 (`geo`), GAP-7 (`original_locale`), GAP-8 (provenance txids) + защита от рецидива
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Решения интервью:** [`interview-issues-read-contract-2026-06-19.md`](./interview-issues-read-contract-2026-06-19.md) — D-RC-4, D-RC-3
- **Зависит от:** [GW-RC-01](./STORY-GW-RC-01-read-path-column-merge.md), [GW-RC-02](./STORY-GW-RC-02-type-canonical-on-read.md)

## Зачем простыми словами
Две задачи. (1) **Защита от рецидива:** сейчас невалидный ответ бэка тихо приводит к пустой доске, без ошибки — это скрыло баг надолго. Нужен тест, который гарантирует форму ответа на стороне бэка. (2) **Остаточные поля:** `institution/geo/original_locale/провенанс-хэши` нужны для фильтров и деталей; для новых issue они уже едут, но у старых записей их нет — решить, чинить ли данные.

## Что наблюдаю сейчас (verified по коду)
- Поля `institution/geo/original_locale/arweave_txid/image_txid/image_hash` формируются в `to_public_dict()` ([`dto.py:37-50`](../../../../src/core/projection/dto.py#L37-L50)) и **read-path их уже возвращает** (он отдаёт payload). То есть для НОВЫХ issue они присутствуют — это **data-only gap** (legacy payload их не содержит), не дефект read-path.
- Контракт ответа на бэке **не гарантируется тестом для неполного payload** — существующий `test_req24` проверяет полный intake-путь, но не «кривой» payload.
- Фронт не прогоняет `assertIssue` на gateway-пути → невалидный ответ = тихая пустая доска ([отчёт §«контракт не энфорсится»]).

## Требование / целевое состояние (D-RC-4, D-RC-3)
1. **Контракт-гарантия (тест):** регресс-тест «seed строки `issue_id`+`status` + payload **без** id/status и со строчным type → `GET` list/get возвращает `id`, `status ∈ {…}`, `type` в каноне». Зеркалит [`test_req24_tallinn_issues_read_api.py:160`](../../../../tests/test_req24_tallinn_issues_read_api.py#L160).
2. **Гигиена legacy-данных (опционально):** аудит 5 записей; решить — оставить (поля появятся при следующем ре-проджектинге) или прогнать бэкфилл сейчас. `institution/geo/original_locale/provenance` доезжают из payload, поэтому это «появятся при ре-проджектинге», не блокер.

## Граница и контракт
- Гарантируем форму ответа на бэке; FE-side `assertIssue` — зона фронта (упомянуть в handoff, не делать здесь).
- Реальная запись недостающих полей в legacy — только если решено в открытом вопросе.

## Подзадачи (черновик)
- **T01** — Контракт-тест неполного payload → валидный ответ (list + get; все бэкенды).
- **T02** — SQL-аудит 5 live-записей (наличие id/status/type/institution/geo/original_locale/txids в payload).
- **T03** — (Опционально, по решению) бэкфилл legacy через ре-проджектинг.
- **T04** — Backend handoff: зафиксировать для фронта, что форма ответа гарантирована; FE может включить `assertIssue`/контракт-тест.

## Acceptance Criteria
- [ ] Регресс-тест: неполный payload → ответ содержит `id`, `status`, канон `type`.
- [ ] Проведён аудит legacy-записей; принято и зафиксировано решение по бэкфиллу.
- [ ] (Если решено) legacy-issue получили недостающие поля.
- [ ] Тест-суит без регрессий.

## Открытые вопросы
- `geo/institution/original_locale/provenance` для legacy — бэкфиллить сейчас или принять «появятся при ре-проджектинге»?
