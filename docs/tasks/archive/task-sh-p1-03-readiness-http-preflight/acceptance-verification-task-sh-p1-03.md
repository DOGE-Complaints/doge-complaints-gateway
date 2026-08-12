# Acceptance verification — TASK-SH-P1-03

## Checklist
- [ ] Readiness probes не используют DSN/psycopg путь.
- [ ] Причины `db.not_ready` выдаются детерминированно.
- [ ] Regression по readiness API проходит.

## Verification commands
- `python3 -m pytest tests/test_http_readiness.py tests/test_api_security_and_ops.py -q`
- `rg -n "required_tables_ready|required_columns_ready|service_role_policy_probe" src/core`
