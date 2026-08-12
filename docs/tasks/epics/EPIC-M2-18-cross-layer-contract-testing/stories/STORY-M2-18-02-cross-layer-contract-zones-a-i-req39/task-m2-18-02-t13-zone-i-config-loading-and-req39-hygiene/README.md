## Task workspace — `task-m2-18-02-t13-zone-i-config-loading-and-req39-hygiene`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **I**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — DB_BACKEND ↔ factory wiring + REQ-39 docs hygiene

### Цель
DB_BACKEND ↔ factory wiring + REQ-39 docs hygiene (Zone **I**). Offline contract tests per REQ-39.

### Факты из кода
1. `test_config_loading.py` — partial zone I coverage.
2. `ServiceFactory` / `DB_BACKEND` — `service_factory.py`, `providers.py`.
3. Stale refs: `req-cross-layer-contract-testing.md` in tests/tasks; README-index line 70.

### Gap / Проблема
Factory wiring regressions; documentation drift from unnumbered req file.

### AC/DoD
- [x] (P0) I-01..I-03 (+3) per REQ-39 §I in `test_config_loading.py`.
- [x] (P0) AC-39-1: update `README-index.md` — add `39-cross-layer-contract-testing.md`; fix/remove `39-issue-management-api-endpoint.md` entry.
- [x] (P1) Update `test_stories_schema_cross_layer_invariant.py` comment + `task-m2-02-05-t08` Decision Ref.

### Где менять код
- `tests/test_config_loading.py` (extend)
- `docs/requirements/README-index.md`
- `tests/test_stories_schema_cross_layer_invariant.py` (comment)
- `docs/tasks/.../task-m2-02-05-t08-.../README.md` (Decision Ref)

### Out of scope
Zones A–H test implementation (other tasks).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_config_loading.py
```
