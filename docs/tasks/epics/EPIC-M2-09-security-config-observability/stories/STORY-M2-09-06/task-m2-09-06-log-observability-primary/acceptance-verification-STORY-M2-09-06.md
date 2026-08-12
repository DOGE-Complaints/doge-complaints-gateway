# Acceptance verification — task-m2-09-06-log-observability-primary

## AC checklist
- [x] Story gate закрыт, все GAP-LOG задачи покрыты в task artifacts.

## Verification commands
```bash
cd doge-complaints-gateway && pytest -q tests/test_cluster_cron_job.py tests/test_asgi_lifespan_cron.py tests/test_http_intake_endpoint.py tests/test_supabase_observability.py
```

## Verification performed
- Реализованы structured runtime exception события через `log_runtime_exception` и HTTP middleware.
- Реализованы `cluster.cron_run_start`/`cluster.cron_run_end` + агрегированные поля цикла.
- Реализовано unified событие `supabase.request_failed` в transport слое.
- Реализовано финальное событие `story.pipeline_outcome` в intake path.
- Реализовано событие `shutdown.lifecycle` с `shutdown_reason`.
- Тесты: `11 passed`.
