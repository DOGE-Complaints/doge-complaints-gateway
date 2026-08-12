# Acceptance verification — task-m2-09-06-t03-gap-log-03-supabase-request-failed

## AC checklist
- [x] GAP-LOG-03 закрыт: persistence ошибки Supabase фиксируются единообразно в `supabase.request_failed`.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```

## Verification performed
- В `SupabaseDatabase._request` добавлен унифицированный error event `supabase.request_failed`.
- Событие содержит `method/path/status_code/error_body_preview/error_type/stage`.
- Добавлен тест `tests/test_supabase_observability.py`.
