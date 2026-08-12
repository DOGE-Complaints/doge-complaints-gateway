# Acceptance verification — task-m2-09-06-t01-gap-log-01-global-exception-trace

## AC checklist
- [x] GAP-LOG-01 закрыт: runtime исключения имеют структурный trace с `stage` и `stack`.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```

## Verification performed
- Добавлен helper `log_runtime_exception` в `src/core/logging_setup.py`.
- Добавлен HTTP middleware runtime exception diagnostics в `src/core/api/asgi_app.py`.
- Исключения intake и cron логируются через единый event `runtime.exception`.
