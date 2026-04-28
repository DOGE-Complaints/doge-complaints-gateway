## Task: implement — Supabase readiness and preflight via HTTP probes

Key: TASK-SH-P1-03  
Priority: P1  
Status: Todo  
Closes: SH-READINESS-HTTP-01  
Supersedes: TASK-DB-READINESS-SUPABASE-02  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Убрать DSN-зависимость из readiness и перейти на HTTP preflight probes с диагностикой причин `db.not_ready`.

### AC/DoD
- [ ] Connectivity/table/column/policy probes работают через HTTP.
- [ ] `/health` и `/readiness` возвращают детализированные DB checks.
- [ ] Тесты readiness ветки покрывают positive/negative режимы.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_http_readiness.py tests/test_api_security_and_ops.py -q
```
