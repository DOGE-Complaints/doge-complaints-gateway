# DOC-TASK-CRON-SCOPE-02 — Architecture SSOT: MVP-cron caveat в requirements / solution architecture

- **Тип:** Documentation task (не product story — правки только в доках, код не трогаем).
- **Пакет:** demo-data-seeding.
- **Статус:** ✅ Done (2026-07-23)
- **Источник:** [audit-doc-task-cron-scope-01-followup-2026-07-23.md](../../../analysis/audit-doc-task-cron-scope-01-followup-2026-07-23.md) §3–§4 (G1–G4).
- **Предшественник:** [DOC-TASK-CRON-SCOPE-01](./DOC-TASK-CRON-SCOPE-01-clarify-cron-in-mvp.md) (Done; product docs). Этот task — архитектурный слой.
- **Приоритет:** P2.

## Проблема

После -01 high-level / seeding INDEX / EPIC-M2-11 / example.env согласованы с кодом, но `requirements/03`, `solution architecture/16`, `solution architecture/10`, `requirements/20` по-прежнему фреймили cron / периодические пересчёты как целиком post-demo без упоминания MVP `ClusterCronJob`.

## Канонический caveat

Минимальный in-process `ClusterCronJob` (`CLUSTER_CRON_ENABLED`, default ON) — триггер promotion→projection→доска — **входит в MVP** и уже вызывает те же application use-case, что и API. «Post-demo automation» относится к **обобщённому** plane (job runner / queue / sweep / ручной replay) поверх него (EPIC-M2-11), а не к этому минимальному циклу.

## Scope of edits (выполнено)

1. **G1** [`requirements/03-scope-and-boundaries.md`](../../../requirements/03-scope-and-boundaries.md) — Post-demo backlog: обобщённый plane + NB MVP-cron.
2. **G2** [`solution architecture/16-automation-orchestration-and-scheduled-jobs.md`](../../../solution%20architecture/16-automation-orchestration-and-scheduled-jobs.md) — §Назначение: «Уже в MVP».
3. **G3** [`solution architecture/10-data-architecture-and-state-model.md`](../../../solution%20architecture/10-data-architecture-and-state-model.md) — заголовок без абсолюта `(post-demo)` + инвариант соблюдён MVP-cron.
4. **G4** [`requirements/20-post-demo-orchestration-and-scheduled-jobs.md`](../../../requirements/20-post-demo-orchestration-and-scheduled-jobs.md) — §Статус: back-ref на MVP-cron.

## Явно НЕ входит

- Изменения кода / поведения cron.
- Выбор runner/queue (EPIC-M2-11).

## Definition of Done

- [x] G1: requirements/03 — NB, что MVP-cron входит в скоуп.
- [x] G2: solution architecture/16 §Назначение — «уже в MVP» разграничение.
- [x] G3: solution architecture/10 — заголовок без абсолюта «(post-demo)» + инвариант MVP-cron.
- [x] G4: requirements/20 §Статус — back-ref на MVP-cron.
- [x] Grep-гейт: нет утверждений «оркестрация/cron = post-demo» без caveat.
- [x] Dashboard §Docs backlog — строка DOC-TASK-CRON-SCOPE-02 Done.
