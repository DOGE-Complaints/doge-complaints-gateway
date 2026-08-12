# Acceptance verification — task-m2-09-06-t05-gap-log-05-shutdown-reason

## AC checklist
- [x] GAP-LOG-05 закрыт: в логах фиксируется структурный `shutdown_reason`.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```

## Verification performed
- В lifespan добавлено событие `shutdown.lifecycle` с полем `shutdown_reason`.
- Добавлены signal hooks (`SIGINT`/`SIGTERM`) для явной маркировки причины завершения.
- Добавлен тест `test_lifespan_emits_shutdown_reason_log`.
