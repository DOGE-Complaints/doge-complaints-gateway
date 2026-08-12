## Task workspace — `task-m2-09-08-t02-logging-setup-tests-handler-split-update`

- Story: [`../STORY-M2-09-08-production-logging-noise-reduction-req45.md`](../STORY-M2-09-08-production-logging-noise-reduction-req45.md)
- Decision Ref: [`../../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../../requirements/45-production-logging-noise-reduction.md) §3.4, §5

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~20 min  
**Status:** ready  
---

## Task
Обновить тест `test_configure_logging_removes_old_handlers` под stdout/stderr split.

## Scope (code)
- [`tests/test_logging_setup.py`](../../../../../../../tests/test_logging_setup.py)

## AC / DoD (source-of-truth: REQ-45)
- [ ] Проверка количества handlers: `1 -> 2`
- [ ] Проверка, что оба handlers — `StreamHandler`
- [ ] Остальные тесты модуля остаются зелеными

## Constraints
- Изменения только в тестах logging setup
- Не расширять scope в e2e/integration
