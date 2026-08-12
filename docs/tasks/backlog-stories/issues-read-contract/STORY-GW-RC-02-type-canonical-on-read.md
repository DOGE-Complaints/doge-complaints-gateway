# STORY-GW-RC-02 — Канонизация `type` на чтении + legacy type

## Meta
- **Key:** `STORY-GW-RC-02`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000031](../../gateway-active-packages/pkg-000031-20260529-gw-rc-02-type-canonical-on-read.yaml), T01–T06, gate PASS 2026-06-19; audit T07 Done 2026-05-29, G1 closed, 505 unit, GAP-3 closed); код-аудит [`audit-gw-rc-02-type-canonical-on-read-2026-06-19.md`](../../../analysis/audit-gw-rc-02-type-canonical-on-read-2026-06-19.md) (G1 closed). SSOT исполнения — pipeline-копия. Раздел «Что наблюдаю сейчас» ниже — до-реализационное состояние.
- **Приоритет:** P2 (High — contract violation)
- **Закрывает:** GAP-3 (`type` в нижнем регистре)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Решения интервью:** [`interview-issues-read-contract-2026-06-19.md`](./interview-issues-read-contract-2026-06-19.md) — D-RC-1, D-RC-3
- **Зависит от:** [GW-RC-01](./STORY-GW-RC-01-read-path-column-merge.md)

## Зачем простыми словами
В live-данных `type` приходит строчными (`"improvement"`), а фронт и контракт ждут UPPERCASE (`IMPROVEMENT`). Из-за этого ломается фильтр по типу и локализация типа в деталях issue. Надо, чтобы API всегда отдавал `type` в каноне, даже если в БД лежит старое строчное значение.

## Что наблюдаю сейчас (verified по коду)
- Канон бэка — UPPERCASE: `DOGEIssueType.IMPROVEMENT = "IMPROVEMENT"` ([`enums.py:14-19`](../../../../src/core/projection/enums.py#L14-L19)).
- Текущий код проекции пишет канон (через `to_public_dict`), значит live `"improvement"` — **legacy/incomplete payload**, не баг текущего write-path.
- Read-path возвращает `type` как есть из payload (не нормализует) → старое строчное значение доезжает до фронта.
- На фронте: `t('issueType.improvement')` промахивается мимо `issueType.IMPROVEMENT`; фильтр Type сравнивает с uppercase-каноном ([отчёт §GAP-3]).

## Требование / целевое состояние (D-RC-3)
- API всегда отдаёт `type` в каноне `{IMPROVEMENT, SERVICE_REQUEST, INCIDENT}` — нормализация на чтении (`.upper()` или маппинг), чтобы старое строчное значение не утекало.
- Нормализация применяется и в списке, и в одиночном endpoint; во всех бэкендах.
- Неизвестное/пустое значение — зафиксировать поведение (оставить как есть vs дефолт) — см. открытый вопрос.

## Граница и контракт
- Меняется только представление `type` на чтении; форма/имя поля не меняется.
- Реальная гигиена legacy-данных (перезапись в БД) — опциональна и относится к RC-03; здесь — устойчивость на чтении.

## Подзадачи (черновик)
- **T01** — В сборке ответа read-path нормализовать `type` к канону (после merge из RC-01).
- **T02** — Решить кейс неизвестного `type` (не в enum): оставить/дефолт/лог.
- **T03** — Acceptance-тесты: seed payload с `type:"improvement"` → ответ `IMPROVEMENT`; список и одиночный; все бэкенды.

## Acceptance Criteria
- [ ] `GET /tallinn/issues` и `/{id}` отдают `type` в каноне даже для legacy строчного значения.
- [ ] Фильтр `?type=` и i18n типа на фронте работают на live-данных (проверяется на стороне FE отдельно; бэк гарантирует канон).
- [ ] Поведение для неизвестного `type` определено и покрыто тестом.
- [ ] Тест-суит без регрессий.

## Открытые вопросы
- Неизвестный `type` (не из enum) — отдавать как есть, маппить в дефолт, или логировать как аномалию?
