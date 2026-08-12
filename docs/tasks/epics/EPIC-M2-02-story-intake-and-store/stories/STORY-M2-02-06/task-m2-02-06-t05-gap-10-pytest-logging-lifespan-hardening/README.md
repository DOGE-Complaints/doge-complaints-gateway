## Task workspace — `task-m2-02-06-t05-gap-10-pytest-logging-lifespan-hardening`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 4, **GAP-10** (закрыт: session autouse `configure_logging` в pytest)
- Существующая заметка: [`docs/runtime-docs/testing/pytest-logging-without-asgi-lifespan.md`](../../../../../../../docs/runtime-docs/testing/pytest-logging-without-asgi-lifespan.md)

## Task: tests — pytest: `configure_logging` без ASGI lifespan

### Цель
Закрыть остаток §16: либо `conftest.py` с opt-in вызовом `configure_logging`, либо unit-тест, фиксирующий уровень root до/после (без изменения prod-поведения без ADR).

### Факты из кода (§16)
1) `configure_logging` — [`src/core/logging_setup.py`](../../../../../../../src/core/logging_setup.py).
2) Вызов из lifespan — [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Тесты intake observability могут быть ложно-позитивны; нет узкого автотеста на сценарий «pytest без lifespan».

### AC/DoD
- [x] (P1) `tests/conftest.py`: session-scoped autouse fixture вызывает `configure_logging(...)`.
- [x] (P2) Строка GAP-10 в §16 анализа обновлена.

### Где менять код
- [`tests/conftest.py`](../../../../../../../tests/conftest.py) (создать при отсутствии)
- [`tests/test_intake_observability.py`](../../../../../../../tests/test_intake_observability.py) при необходимости

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_intake_observability.py tests/test_supabase_observability.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t05.md`](./implementation-plan-m2-02-06-t05.md)
- [`acceptance-verification-m2-02-06-t05.md`](./acceptance-verification-m2-02-06-t05.md)
- [`retrospective-m2-02-06-t05-full.md`](./retrospective-m2-02-06-t05-full.md)
