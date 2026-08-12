# Demo data seeding — backend story package · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/`
**Тип:** backlog (продуктовая проработка).
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — факты по фактическому коду, пути указаны.

## Связи (traceability)
- **Стартовые артефакты:** [`tests/sandbox/dogestonia_simulation_canvas_v0_1.json`](../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json), [`simulation-runner-manual.md`](../../../runtime-docs/testing/simulation-runner-manual.md).
- **Интервью CPO/CTO (решения D-SEED):** [`docs/analysis/interview-seed-demo-data-2026-06-20.md`](../../../analysis/interview-seed-demo-data-2026-06-20.md).
- **Итоговый мануал:** [`docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md`](../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md).

## Цель одной фразой
Наполнить hosted-демо (Railway+Supabase) тестовыми историями так, чтобы сработала кластеризация (кластеры ≥8) и **дашборд показал issue-карточки**, плюс воспроизводимый мануал «как это делать».

## Ключевой verified-факт
Загрузка истории ≠ карточка на доске. Цепочка: `POST /story-drafts` (service stash) → `POST /story-drafts/{id}/submit` (browser Bearer + identity `/me`) → cron-кластеризация (`process_all_pending`) → промоушн кластера ≥`CLUSTER_MIN_SIZE=8` → проекция issue → `GET /tallinn/issues` (доска). Legacy `POST /intake/stories` удалён ([GW-DRAFT-06](../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) Done). Ручного триггера кластеризации нет; cron `CLUSTER_CRON_ENABLED` default=`true`, интервал 60s. NB: `CLUSTER_MIN_SIZE` — **вариабельное значение** (per-environment tunable); `8` здесь — пример/дефолт, не фиксированный контракт (см. [audit-mvp-scope-hard-2026-07-21](../../../analysis/audit-mvp-scope-hard-2026-07-21.md) §F6). Этот MVP in-process `ClusterCronJob` ≠ post-demo automation plane (job runner / queue / replay) — разведение скоупа: [DOC-TASK-CRON-SCOPE-01](./DOC-TASK-CRON-SCOPE-01-clarify-cron-in-mvp.md), EPIC-M2-11.

## Коды статусов (S)
⚪ Todo · 🟡 In Progress · 🔵 Implemented (Waiting Acceptance) · 🟢 Done (Committed)

## Стори пакета

| S | Key | Story | Закрывает | Зависит от | Status |
|---|-----|-------|-----------|------------|--------|
| 🔵 | GW-SEED-01 | [Загрузчик + готовность hosted-таргета](./STORY-GW-SEED-01-loader-and-hosted-readiness.md) | D-SEED-1, D-SEED-3 | RC-04 (columnar на hosted) | Done |
| 🔵 | GW-SEED-02 | [Расширение датасета для кластеризации (≥8/кластер)](./STORY-GW-SEED-02-dataset-expansion-for-clustering.md) → [pipeline](../epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/STORY-GW-SEED-02-dataset-expansion-for-clustering.md) | D-SEED-2 | — | Done |
| 🔵 | GW-SEED-03 | [E2E seed-runbook + board fill verification](./STORY-GW-SEED-03-end-to-end-seed-runbook.md) | D-SEED-4 | SEED-01, SEED-02, DRAFT-06 | Done (Awaiting Commits) |
| 🔵 | GW-SEED-04 | [Runner auth bootstrap (email+password → Supabase token)](./STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) → [pipeline](../epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-04-runner-auth-bootstrap-email-password/STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) | ops-запрос 2026-07-11 (убрать ручной `GATEWAY_USER_TOKEN`) | SEED-03, DRAFT-06 | Done (Awaiting Commits) |

**Progress:** 4/4 Done (100%); GW-SEED-04 pkg-000051 T01–T06 + audit follow-up T07–T08 Done 2026-07-11

## Решения интервью (D-SEED, 2026-06-20)
- **D-SEED-1:** таргет — hosted Railway+Supabase (живой демо); предусловие — columnar-миграции RC-04 применены + cron включён.
- **D-SEED-2:** объём — расширить датасет (общие `canonical_labels` → ≥8/кластер), НЕ понижать `CLUSTER_MIN_SIZE`.
- **D-SEED-3:** триггер — cron (включить+подождать), новый ручной триггер не делаем.
- **D-SEED-4:** полный seed-пакет (загрузка + объём + cron + мануал).
