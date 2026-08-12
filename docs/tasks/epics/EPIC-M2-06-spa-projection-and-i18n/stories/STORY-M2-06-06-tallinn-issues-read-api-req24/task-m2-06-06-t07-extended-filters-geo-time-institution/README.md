## Task workspace — `task-m2-06-06-t07-extended-filters-geo-time-institution`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §3.1.1–3.1.2, §6 Phase 2 steps 13–17; REQ-40; GAP-24-07

---
**Приоритет:** P1  
**Сложность:** L  
**Оценка времени:** ~3–4 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — geo, time, institution filters (Phase 2)

### Цель
Реализовать расширенные фильтры во всех stores, handlers и route Query params: `institution`, `created_after`/`before`, geo bbox и address fields.

### Факты из кода
1. [`scope.py`](../../../../../../../src/core/geo/scope.py) L15 — `normalize_geo_token()` для address filters.
2. [`dto.py`](../../../../../../../src/core/projection/dto.py) — `to_public_dict()` emits `"geo"` when present (REQ-40).
3. REQ-24 §3.1.1 — post-fetch order; issues without `"geo"` excluded when any geo filter active.
4. REQ-24 §6 L701 — Phase 2 after REQ-40 (REQ-40 Done per STORY-M2-06-05).
5. SA-18 §2 — propagation gap **closed**; use payload `geo` for filters.

### Gap / Проблема
**GAP-24-07:** list endpoint не поддерживает geo/time/institution (AC-14..20, AC-19).

### AC/DoD
- [ ] (P0) All stores: full `list_projections` filter semantics per §3.1.1.
- [ ] (P0) Handlers pass all parameters to read store.
- [ ] (P0) Routes expose all Query params (REQ-24 §4.2).
- [ ] (P0) AC-14 bbox, AC-15 null-safety, AC-16 normalized district, AC-17 OR multi district, AC-18 bbox+address AND.
- [ ] (P0) AC-19 created_after/before; AC-20 empty geo params ignored.
- [ ] (P1) Reuse `normalize_geo_token` — no duplicate normalizer.

### Где менять код
- [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

### Out of scope
- `geo_postal_code` data population (REQ-40 Phase 3)
- PostGIS

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_req24_tallinn_issues_read_api.py -k geo --maxfail=1 2>/dev/null || echo "run after T08 creates file"
```
