# Story acceptance gate — STORY-M2-02-08

- **Story:** GPT signals intake → story_signals (REQ-42)
- **Package:** `pkg-000022-20260522-req42-gpt-signals-story-intake.yaml`
- **Result:** PASS
- **Date:** 2026-05-22

## AC checklist (REQ-42 §5)

| AC | Status | Evidence |
|----|--------|----------|
| Intake with valid `gpt_signals` → HTTP 202 | PASS | `test_intake_with_gpt_signals_returns_202_and_persists_sqlite` |
| `story_signals` row with `gpt.story_classifier.v1` | PASS | sqlite `get_signals` assertion |
| Intake without `gpt_signals` → no policy row | PASS | `test_intake_without_gpt_signals_no_classifier_row` |
| Invalid enum → HTTP 400 | PASS | `test_intake_invalid_gpt_signals_severity_returns_400` |
| Signals persist failure does not block 202 | PASS | `test_intake_gpt_signals_persist_failure_still_returns_202` |
| Runtime docs + OpenAPI v2 + GptSignals | PASS | T04 + `test_openapi_runtime_compliance.py` |

## Verification command

```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gpt_signals_intake.py
```

| Empty `gpt_signals: {}` → no policy row | PASS | `test_intake_empty_gpt_signals_object_no_classifier_row` |

**Outcome:** 10 passed (2026-05-23 re-validation).
