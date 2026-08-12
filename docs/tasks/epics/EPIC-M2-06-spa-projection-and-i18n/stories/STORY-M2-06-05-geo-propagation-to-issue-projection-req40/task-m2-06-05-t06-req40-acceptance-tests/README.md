## Task workspace — `task-m2-06-05-t06-req40-acceptance-tests`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §7; REQ-40 AC-1..AC-4

---
**Приоритет:** P2  
**Сложность:** M  
**Оценка времени:** 2–3 ч  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: tests — REQ-40 geo propagation acceptance

### Цель
Добавить `tests/test_req40_geo_propagation.py` с покрытием AC-1..AC-4 и story gate evidence.

### Факты из кода
1. REQ-40 §7 AC-1 — intake с `location_query` → issue payload `geo` с lat/lon/admin fields.
2. AC-2 — без location_query → ключ `geo` отсутствует.
3. AC-3 — cluster 2 stories, разный geo → payload geo = доминантная (alpha_score).
4. AC-4 — issues без geo не ломают read contract (backward compat).
5. Существующие e2e: [`tests/test_e2e_story_cluster_issue_pipeline.py`](../../../../../../../tests/test_e2e_story_cluster_issue_pipeline.py) — переиспользовать fixtures/patterns где возможно.

### Gap / Проблема
Нет dedicated REQ-40 acceptance file; story gate blocked без T01–T05.

### AC/DoD
- [ ] (P0) Создать `tests/test_req40_geo_propagation.py`.
- [ ] (P0) AC-1: geo present in stored projection payload after promote.
- [ ] (P0) AC-2: no `geo` key when story has no geo.
- [ ] (P0) AC-3: dominant story geo wins in 2-story cluster.
- [ ] (P1) AC-4: read/load issue without geo field — no error.
- [ ] (P0) `python3 -m pytest tests/test_req40_geo_propagation.py -q` green.
- [ ] (P0) Story gate `story-acceptance-gate-STORY-M2-06-05.md` — PASS after full suite.

### Где менять код
- **Создать:** [`tests/test_req40_geo_propagation.py`](../../../../../../../tests/test_req40_geo_propagation.py)
- **Артефакты:** `acceptance-verification-m2-06-05-t06.md`, `BULLRUN-PHASE-LOG.md` (this folder)

### Out of scope
- REQ-24 bbox/district HTTP filters
- Postal code Phase 3

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req40_geo_propagation.py -q --tb=short
cd doge-complaints-gateway && python3 -m pytest -q --tb=no
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
```
