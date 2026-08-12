## Task workspace — `task-m2-09-07-t03-services-intake-debug-logger`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: REQ-37 §2.1 intake stage; G-06

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: implement — intake `StoryDebugLogger` + PII in services

### Цель
Инстанцировать `StoryDebugLogger` в story pipeline entry; логировать `intake` / `story_accepted`; применить `redact_pii` где narrative попадает в логи; передавать logger downstream.

### Факты из кода
1. [`application/services.py`](../../../../../../../src/core/application/services.py) L30 — module logger; L168–235 intake persistence logs без JSONL stage.
2. L409 — `_canonical_story_embedding_source`: `f"text={story.narrative_original_text.strip()}"` (**PII leak risk**, GAP-37-04).
3. REQ-37 §2.1 — `data`: lifecycle, language, session_language, has_canonical_type.

### Gap / Проблема
**GAP-37-04:** services не создаёт/не передаёт `StoryDebugLogger`; narrative text в embedding source string без redaction.

### AC/DoD
- [ ] (P0) `StoryDebugLogger` created per story when `log_debug_dir` configured.
- [ ] (P0) `stage=intake`, `event=story_accepted` with REQ-37 fields.
- [ ] (P0) `redact_pii` on any logged `original_text` / narrative fields when `privacy_contains_pii`.
- [ ] (P1) Optional param or context for downstream (geo, enrichment, cluster).

### Где менять код
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)

### Out of scope
- Geo/signals/cluster stages (T04–T05)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req37_pipeline_observability_pii.py -q -k intake 2>/dev/null || true
```
