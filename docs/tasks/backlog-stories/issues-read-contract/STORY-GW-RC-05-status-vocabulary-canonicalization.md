# STORY-GW-RC-05 — Канонизация status (write board-vocab + read-канонизация + контракт-тест)

## Meta
- **Key:** `STORY-GW-RC-05`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000034](../../gateway-active-packages/pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml), T01–T05, gate PASS 2026-06-20, 522 unit + integration green, reopened GAP-2 закрыт). Код-аудит [`audit-gw-rc-05-...`](../../../analysis/audit-gw-rc-05-status-vocabulary-canonicalization-2026-06-20.md) (verified; write-fix все 3 callers, read-canon вывод+фильтр, контракт-тест на реальном create→extend). **Бонус:** read-canon мапит `promoted`→PUBLISHED на чтении → доска работает на live-данных без миграции; GW-RC-06 понижен до гигиены. SSOT исполнения — pipeline-копия.
- **Приоритет:** P1 (Blocker — доска пустая, reopened GAP-2)
- **Тип:** implement
- **Закрывает:** reopened GAP-2 (status = невалидное `promoted`) на уровне КОДА
- **Основание:** [`CLOSURE`](./CLOSURE-empty-board-status-vocabulary-2026-06-20.md) · [`investigation`](./investigation-empty-board-status-vocabulary-2026-06-20.md) §Recommended fixes 1/2/4 · [`interview`](./interview-rc05-rc06-status-vocabulary-2026-06-20.md) (D-RC05-1/4)
- **Зависит от:** [GW-RC-01](./STORY-GW-RC-01-read-path-column-merge.md) (column-as-truth), [GW-RC-02](./STORY-GW-RC-02-type-canonical-on-read.md) (паттерн канонизации)
- **Парная:** [GW-RC-06](./STORY-GW-RC-06-hosted-status-data-hygiene.md) (данные hosted)

## Зачем простыми словами
Доска раскладывает карточки только по `NEW/IN_REVIEW/PUBLISHED`, а API отдаёт `promoted` — значение из **другого** enum (промоушн-пайплайн). Карточки не попадают ни в одну колонку → доска пустая. Надо: (1) перестать писать candidate-статус в проекцию; (2) на чтении страховать legacy `promoted`→`PUBLISHED`; (3) проверять контракт на **реальных** данных пайплайна, а не на «удобных» seed.

## Что наблюдаю сейчас (verified по коду)
- **Два enum:** `DOGEIssueStatus` = NEW/IN_REVIEW/PUBLISHED ([enums.py:6-11](../../../../src/core/projection/enums.py#L6-L11)); `IssueCandidateStatus` = …/`promoted`/… ([promotion/types.py:8-13](../../../../src/core/promotion/types.py#L8-L13)).
- **Write:** create-path корректен ([issue_create.py:252](../../../../src/core/application/issue_create.py#L252) — projection-status); **extend-path баг** ([:334](../../../../src/core/application/issue_create.py#L334) `updated.status.value`=`promoted`). Extend вызывается cron'ом при росте кластера → статус «уезжает» в `promoted`.
- **Read:** `out["status"]=row_status` без канонизации ([read_filters.py:234](../../../../src/core/projection/read_filters.py#L234)); фильтр статуса по `row_status` ([:271](../../../../src/core/projection/read_filters.py#L271)). (Для `type` канонизация ЕСТЬ — [:236](../../../../src/core/projection/read_filters.py#L236) — паттерн для копирования.)
- **Тесты фиксируют баг:** `test_spa_projection_supabase_roundtrip.py:29,53` (projection seed/assert `promoted`); `test_supabase_live_full_pipeline_roundtrip.py:155` (projection assert `promoted`). ⚠️ `:133` того же файла — `candidate_rows` (issue_candidates), `promoted` там **корректен**, не трогать.

## Требование / целевое состояние
- `doge_issues.status` (и API) — всегда из `DOGEIssueStatus` (board-vocab). Источник — projection-status, не candidate.
- **Write:** все save_projection-пути пишут projection board-status (как create-path), не `*.status.value` кандидата.
- **Read (defense-in-depth):** `canonicalize_status_on_read` (`promoted`→`PUBLISHED` как documented alias; неизвестное → дефолт + лог, по образцу `canonicalize_issue_type_on_read`); применять в выводе и в фильтре статуса.
- **Тесты:** обновить projection-asserts (`promoted`→`PUBLISHED`), НЕ трогая candidate-asserts; добавить контракт-тест на **реальном** пайплайне (create→extend) с проверкой `status ∈ {NEW,IN_REVIEW,PUBLISHED}`.

## Подзадачи (черновик)
- **T01** — Write-fix: extend-path (+ ревизия всех save_projection вызовов) использует projection board-status.
- **T02** — `canonicalize_status_on_read` в `read_filters` (alias `promoted`→`PUBLISHED`, unknown→default+log); применить в merge-выводе и фильтре статуса.
- **T03** — Обновить тесты, фиксирующие projection `promoted`→`PUBLISHED` (roundtrip :29/53, live :155); НЕ трогать candidate-assert (:133).
- **T04** — Контракт-тест на реальном выводе пайплайна: прогнать create→extend, assert `status ∈ board`; и тест канонизации legacy `promoted`→`PUBLISHED`.
- **T05** — story acceptance gate.

## Acceptance Criteria
- [ ] После write-fix реальный create→extend кладёт в `doge_issues.status` board-vocab (PUBLISHED), не `promoted`.
- [ ] `GET /tallinn/issues` отдаёт `status ∈ {NEW,IN_REVIEW,PUBLISHED}` даже для legacy `promoted` (read-канонизация).
- [ ] Контракт-тест гоняет **реальный** пайплайн (не happy-seed) и ловит невалидный status.
- [ ] Тесты, фиксировавшие projection `promoted`, обновлены; candidate-asserts не затронуты.
- [ ] Тест-суит без регрессий.

## Открытые вопросы
- Неизвестный status (не board, не `promoted`) — дефолт `PUBLISHED`? `NEW`? оставить+лог? (mirror решения RC-02 по type).
