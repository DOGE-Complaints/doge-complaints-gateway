## Task: test — Live Supabase HTTP integration and story-first roundtrip

Key: TASK-SH-P2-02  
Priority: P2  
Status: Todo  
Closes: SH-TEST-HTTP-INT-01  
Decision Ref: `docs/tasks/task-test-integration-supabase-live-01/task-test-integration-supabase-live-01.md`

### Goal
Проверить HTTP-ветку на live Supabase: roundtrip intake->cluster->issue->projection и readiness probes.

### AC/DoD
- [ ] Live integration tests покрывают story-first roundtrip.
- [ ] Live readiness probes работают в HTTP режиме.
- [ ] Все live тесты skip-safe при отсутствии env.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/integration/supabase -q
python3 -m pytest tests -k "story_first and supabase and live" -q
```
