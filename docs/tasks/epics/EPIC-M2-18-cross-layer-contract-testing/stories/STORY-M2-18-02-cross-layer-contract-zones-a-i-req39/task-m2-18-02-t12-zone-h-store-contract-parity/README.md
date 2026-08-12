## Task workspace — `task-m2-18-02-t12-zone-h-store-contract-parity`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **H**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — Embedding/Signal/Cluster store parity

### Цель
Embedding/Signal/Cluster store parity (Zone **H**). Offline contract tests per REQ-39.

### Факты из кода
1. Store protocols — embedding, signal, cluster membership paths.
2. In-memory vs persistence backends per REQ-39 §H.

### Gap / Проблема
Auxiliary stores can diverge silently between backends.

### AC/DoD
- [x] (P0) H-01..H-03 per REQ-39 §H.

### Где менять код
- `tests/test_store_contract_parity.py` (new)

### Out of scope
Full E2E pipeline (zone N).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_store_contract_parity.py
```
