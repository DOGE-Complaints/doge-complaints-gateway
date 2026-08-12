## Task workspace — `task-m2-02-12-t06-intake-transparency-acceptance-tests`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §4

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~2 h  
**Status:** ready  
**Wave:** `pkg-000026`  
**Depends on:** T01–T05  
---

## Task: tests — REQ-46 acceptance (geo, intake_notes, logging)

### Цель
Закрыть AC REQ-46 §4 через automated tests: geo aliases, `intake_notes` in 202, logging levels/messages.

### AC/DoD (REQ-46 §4)
- [ ] (P0) Geo cases: Таллин, Kalamaja, Tartu/Тарту, Нарва, empty query (REQ §4 Geo expansion).
- [ ] (P0) Response: `data.intake_notes.geo_resolved` / `gpt_signals_persisted` for scenarios in REQ §4 intake_notes.
- [ ] (P0) No `gpt_signals` → `gpt_signals_persisted: true`.
- [ ] (P0) Simulated persist failure → `gpt_signals_persisted: false`.
- [ ] (P1) Logging: caplog/capsys asserts for `intake.geo_not_resolved` INFO and `intake.gpt_signals_drop` WARNING where applicable.
- [ ] (P0) Full unit suite (excl. smoke/integration if project convention): no regressions.

### Где менять
- Prefer: `tests/test_req46_intake_transparency.py` (new) or extend [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py), [`tests/test_gpt_signals_intake.py`](../../../../../../../tests/test_gpt_signals_intake.py).
- Geo unit tests may live with T01 module.

### Out of scope
- Smoke / live Railway (REQ-47).
- Title hint migration (T07).

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_req46_intake_transparency.py
python3 -m pytest -q --ignore=tests/smoke --ignore=tests/integration
```
