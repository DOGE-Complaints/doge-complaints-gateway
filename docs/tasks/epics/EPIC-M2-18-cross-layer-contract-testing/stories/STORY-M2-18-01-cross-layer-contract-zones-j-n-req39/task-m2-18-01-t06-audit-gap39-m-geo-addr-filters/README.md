## Task workspace — `task-m2-18-01-t06-audit-gap39-m-geo-addr-filters`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-M-GEO-ADDR; [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) Zone M

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~30 мин  
**Статус:** ready  
**Wave:** audit override (`run_mode=story18_audit_req39_followup`)  
---

## Task: tests — Zone M geo-address filter coverage (settlement/region/country/postal_code)

### Цель
Добавить 4 contract-теста для гео-адресных фильтров в `filter_projection_rows()`, не покрытых текущими M-06..M-08 (bbox + district only).

### Почему это важно (риск)
`_matches_geo_filters()` в `read_filters.py` обрабатывает 9 параметров; без тестов на `geo_settlement`, `geo_region`, `geo_country`, `geo_postal_code` регрессия в ключах `geo` dict не будет поймана.

### Факты из кода
1. [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py) — `_matches_geo_filters()` ~L55–131: settlement/region/country/postal_code используют ту же OR-логику, что и district.
2. [`test_filter_projection_rows_contract.py`](../../../../../../../tests/test_filter_projection_rows_contract.py) — M-06..M-08 покрывают bbox и `geo_district` only (аудит §6).
3. Аудит рекомендует порядок закрытия: **первый** в audit follow-up wave.

### Gap / Проблема
**AUDIT-GAP-39-M-GEO-ADDR:** 4 фильтра без dedicated tests.

### AC/DoD
- [ ] (P0) `test_m09_geo_settlement_filter_or_semantics` — OR по `geo_settlement`.
- [ ] (P0) `test_m10_geo_region_filter` — `geo_region`.
- [ ] (P0) `test_m11_geo_country_filter` — `geo_country`.
- [ ] (P0) `test_m12_geo_postal_code_filter` — `geo_postal_code`.
- [ ] (P1) Опционально: явный import `normalize_geo_token` из `core.projection.read_filters` (подпункт GAP-39-M-IMPORT в аудите Zone M) — без смены поведения.

### Где менять код
- [`tests/test_filter_projection_rows_contract.py`](../../../../../../../tests/test_filter_projection_rows_contract.py)

### Out of scope
- Изменение `read_filters.py` (только тесты, если логика уже верна).
- `pkg-000020` YAML; HTTP/store SQL paths.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_filter_projection_rows_contract.py -k 'm09 or m10 or m11 or m12'
```
