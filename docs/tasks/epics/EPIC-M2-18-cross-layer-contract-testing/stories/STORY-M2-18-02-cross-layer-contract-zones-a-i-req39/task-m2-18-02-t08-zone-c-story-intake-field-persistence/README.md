## Task workspace — `task-m2-18-02-t08-zone-c-story-intake-field-persistence`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **C**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — StoryIntakeRequest ↔ StoryRecord field mapping

### Цель
StoryIntakeRequest ↔ StoryRecord field mapping (Zone **C**). Offline contract tests per REQ-39.

### Факты из кода
1. Mapping in `services.py` StoryIntakeService.
2. MVP: `tests/test_stories_schema_cross_layer_invariant.py` (STORY-M2-02-05-T08).
3. REQ-39 §C — fuller seam C-01..C-04.

### Gap / Проблема
MVP invariant ≠ full intake field persistence contract.

### AC/DoD
- [x] (P0) C-01..C-04 per REQ-39 §C.
- [x] (P1) Do not duplicate MVP invariant assertions — extend seam only.
- [x] (P2) Update comment in `test_stories_schema_cross_layer_invariant.py` → REQ-39 path (or defer to T13).

### Где менять код
- `tests/test_story_intake_field_persistence.py` (new)

### Out of scope
Intake contract v2 breaking changes (REQ-33).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_field_persistence.py
```
