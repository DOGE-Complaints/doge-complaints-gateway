# Acceptance verification — TASK-M2-02-08-T01

- **Task:** intake contract `gpt_signals` block
- **Result:** PASS
- **Date:** 2026-05-22
- **Evidence:** `pytest tests/test_gpt_signals_intake.py -k parse -q` → 3 passed; `GptSignalsBlock` + `StoryIntakeRequest.gpt_signals` in `src/core/intake/contracts.py`
