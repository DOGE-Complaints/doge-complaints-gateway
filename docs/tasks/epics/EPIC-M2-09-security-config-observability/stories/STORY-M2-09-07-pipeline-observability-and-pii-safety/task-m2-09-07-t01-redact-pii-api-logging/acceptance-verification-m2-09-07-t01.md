# Acceptance verification — TASK-M2-09-07-T01

- **Task:** `redact_pii()` for narrative fields
- **Result:** PASS
- **Evidence:** `src/core/redaction.py`; `from core.api.logging import redact_pii` re-export; REQ-37 §2.2
- **Commands:** `python3 -c "from core.api.logging import redact_pii; assert redact_pii('x', True)=='[REDACTED]'"`
