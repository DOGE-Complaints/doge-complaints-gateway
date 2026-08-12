# STORY-GW-RC-05 — Канонизация status (write board-vocab + read-канонизация + контракт-тест)

## Meta
- **Key:** `STORY-GW-RC-05`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 (Blocker — доска пустая, reopened GAP-2)
- **Тип:** implement
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-05-status-vocabulary-canonicalization.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Закрывает:** reopened GAP-2 (status = невалидное `promoted`) на уровне КОДА
- **Основание:** [`CLOSURE`](../../../../backlog-stories/issues-read-contract/CLOSURE-empty-board-status-vocabulary-2026-06-20.md) · [`investigation`](../../../../backlog-stories/issues-read-contract/investigation-empty-board-status-vocabulary-2026-06-20.md) §Recommended fixes 1/2/4 · [`interview`](../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) (D-RC05-1/4)
- **Decision Ref:** backlog file above; [`interview-rc05-rc06-status-vocabulary-2026-06-20.md`](../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) — D-RC05-1/4
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml`](../../../../gateway-active-packages/pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05
- **Зависит от:** [GW-RC-01](../STORY-GW-RC-01-read-path-column-merge/STORY-GW-RC-01-read-path-column-merge.md) (column-as-truth), [GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read/STORY-GW-RC-02-type-canonical-on-read.md) (паттерн канонизации)
- **Парная:** [GW-RC-06](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-06-hosted-status-data-hygiene.md) (данные hosted)

## Зачем простыми словами
Доска раскладывает карточки только по `NEW/IN_REVIEW/PUBLISHED`, а API отдаёт `promoted` — значение из **другого** enum (промоушн-пайплайн). Карточки не попадают ни в одну колонку → доска пустая. Надо: (1) перестать писать candidate-статус в проекцию; (2) на чтении страховать legacy `promoted`→`PUBLISHED`; (3) проверять контракт на **реальных** данных пайплайна, а не на «удобных» seed.

## Что наблюдаю сейчас (verified по коду)
- **Два enum:** `DOGEIssueStatus` = NEW/IN_REVIEW/PUBLISHED ([enums.py:6-11](../../../../../../../src/core/projection/enums.py#L6-L11)); `IssueCandidateStatus` = …/`promoted`/… ([promotion/types.py:8-13](../../../../../../../src/core/promotion/types.py#L8-L13)).
- **Write:** create-path корректен ([issue_create.py:252](../../../../../../../src/core/application/issue_create.py#L252) — projection-status); **extend-path баг** ([:334](../../../../../../../src/core/application/issue_create.py#L334) `updated.status.value`=`promoted`). Extend вызывается cron'ом при росте кластера → статус «уезжает» в `promoted`.
- **Read:** `out["status"]=row_status` без канонизации ([read_filters.py:234](../../../../../../../src/core/projection/read_filters.py#L234)); фильтр статуса по `row_status` ([:271](../../../../../../../src/core/projection/read_filters.py#L271)). (Для `type` канонизация ЕСТЬ — [:236](../../../../../../../src/core/projection/read_filters.py#L236) — паттерн для копирования.)
- **Тесты фиксируют баг:** `test_spa_projection_supabase_roundtrip.py:29,53` (projection seed/assert `promoted`); `test_supabase_live_full_pipeline_roundtrip.py:155` (projection assert `promoted`). ⚠️ `:133` того же файла — `candidate_rows` (issue_candidates), `promoted` там **корректен**, не трогать.

## Требование / целевое состояние
- `doge_issues.status` (и API) — всегда из `DOGEIssueStatus` (board-vocab). Источник — projection-status, не candidate.
- **Write:** все save_projection-пути пишут projection board-status (как create-path), не `*.status.value` кандидата.
- **Read (defense-in-depth):** `canonicalize_status_on_read` (`promoted`→`PUBLISHED` как documented alias; неизвестное → дефолт + лог, по образцу `canonicalize_issue_type_on_read`); применять в выводе и в фильтре статуса.
- **Тесты:** обновить projection-asserts (`promoted`→`PUBLISHED`), НЕ трогая candidate-asserts; добавить контракт-тест на **реальном** пайплайне (create→extend) с проверкой `status ∈ {NEW,IN_REVIEW,PUBLISHED}`.

## Out of scope
- Hosted SQL `UPDATE doge_issues` и S1 пустой контент — [GW-RC-06](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-06-hosted-status-data-hygiene.md) (данные hosted)
- Изменение SPA / BoardPage кода
- FE-side contract tests (gateway guarantees storage + API shape only)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-05-t01-write-fix-extend-path-projection-board-status`](./task-gw-rc-05-t01-write-fix-extend-path-projection-board-status/README.md) | pkg-000034 |
| 2 | [`task-gw-rc-05-t02-canonicalize-status-on-read`](./task-gw-rc-05-t02-canonicalize-status-on-read/README.md) | pkg-000034 |
| 3 | [`task-gw-rc-05-t03-update-projection-tests-promoted-to-published`](./task-gw-rc-05-t03-update-projection-tests-promoted-to-published/README.md) | pkg-000034 |
| 4 | [`task-gw-rc-05-t04-real-pipeline-contract-test-status-vocab`](./task-gw-rc-05-t04-real-pipeline-contract-test-status-vocab/README.md) | pkg-000034 |
| 5 | [`task-gw-rc-05-t05-story-acceptance-gate`](./task-gw-rc-05-t05-story-acceptance-gate/README.md) | pkg-000034 |

## Audit gap map (post-audit 2026-06-20)

| Gap | Disposition | Status |
|-----|-------------|--------|
| G1 RC-06 hygiene | defer to GW-RC-06 backlog | N/A (cross-story) |
| G2 unknown→PUBLISHED | accepted fail-open | Closed (by design) |

## Acceptance Criteria
- [x] После write-fix реальный create→extend кладёт в `doge_issues.status` board-vocab (PUBLISHED), не `promoted`.
- [x] `GET /tallinn/issues` отдаёт `status ∈ {NEW,IN_REVIEW,PUBLISHED}` даже для legacy `promoted` (read-канонизация).
- [x] Контракт-тест гоняет **реальный** пайплайн (не happy-seed) и ловит невалидный status.
- [x] Тесты, фиксировавшие projection `promoted`, обновлены; candidate-asserts не затронуты.
- [x] Тест-суит без регрессий.

## Открытые вопросы
- ~~Неизвестный status (не board, не `promoted`)~~ — resolved P3: default `PUBLISHED` + `record_unknown_issue_status` ([`read_status_telemetry.py`](../../../../../../../src/core/projection/read_status_telemetry.py)).
