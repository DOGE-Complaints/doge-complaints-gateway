## Task workspace — `task-m2-17-02-t05-req38-acceptance-tests`

- Story: [`../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md`](../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md)
- Decision Ref: REQ-38 §5 (all AC)

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000017`  
---

## Task: tests — REQ-38 acceptance matrix

### Цель
Закрыть REQ-38 §5: consolidated regression pack + story gate artifacts (`story-acceptance-gate-STORY-M2-17-02.md`, run-summary).

### Факты из кода
1. Нет [`tests/test_req38_data_integrity.py`](../../../../../../../tests/test_req38_data_integrity.py) (planned).
2. T01–T04 deliver partial coverage; T05 aggregates AC matrix and full `pytest -q`.
3. Audit baseline: 283 passed, 10 skipped (2026-05-17).

### Gap / Проблема
Нет единого регрессионного пакета и story-level gate doc для REQ-38 end-to-end acceptance.

### AC/DoD
- [ ] (P0) `tests/test_req38_data_integrity.py` (or documented re-export of T01/T04 tests) covers §5 checklist.
- [ ] (P0) G-10: extend file passes in_memory.
- [ ] (P0) G-11: index + lookup tests green.
- [ ] (P0) G-12: `validate_arweave_txid` three cases from REQ §5.
- [ ] (P0) `python3 -m pytest -q` green.
- [ ] (P1) `story-acceptance-gate-STORY-M2-17-02.md` PASS; optional `run-summary-*-req38-*.md`.

### Где менять код
- **Создать:** [`tests/test_req38_data_integrity.py`](../../../../../../../tests/test_req38_data_integrity.py)
- **Создать:** [`../story-acceptance-gate-STORY-M2-17-02.md`](../story-acceptance-gate-STORY-M2-17-02.md) (at story gate)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req38_data_integrity.py tests/test_living_issues_extend_existing.py -q --tb=short
cd doge-complaints-gateway && python3 -m pytest -q
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
```
