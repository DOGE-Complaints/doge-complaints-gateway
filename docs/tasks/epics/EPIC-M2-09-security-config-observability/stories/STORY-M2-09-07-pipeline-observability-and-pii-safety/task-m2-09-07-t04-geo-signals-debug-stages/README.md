## Task workspace — `task-m2-09-07-t04-geo-signals-debug-stages`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: REQ-37 §2.1 geo + signals rows

---
**Приоритет:** P1  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: implement — geo and signals JSONL stages

### Цель
Принять optional `StoryDebugLogger` (or protocol) в geo resolve и profile enrichment; записать `geo` (`resolved`/`skipped`) и `signals` (`inferred`) events.

### Факты из кода
1. [`geo/service.py`](../../../../../../../src/core/geo/service.py) L26–50 — `logger.debug` only; no `debug_logger` parameter.
2. [`profile/enrichment.py`](../../../../../../../src/core/profile/enrichment.py) — exists; signal inference path for civic dimensions.
3. REQ cascade lists `engine.py` — **факт:** geo/signals stages wire here, not engine.

### Gap / Проблема
**GAP-37-05 (partial):** downstream layers lack structured per-story JSONL for geo and signals.

### AC/DoD
- [ ] (P0) `geo` stage: `resolved` with provider, normalized_label, confidence, admin_* when present; or `skipped`.
- [ ] (P0) `signals` stage: `inferred` with signals dict summary (no raw PII in `data`).
- [ ] (P1) No-op when `debug_logger` is None.

### Где менять код
- [`src/core/geo/service.py`](../../../../../../../src/core/geo/service.py)
- [`src/core/profile/enrichment.py`](../../../../../../../src/core/profile/enrichment.py)

### Out of scope
- Cluster/promotion (T05)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req37_pipeline_observability_pii.py -q -k geo 2>/dev/null || true
```
