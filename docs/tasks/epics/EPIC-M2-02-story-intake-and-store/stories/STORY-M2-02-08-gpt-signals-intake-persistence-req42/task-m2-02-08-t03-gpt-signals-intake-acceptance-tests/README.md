## Task workspace — `task-m2-02-08-t03-gpt-signals-intake-acceptance-tests`

- Story: [`../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md`](../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md)
- Decision Ref: [`../../../../../../requirements/42-gpt-signals-story-intake-extension.md`](../../../../../../requirements/42-gpt-signals-story-intake-extension.md) §5

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
---

## Task: tests — REQ-42 acceptance for gpt_signals intake

### Цель
Закрыть REQ-42 §5 automated: HTTP 202/400, sqlite `story_signals` roundtrip, idempotency, non-blocking signals error.

### Факты из кода
1. [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py) L54 — intake HTTP **202** (не 200).
2. [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py) — `valid_v2_intake_payload()`.
3. [`tests/test_story_signal_store.py`](../../../../../../../tests/test_story_signal_store.py) — sqlite roundtrip для `save_signals`.
4. [`tests/test_integration_cross_layer_api_app_infra.py`](../../../../../../../tests/test_integration_cross_layer_api_app_infra.py) L68 — invalid payload → 400.

### Gap / Проблема
Нет regression suite для gpt_signals wire path end-to-end.

### AC/DoD
- [ ] (P0) `tests/test_gpt_signals_intake.py` (new): valid `gpt_signals` → 202 + sqlite row `extraction_policy='gpt.story_classifier.v1'` + JSON fields.
- [ ] (P0) Payload без `gpt_signals` → 202, нет строки для `gpt.story_classifier.v1`.
- [ ] (P0) `gpt_signals.severity: "INVALID"` → 400.
- [ ] (P0) Idempotency: повторный POST с тем же key → тот же `story_id`, одна signals row (upsert).
- [ ] (P1) Mock/fake store raise on `save_signals` → response still 202 (non-blocking).
- [ ] (P1) Reuse `TestClient` + `_clear_api_dependencies_cache` pattern from [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py).

### Где менять код
- `tests/test_gpt_signals_intake.py` (new)

### Out of scope
- Live Supabase tests.
- Clustering using gpt_signals.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gpt_signals_intake.py
```
