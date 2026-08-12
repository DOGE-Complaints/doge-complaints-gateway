## Task workspace — `task-m2-09-08-t01-logging-setup-stdout-stderr-split-and-httpx-httpcore-suppress`

- Story: [`../STORY-M2-09-08-production-logging-noise-reduction-req45.md`](../STORY-M2-09-08-production-logging-noise-reduction-req45.md)
- Decision Ref: [`../../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../../requirements/45-production-logging-noise-reduction.md) §3.1, §3.2, §3.3

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~60 min  
**Status:** ready  
---

## Task
Внести runtime-патч в `configure_logging()`:
- stdout/stderr split handlers,
- suppress `httpx`/`httpcore` до `WARNING`,
- уточнить комментарий про `log_debug_dir` (REQ-37 compatibility).

## Scope (code)
- [`src/core/logging_setup.py`](../../../../../../../src/core/logging_setup.py)

## AC / DoD (source-of-truth: REQ-45)
- [ ] Добавлен `_LevelBelowWarningFilter`
- [ ] `DEBUG/INFO` -> stdout handler, `WARNING+` -> stderr handler
- [ ] `logging.getLogger("httpx").setLevel(logging.WARNING)` и аналог для `httpcore`
- [ ] Комментарий `del log_debug_dir` уточнен без изменения поведения REQ-37

## Constraints
- Не менять логику domain/application/infra
- Не менять OpenAPI/API contracts
- Сохранить обратную совместимость с текущими тестами после update T02
