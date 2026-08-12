## Task workspace — `task-m2-09-08-t04-audit-gap45-01-asgi-lifespan-capsys-stdout`

- Story: [`../STORY-M2-09-08-production-logging-noise-reduction-req45.md`](../STORY-M2-09-08-production-logging-noise-reduction-req45.md)
- Decision Ref: [`../../../../../../analysis/audit-req45-production-logging-noise-reduction-2026-05-28.md`](../../../../../../analysis/audit-req45-production-logging-noise-reduction-2026-05-28.md) §4 GAP-01; [`../../../../../../requirements/45-production-logging-noise-reduction.md`](../../../../../../requirements/45-production-logging-noise-reduction.md) §5 (full unit suite)

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~15 min  
**Status:** ready  
**Wave:** audit override (`run_mode=story09_08_audit_req45_followup`)  
---

## Task: tests — capsys INFO assertions → stdout after REQ-45 split

### Цель
Восстановить зелёный прогон `tests/test_asgi_lifespan_cron.py` после stdout/stderr split в `configure_logging()`: INFO lifecycle-логи теперь в stdout, не в stderr.

### Почему это важно (риск)
Три теста assertят `captured.err` для INFO-сообщений; после REQ-45 T01 они пишутся в `captured.out` → 3 failing tests, suite 427 passed / 4 failed (audit §3).

### Факты из кода
1. [`tests/test_asgi_lifespan_cron.py`](../../../../../../../tests/test_asgi_lifespan_cron.py) L83 — `assert "shutdown.lifecycle" in captured.err`
2. [`tests/test_asgi_lifespan_cron.py`](../../../../../../../tests/test_asgi_lifespan_cron.py) L99 — `assert "startup.persistence_backend backend=in_memory" in captured.err`
3. [`tests/test_asgi_lifespan_cron.py`](../../../../../../../tests/test_asgi_lifespan_cron.py) L115 — `assert "startup.persistence_backend backend=supabase" in captured.err`
4. [`src/core/logging_setup.py`](../../../../../../../src/core/logging_setup.py) L29-33, L138-149 — `_LevelBelowWarningFilter` + stdout handler для DEBUG/INFO.

### Gap / Проблема
**GAP-01 (audit):** механическая смена потока capsys `err` → `out` в трёх тестах; логика тестов корректна.

### AC / DoD
- [ ] (P0) L83, L99, L115: `captured.err` → `captured.out` для перечисленных INFO assertions.
- [ ] (P0) `python3 -m pytest -q tests/test_asgi_lifespan_cron.py` — all passed.
- [ ] (P1) Не менять `src/core/logging_setup.py` в этой задаче.

### Где менять
- Только [`tests/test_asgi_lifespan_cron.py`](../../../../../../../tests/test_asgi_lifespan_cron.py).

### Out of scope
- [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py) — TASK-M2-09-08-T05 (GAP-02).
- Новый или изменённый `pkg-*.yaml`; `gateway-active-package.current.yaml`.
- Повторная реализация T01–T03 из `pkg-000025`.

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_asgi_lifespan_cron.py
```
