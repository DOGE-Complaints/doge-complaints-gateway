## Task workspace — `task-m2-18-01-t04-zone-k-geo-propagation-contract`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **K**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — Geo propagation StoryRecord.geo → doge_issues payload

### Цель
Geo propagation StoryRecord.geo → doge_issues payload (Zone **K**). Offline contract tests; дополняют REQ acceptance suites, не заменяют `test_req24_*` / `test_req40_*` без решения оператора.

### Факты из кода
1. Chain: `StoryRecord.geo` → `ProjectionInput.geo_snapshot` → `DOGEIssue.geo` → `payload_json["geo"]` (REQ-39 §K).
2. `tests/test_req40_geo_propagation.py` — overlap risk; contract file focuses on seam assertions only.

### Gap / Проблема
Geo can be dropped in bridge/policy without unit tests catching serialization path.

### AC/DoD
- [x] (P0) K-01..K-04 per REQ-39 §K.
- [x] (P0) Reuse `test_req40` helpers where DRY; no duplicate full REQ-40 AC matrix.
- [x] (P1) `normalize_geo_token` for district (K-03).

### Где менять код
- `tests/test_geo_propagation_contract.py` (new)

### Out of scope
REQ-40 feature changes; geo scope filtering (REQ-35).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_geo_propagation_contract.py
```
