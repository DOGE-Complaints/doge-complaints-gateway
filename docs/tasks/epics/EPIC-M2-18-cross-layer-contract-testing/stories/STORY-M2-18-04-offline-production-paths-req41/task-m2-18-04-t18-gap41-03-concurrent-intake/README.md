## Task workspace — `task-m2-18-04-t18-gap41-03-concurrent-intake`

- Story: [`../STORY-M2-18-04-offline-production-paths-req41.md`](../STORY-M2-18-04-offline-production-paths-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-03; PS-11

---
**Приоритет:** P2  
**Сложность:** M  
**Оценка времени:** ~2–3 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: tests — concurrent intake contract

### Цель
`tests/test_concurrent_intake_contract.py` — CC-01..02 with `ThreadPoolExecutor` + TestClient.

### Почему это важно (риск)
No concurrent intake tests; race on idempotency_keys or duplicate stories under load.

### Факты из кода
1. REQ-41 §3 — N=5 workers, unique `external_user_id` + `idempotency-key` per request.
2. Existing idempotency covered in single-thread tests (PS-12 Done).

### Gap / Проблема
**GAP-41-03:** zero concurrent intake coverage.

### AC/DoD
- [x] (P0) CC-01: 5 parallel `POST /intake/stories` → 5 unique story_ids, no HTTP errors.
- [x] (P0) CC-02: 5 parallel with same `idempotency-key` → exactly 1 story created.
- [x] (P1) Run 3× locally to confirm non-flaky.

### Где менять код
- `tests/test_concurrent_intake_contract.py` (new)

### Out of scope
- Load testing / k6; prod rate limits.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_concurrent_intake_contract.py
```
