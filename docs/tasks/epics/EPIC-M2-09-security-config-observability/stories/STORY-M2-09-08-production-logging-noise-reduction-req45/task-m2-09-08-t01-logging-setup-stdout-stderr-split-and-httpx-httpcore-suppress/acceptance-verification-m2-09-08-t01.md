# Acceptance verification — TASK-M2-09-08-T01

- **Task:** stdout/stderr split + suppress noisy transport loggers.
- **Result:** PASS
- **Evidence (code):**
  - `src/core/logging_setup.py` — `import sys`, `_LevelBelowWarningFilter`, `stdout_handler`, `stderr_handler`.
  - `src/core/logging_setup.py` — `logging.getLogger("httpx").setLevel(logging.WARNING)`.
  - `src/core/logging_setup.py` — `logging.getLogger("httpcore").setLevel(logging.WARNING)`.
- **Commands:**
  - `cd "/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway" && python3 -m pytest tests/test_logging_setup.py tests/test_req37_pipeline_observability_pii.py -q`
- **Output:** `11 passed in 0.25s`
