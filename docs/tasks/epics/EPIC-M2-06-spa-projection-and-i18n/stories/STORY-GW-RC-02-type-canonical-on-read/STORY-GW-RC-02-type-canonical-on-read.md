# STORY-GW-RC-02 — Канонизация `type` на чтении + legacy type

## Meta
- **Key:** `STORY-GW-RC-02`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P2 (High — contract violation)
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-02-type-canonical-on-read.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-02-type-canonical-on-read.md)
- **Закрывает:** GAP-3 (`type` в нижнем регистре)
- **Стартовый документ:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- **Decision Ref:** backlog file above; [`interview-issues-read-contract-2026-06-19.md`](../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) — D-RC-1, D-RC-3
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000031-20260529-gw-rc-02-type-canonical-on-read.yaml`](../../../../gateway-active-packages/pkg-000031-20260529-gw-rc-02-type-canonical-on-read.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06; audit follow-up **T07** вне pkg (`run_mode=gw_rc_02_audit_followup`)
- **Зависит от:** [GW-RC-01](../STORY-GW-RC-01-read-path-column-merge/STORY-GW-RC-01-read-path-column-merge.md)
- **Разблокирует:** GW-RC-03 (backlog package)

## Зачем простыми словами
В live-данных `type` приходит строчными (`"improvement"`), а фронт и контракт ждут UPPERCASE (`IMPROVEMENT`). Из-за этого ломается фильтр по типу и локализация типа в деталях issue. Надо, чтобы API всегда отдавал `type` в каноне, даже если в БД лежит старое строчное значение.

## Что наблюдаю сейчас (verified по коду)
- Канон бэка — UPPERCASE: `DOGEIssueType.IMPROVEMENT = "IMPROVEMENT"` ([`enums.py:14-19`](../../../../../../../src/core/projection/enums.py#L14-L19)).
- Текущий код проекции пишет канон (через `to_public_dict`), значит live `"improvement"` — **legacy/incomplete payload**, не баг текущего write-path.
- Read-path возвращает `type` как есть из payload (не нормализует) → старое строчное значение доезжает до фронта ([`merge_projection_columns`](../../../../../../../src/core/projection/read_filters.py#L188-L200) — только `id`/`status`/`created_at`).
- На фронте: `t('issueType.improvement')` промахивается мимо `issueType.IMPROVEMENT`; фильтр Type сравнивает с uppercase-каноном ([отчёт §GAP-3]).
- `?type=` сравнивает сырой payload до merge ([`read_filters.py:161`](../../../../../../../src/core/projection/read_filters.py#L161)).

## Требование / целевое состояние (D-RC-3)
- API всегда отдаёт `type` в каноне `{IMPROVEMENT, SERVICE_REQUEST, INCIDENT}` — нормализация на чтении (`.upper()` или маппинг), чтобы старое строчное значение не утекало.
- Нормализация применяется и в списке, и в одиночном endpoint; во всех бэкендах.
- Неизвестное/пустое значение — зафиксировать поведение (оставить как есть vs дефолт) — см. Product decisions ниже.

## Граница и контракт
- Меняется только представление `type` на чтении; форма/имя поля не меняется.
- Реальная гигиена legacy-данных (перезапись в БД) — опциональна и относится к RC-03; здесь — устойчивость на чтении.

## Product decisions (fixed, P1 materialization)
- **Known legacy:** `improvement` / `service_request` / `incident` (any case) → канон `{IMPROVEMENT, SERVICE_REQUEST, INCIDENT}` via `.strip().upper()` + membership in `DOGEIssueType`.
- **Unknown / not in enum:** ответ API → **`IMPROVEMENT`** (дефолт).
- **Empty / missing `type`:** → **`IMPROVEMENT`** (тот же дефолт; покрыть тестом).
- **Choke-point:** нормализация в `merge_projection_columns` (после RC-01 column merge) — все бэкенды наследуют без отдельных parity-тасков.
- **Anomaly log:** при первом появлении неизвестного raw-значения — append **один раз** в `{LOG_DEBUG_DIR}/unknown_issue_types.jsonl` (`ts`, `raw_type`, `issue_id`, `normalized_to`). Паттерн — `StoryDebugLogger` ([`logging_setup.py:36-74`](../../../../../../../src/core/logging_setup.py#L36-L74)). Без `LOG_DEBUG_DIR` — только дефолт. Railway: ephemeral FS — [`server-env-quickstart.md:82`](../../../../../../../docs/runtime-docs/server-env-quickstart.md).

## Out of scope
- Перезапись legacy-данных в БД (GW-RC-03)
- Удаление `payload_json` / колоночная миграция (GW-RC-04)
- Проверка i18n типа на фронте (FE отдельно; бэк гарантирует канон в ответе)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-02-t01-canonicalize-type-in-merge`](./task-gw-rc-02-t01-canonicalize-type-in-merge/README.md) | pkg-000031 |
| 2 | [`task-gw-rc-02-t02-unknown-type-default-improvement`](./task-gw-rc-02-t02-unknown-type-default-improvement/README.md) | pkg-000031 |
| 3 | [`task-gw-rc-02-t03-unknown-type-anomaly-file-log`](./task-gw-rc-02-t03-unknown-type-anomaly-file-log/README.md) | pkg-000031 |
| 4 | [`task-gw-rc-02-t04-type-filter-canonical-compare`](./task-gw-rc-02-t04-type-filter-canonical-compare/README.md) | pkg-000031 |
| 5 | [`task-gw-rc-02-t05-acceptance-tests-legacy-lowercase-type`](./task-gw-rc-02-t05-acceptance-tests-legacy-lowercase-type/README.md) | pkg-000031 |
| 6 | [`task-gw-rc-02-t06-story-acceptance-gate`](./task-gw-rc-02-t06-story-acceptance-gate/README.md) | pkg-000031 |
| 7 | [`task-gw-rc-02-t07-canonicalize-type-query-param-on-filter`](./task-gw-rc-02-t07-canonicalize-type-query-param-on-filter/README.md) | audit override (`run_mode=gw_rc_02_audit_followup`) |

## Audit gap map (post-audit 2026-06-19)

| Gap | Task | Status |
|-----|------|--------|
| G1 query-type canon | T07 | Done |
| G2 FE i18n | — | backlog/FE |

## Acceptance Criteria
- [x] `GET /tallinn/issues` и `/{id}` отдают `type` в каноне даже для legacy строчного значения.
- [x] Фильтр `?type=` и i18n типа на фронте работают на live-данных (проверяется на стороне FE отдельно; бэк гарантирует канон).
- [x] Поведение для неизвестного `type` определено и покрыто тестом.
- [x] Тест-суит без регрессий.

## Открытые вопросы
- ~~Неизвестный `type` (не из enum)~~ — закрыто P1: дефолт `IMPROVEMENT` + anomaly file log (Product decisions).
