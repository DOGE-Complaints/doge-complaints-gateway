# STORY-GW-SEED-02 — Расширение датасета для кластеризации (≥8 на кластер)

## Meta
- **Key:** `STORY-GW-SEED-02`
- **Parent Epic:** [`../../../EPIC-M2-19-demo-data-seeding.md`](../../../EPIC-M2-19-demo-data-seeding.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Закрывает:** D-SEED-2 (объём для срабатывания кластеризации)
- **source:** [`../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-02-dataset-expansion-for-clustering.md`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Стартовый документ:** [`tests/sandbox/dogestonia_simulation_canvas_v0_1.json`](../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json); [интервью](../../../../../analysis/interview-seed-demo-data-2026-06-20.md)
- **Зависит от:** —
- **Decision Ref:** backlog file above; [`interview-seed-demo-data-2026-06-20.md`](../../../../../analysis/interview-seed-demo-data-2026-06-20.md) — D-SEED-2; [`analysis-clustering-seed-data-investigation-2026-06-22.md`](../../../../../analysis/analysis-clustering-seed-data-investigation-2026-06-22.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000037-20260622-gw-seed-02-dataset-expansion-for-clustering.yaml`](../../../../gateway-active-packages/pkg-000037-20260622-gw-seed-02-dataset-expansion-for-clustering.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05

## Зачем простыми словами
Чтобы на доске появились карточки, система должна собрать **минимум 8 похожих историй** в один кластер (`CLUSTER_MIN_SIZE=8`). Текущие 130 историй размазаны по разным меткам — не факт, что хоть один кластер наберёт 8. Нужно добавить историй так, чтобы по ключевым темам набиралось ≥8, и доска реально наполнилась.

## Что наблюдаю сейчас (verified)
- Кластеризация группирует по `canonical_labels` через lens (`cluster_key_for_lens`, [engine.py:70-85](../../../../../../src/core/cluster/engine.py#L70-L85)), а НЕ по `cluster_metadata.primary_cluster_key` из canvas.
- Порог: `CLUSTER_MIN_SIZE=8`; батч скипается при <8 ready-историй ([cluster_orchestrator.py:159-160](../../../../../../src/core/application/cluster_orchestrator.py#L159-L160)).
- Лейблы в canvas разнородные (напр. `roads/education/safety/unsafe_condition/...`), gateway маппит canonical→governed (`waste/district/infrastructure/safety`).
- Загрузчик берёт canvas по пути `SIMULATION_CANVAS_PATH` (можно указать новый файл, не трогая v0_1).
- Primary lens `civic_domain_micro` + `CLUSTER_GEO_FILTER` → кластер по civic_domain signal и geo bucket ([enrichment.py:37-78](../../../../../../src/core/profile/enrichment.py), [service_factory.py:97-100](../../../../../../src/core/infrastructure/service_factory.py)).

## Требование / целевое состояние
- Подготовить расширенный датасет, где по нескольким темам набирается **≥8 историй с общими `canonical_labels`** → гарантированно ≥1 issue на доске (лучше несколько, по разным группам).
- Не понижать `CLUSTER_MIN_SIZE` (D-SEED-2).
- Новый файл (напр. `dogestonia_simulation_canvas_v0_2.json`), v0_1 остаётся baseline тестов (не ломать существующие тесты на v0_1).
- Реалистичность: вариации текста/локали/шумности на одну тему (как разные жители об одном), чтобы кластер был осмысленным.

## Out of scope
- Правки `src/core/` application code
- Понижение `CLUSTER_MIN_SIZE` (D-SEED-2)
- E2E seed-runbook / hosted board verify (SEED-03)
- Новый ручной триггер кластеризации
- Изменение [`dogestonia_simulation_canvas_v0_1.json`](../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json)
- Audit follow-up SEED-01 T06 / `pkg-000036`

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-seed-02-t01-target-cluster-design-matrix`](./task-gw-seed-02-t01-target-cluster-design-matrix/README.md) | pkg-000037 |
| 2 | [`task-gw-seed-02-t02-generate-simulation-canvas-v0-2`](./task-gw-seed-02-t02-generate-simulation-canvas-v0-2/README.md) | pkg-000037 |
| 3 | [`task-gw-seed-02-t03-local-clustering-and-promotion-verify`](./task-gw-seed-02-t03-local-clustering-and-promotion-verify/README.md) | pkg-000037 |
| 4 | [`task-gw-seed-02-t04-expected-board-fill-matrix`](./task-gw-seed-02-t04-expected-board-fill-matrix/README.md) | pkg-000037 |
| 5 | [`task-gw-seed-02-t05-story-acceptance-gate`](./task-gw-seed-02-t05-story-acceptance-gate/README.md) | pkg-000037 |

## Acceptance Criteria
- [x] Расширенный canvas создан отдельным файлом; v0_1 не изменён.
- [x] По ≥N темам набирается ≥8 историй с общими метками (N согласовано в T01).
- [x] На прогоне формируются проекции issue (локально подтверждено).
- [x] Зафиксировано ожидаемое наполнение доски.

## Открытые вопросы
- Сколько issue-карточек и в каких группах нужно для «наполненного» демо?
- Генерировать историями-вариациями вручную/скриптом, или дублировать реальные с перефразировкой?
