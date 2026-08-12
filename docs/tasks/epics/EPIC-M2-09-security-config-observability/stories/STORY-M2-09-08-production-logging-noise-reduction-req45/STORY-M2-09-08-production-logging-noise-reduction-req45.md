# STORY-M2-09-08: Production logging noise reduction (REQ-45)

## Meta
- Key: `STORY-M2-09-08`
- Parent Epic: [`../../../EPIC-M2-09-security-config-observability.md`](../../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Observability / production logging hygiene
- Decision Ref: [`../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../requirements/45-production-logging-noise-reduction.md)
- Depends on: STORY-M2-09-03 (structured logging baseline), STORY-M2-09-07 (REQ-37)
- Out of scope: domain/application/infra behavior changes; OpenAPI or API contract changes

## Story Goal
Снизить production logging noise и корректно разделить stdout/stderr в runtime, не затрагивая бизнес-логику и не ломая REQ-37 per-story debug path.

## Scope
- Runtime logging setup: `src/core/logging_setup.py`
- Unit tests: `tests/test_logging_setup.py`
- Runtime docs: `docs/runtime-docs/server-env-quickstart.md`

## Out of scope
- Изменения в `services.py`, `cluster_orchestrator.py`, `handlers.py`, DB репозиториях
- Изменения `API_REFERENCE.md`/OpenAPI
- Любые изменения продукта beyond logging behavior

## Why this epic (reuse justification)
1. REQ-45 относится к observability/logging subsystem: [`../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../requirements/45-production-logging-noise-reduction.md).
2. EPIC-M2-09 покрывает security/config/observability и structured logging: [`../../../EPIC-M2-09-security-config-observability.md`](../../../EPIC-M2-09-security-config-observability.md).
3. Launch index фиксирует M2-09 как активную observability wave: [`../../../../bullrun-launch-index.md`](../../../../bullrun-launch-index.md).

## Nested tasks

| Order | Task folder |
|-------|-------------|
| 1 | [`task-m2-09-08-t01-logging-setup-stdout-stderr-split-and-httpx-httpcore-suppress`](./task-m2-09-08-t01-logging-setup-stdout-stderr-split-and-httpx-httpcore-suppress/README.md) |
| 2 | [`task-m2-09-08-t02-logging-setup-tests-handler-split-update`](./task-m2-09-08-t02-logging-setup-tests-handler-split-update/README.md) |
| 3 | [`task-m2-09-08-t03-production-logging-docs-quickstart-guidance`](./task-m2-09-08-t03-production-logging-docs-quickstart-guidance/README.md) |
| 4 | [`task-m2-09-08-t04-audit-gap45-01-asgi-lifespan-capsys-stdout`](./task-m2-09-08-t04-audit-gap45-01-asgi-lifespan-capsys-stdout/README.md) — audit override only |
| 5 | [`task-m2-09-08-t05-audit-gap45-02-http-intake-capsys-stdout`](./task-m2-09-08-t05-audit-gap45-02-http-intake-capsys-stdout/README.md) — audit override only |

## Story AC / DoD (from REQ-45)
- [x] `configure_logging("INFO")` создает 2 `StreamHandler` (stdout + stderr split)
- [x] `INFO` идет в stdout, `WARNING+` идет в stderr
- [x] `httpx` и `httpcore` зажаты до `WARNING` в `configure_logging()`
- [x] `tests/test_logging_setup.py` обновлен под split
- [x] Документация runtime env содержит production guidance (`LOG_LEVEL=INFO`, `LOG_FORMAT=json`)
- [x] REQ-37 функциональность (`LOG_DEBUG_DIR`/StoryDebugLogger) не регрессирует
- [x] Non-smoke unit suite без регрессий от stdout/stderr split (audit [`audit-req45-production-logging-noise-reduction-2026-05-28.md`](../../../../../analysis/audit-req45-production-logging-noise-reduction-2026-05-28.md) §5 — GAP-01/02)

## Traceability: REQ-45 -> tasks
- REQ-45 §3.1, §3.2, §3.3 -> T01
- REQ-45 §3.4 -> T02
- REQ-45 §3.5 -> T03
- audit GAP-01 -> T04 (`run_mode=story09_08_audit_req45_followup`)
- audit GAP-02 -> T05 (`run_mode=story09_08_audit_req45_followup`)
