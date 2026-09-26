# Story acceptance gate — STORY-GW-THR-03

- **Story:** Civic gate: identity_verified only (no phone hard-code)
- **Package:** `pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml`
- **Result:** PASS
- **Date:** 2026-09-21T21:05:11Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-THR03-01: ALLOW only when opaque `identity_verified` true | PASS | `verification_gate.py`; `test_gate_allow_only_opaque_true` |
| AC-GW-THR03-02: phone-only stub must not allow | PASS | `test_gate_phone_only_stub_must_not_allow`; gauth_03 phone-only branch |
| AC-GW-THR03-03: inactive → UNAUTHORIZED; missing/false opaque → VERIFICATION_REQUIRED | PASS | `test_gate_inactive_unauthorized`; `test_gate_missing_or_false_opaque_verification_required` |
| AC-GW-THR03-04: cutover evidence; ignore legacy method flags for allow | PASS | `task-gw-thr-03-t04-cutover-evidence/cutover-evidence.md`; gate ignores `phone_verified` |

## Commands (live verification — P3)

```text
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
utc_now: 2026-09-21T21:05:11Z
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_thr_03_civic_gate_identity_verified.py tests/test_gw_gauth_03_verification_gate_contract.py
→ 9 passed
§Актуальная точка not rewritten; no invent public auth route; no phone dual-read
```
