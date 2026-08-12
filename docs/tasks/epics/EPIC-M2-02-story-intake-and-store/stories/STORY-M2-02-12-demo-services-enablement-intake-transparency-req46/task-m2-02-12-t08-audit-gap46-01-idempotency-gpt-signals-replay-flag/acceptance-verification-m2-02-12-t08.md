# Acceptance verification — TASK-M2-02-12-T08

- **Task:** idempotent replay `gpt_signals_persisted` from signal store.
- **Result:** PASS
- **Evidence:** `src/core/application/services.py` (`_gpt_signals_persisted_on_replay`, idempotent return); `tests/test_req46_intake_transparency.py::test_idempotent_replay_gpt_signals_persisted_true_when_signals_stored`.
- **Commands:** `python3 -m pytest -q tests/test_req46_intake_transparency.py::test_idempotent_replay_gpt_signals_persisted_true_when_signals_stored`
