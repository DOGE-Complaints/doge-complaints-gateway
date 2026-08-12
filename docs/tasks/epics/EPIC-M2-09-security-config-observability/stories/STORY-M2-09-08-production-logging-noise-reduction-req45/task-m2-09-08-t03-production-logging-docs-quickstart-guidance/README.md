## Task workspace — `task-m2-09-08-t03-production-logging-docs-quickstart-guidance`

- Story: [`../STORY-M2-09-08-production-logging-noise-reduction-req45.md`](../STORY-M2-09-08-production-logging-noise-reduction-req45.md)
- Decision Ref: [`../../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../../requirements/45-production-logging-noise-reduction.md) §3.5

---
**Priority:** P2  
**Complexity:** S  
**Estimate:** ~20 min  
**Status:** ready  
---

## Task
Добавить в quickstart секцию production logging recommendations.

## Scope (docs)
- [`docs/runtime-docs/server-env-quickstart.md`](../../../../../../../docs/runtime-docs/server-env-quickstart.md)

## AC / DoD (source-of-truth: REQ-45)
- [ ] Документирован `LOG_LEVEL=INFO` как production recommendation
- [ ] Документирован `LOG_FORMAT=json` для structured logs
- [ ] Уточнен operational note для `LOG_DEBUG_DIR` (ephemeral FS в Railway)

## Constraints
- Не изменять API/runtime контракты
- Изменение только документации quickstart
