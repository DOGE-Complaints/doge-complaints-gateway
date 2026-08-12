## Task workspace — `task-m2-09-08-t05-audit-gap45-02-http-intake-capsys-stdout`

- Story: [`../STORY-M2-09-08-production-logging-noise-reduction-req45.md`](../STORY-M2-09-08-production-logging-noise-reduction-req45.md)
- Decision Ref: [`../../../../../../analysis/audit-req45-production-logging-noise-reduction-2026-05-28.md`](../../../../../../analysis/audit-req45-production-logging-noise-reduction-2026-05-28.md) §4 GAP-02; [`../../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../../requirements/45-production-logging-noise-reduction.md) §5 (full unit suite)

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~15 min  
**Status:** ready  
**Wave:** audit override (`run_mode=story09_08_audit_req45_followup`)  
---

## Task: tests — intake observability capsys INFO → stdout (5 asserts)

### Цель
Восстановить `test_intake_emits_cluster_pending_observability_event` после stdout/stderr split: все INFO observability-строки assert в `captured.out`.

### Почему это важно (риск)
Аудит §4 GAP-02 указывает одну строку (L120); фактически **пять** assert на `captured.err` (L120–124) — все INFO → stdout после REQ-45.

### Факты из кода
1. [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py) L101–124 — `test_intake_emits_cluster_pending_observability_event` + `capsys.readouterr()`.
2. L120 — `story.persistence_backend_selected backend=in_memory`
3. L121 — `story.persistence_commit_ack backend=in_memory lifecycle_status=ready_for_profile`
4. L122 — `story_cluster_issue_pending`
5. L123 — `trace-cluster-pending`
6. L124 — `story.pipeline_outcome`
7. [`src/core/logging_setup.py`](../../../../../../../src/core/logging_setup.py) — INFO → stdout handler only.

### Gap / Проблема
**GAP-02 (audit):** заменить `captured.err` → `captured.out` для L120–124 (не только L120).

### AC / DoD
- [ ] (P0) L120–124: все пять assertions читают `captured.out`.
- [ ] (P0) `python3 -m pytest -q tests/test_http_intake_endpoint.py::test_intake_emits_cluster_pending_observability_event` — passed.
- [ ] (P1) Sanity: `python3 -m pytest -q tests/test_http_intake_endpoint.py` — module green (no regressions in sibling tests).

### Где менять
- Только [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py) в `test_intake_emits_cluster_pending_observability_event`.

### Out of scope
- Intake domain logic, handlers, OpenAPI.
- [`tests/test_asgi_lifespan_cron.py`](../../../../../../../tests/test_asgi_lifespan_cron.py) — TASK-M2-09-08-T04.
- GAP-03 smoke (`tests/smoke/`) — pre-existing, не REQ-45.
- Новый `pkg-*.yaml`.

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_http_intake_endpoint.py::test_intake_emits_cluster_pending_observability_event
python3 -m pytest -q tests/test_http_intake_endpoint.py
```
