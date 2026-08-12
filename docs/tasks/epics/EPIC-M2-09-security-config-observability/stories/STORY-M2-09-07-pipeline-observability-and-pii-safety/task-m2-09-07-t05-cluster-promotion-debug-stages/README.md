## Task workspace — `task-m2-09-07-t05-cluster-promotion-debug-stages`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: REQ-37 §2.1 cluster + promotion rows

---
**Приоритет:** P1  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: implement — cluster and promotion JSONL stages

### Цель
Логировать `cluster` (`assigned`/`created`) и `promotion` (`gate_result`) в per-story JSONL at **actual call sites**.

### Факты из кода
1. [`cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py) L88–151 — cluster membership / grouping; `logger` extra with `cluster_id`.
2. [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) — issue promotion path.
3. [`promotion/gates.py`](../../../../../../../src/core/promotion/gates.py) — pure `evaluate_promotion_gates`; **no logging** inside.
4. REQ §4 cascade mentions `engine.py` / `gates.py` — implement at orchestrator + issue_create callers.

### Gap / Проблема
**GAP-37-05 (partial):** cluster/promotion stages absent from JSONL pipeline trace.

### AC/DoD
- [ ] (P0) `cluster` event: cluster_id, lens, cluster_key, is_new per REQ-37 table.
- [ ] (P0) `promotion` event: readiness_score, threshold, canonical_type gate pass/fail, promoted, issue_id when applicable.
- [ ] (P1) Do not add side effects inside `evaluate_promotion_gates`.

### Где менять код
- [`src/core/application/cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py)
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py)

### Out of scope
- Changing promotion gate logic (REQ-34/36)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req37_pipeline_observability_pii.py -q -k cluster 2>/dev/null || true
```
