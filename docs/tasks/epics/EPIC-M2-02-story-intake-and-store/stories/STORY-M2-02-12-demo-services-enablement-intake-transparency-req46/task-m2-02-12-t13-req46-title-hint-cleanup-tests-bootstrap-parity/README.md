## Task workspace — `task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Depends on: T12

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~45 min  
**Status:** ready  
**Wave:** override `run_mode=story02_12_req46_title_hint_purge_and_cleanup` (T13)  
---

## Task: tests — bootstrap parity and integration payloads without title_hint

### AC/DoD
- [ ] (P0) `test_supabase_bootstrap_schema.py` — no assert on dropped hint columns
- [ ] (P0) `tests/integration/supabase/*` — v2 `narrative_title` only
- [ ] (P0) `pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration` green

### Команды
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_bootstrap_schema.py tests/test_story_repository.py
python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
