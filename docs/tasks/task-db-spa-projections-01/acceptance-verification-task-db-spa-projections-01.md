# Acceptance Verification — TASK-DB-SPA-PROJECTIONS-01

- [ ] `spa_issue_projections` хранится отдельно от доменных source tables.
- [ ] `issue_id` linkage и обязательные projection поля консистентны.
- [ ] Projection persistence покрыта integration tests.
- [ ] PM gate: dashboard читает устойчивую DB проекцию.
- [ ] CTO gate: read-model не смешан с доменным source-of-truth.
