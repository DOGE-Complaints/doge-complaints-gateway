# Acceptance verification — TASK-M2-02-12-T09

- **Task:** test `save_signals` exception → `gpt_signals_persisted: false` + WARNING.
- **Result:** PASS
- **Evidence:** `tests/test_req46_intake_transparency.py::test_intake_notes_gpt_signals_persist_failed_when_save_raises`.
- **Commands:** `python3 -m pytest -q tests/test_req46_intake_transparency.py::test_intake_notes_gpt_signals_persist_failed_when_save_raises`
