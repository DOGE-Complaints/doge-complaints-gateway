## Task workspace — `task-m2-06-06-t10-audit-gap24-b-filter-edge-ac-tests`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: [`../../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md`](../../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md) §6 GAP-B; REQ-24 AC-15, AC-17, AC-18, AC-19

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** ~2–3 ч  
**Статус:** done  
**Wave:** audit override (`run_mode=story06_06_audit_req24_followup`)  
---

## Task: tests — filter edge cases AC-15/17/18/19

### Цель
Формально покрыть acceptance criteria, где логика уже реализована в [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py), но отсутствуют dedicated тесты (audit GAP-B).

### Почему это важно (риск)
Без тестов регрессии в geo/temporal фильтрах не ловятся; AC формально остаются «логика верна, тест отсутствует».

### Факты из кода
1. [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py) — `_matches_geo_filters()`: geo-less exclusion (AC-15), OR district (AC-17), sequential AND bbox+address (AC-18).
2. `filter_projection_rows()` — `created_after` / `created_before` ISO string compare (AC-19).
3. Существующие паттерны: [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py) — `_app_story_repository()`, `process_all_pending()`, direct `save_projection` where needed.

### Gap / Проблема
**AUDIT-GAP-24-B:** нет тестов для AC-15, AC-17, AC-18, AC-19.

### AC/DoD
- [ ] (P0) `test_req24_ac15_geo_less_excluded_when_bbox_active` — issue без `geo` + активный `geo_lat_min` → не в списке.
- [ ] (P0) `test_req24_ac17_geo_district_multi_value_or` — `?geo_district=a&geo_district=b`, OR-семантика.
- [ ] (P0) `test_req24_ac18_bbox_and_district_and` — bbox + district; оба условия должны совпасть.
- [ ] (P0) `test_req24_ac19_created_after_before` — seed с известным `created_at`; фильтры `created_after` / `created_before`.
- [ ] (P1) `acceptance-verification-m2-06-06-t10.md` + `BULLRUN-PHASE-LOG.md`.
- [ ] (P1) Не менять runtime filter logic, если тесты green без правок (только тесты).

### Где менять код
- [`tests/test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py) (preferred)
- Опционально: `tests/test_req24_filter_edge_cases.py` (если основной файл раздувается)

### Out of scope
- Изменения `read_filters.py` (unless test failure proves bug)
- OpenAPI / HTTP routes
- `pkg-000019` YAML

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q -k 'ac15 or ac17 or ac18 or ac19'
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q
```
