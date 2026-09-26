# Story acceptance gate — STORY-GW-REQ9-01

- **Story:** example.env peer URLs + SPA_BASE_URL hard cut
- **Package:** `pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml`
- **Result:** PASS
- **Date:** 2026-09-26T12:06:30Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ901-01: `example.env` contains `IDENTITY_BASE_URL` + local `:8100` comment | PASS | `example.env` T01 |
| AC-GW-REQ901-02: `example.env` contains `API_BASE_URL` | PASS | `example.env` T01 |
| AC-GW-REQ901-03: Configured name `SPA_BASE_URL`; schema/helpers `spa_base_url`; no primary `SPA_VERIFY_*` | PASS | `schema.py`, `verify_url.py`, `identity/__init__.py`; `rg` src=0 |
| AC-GW-REQ901-04: `example.env` documents `SPA_BASE_URL`; `SERVICE_API_TOKEN` retained | PASS | `example.env` |
| AC-GW-REQ901-05: tests/docs do not treat `SPA_VERIFY_BASE_URL` as primary | PASS | tests + `docs/runtime-docs/**`; local `.env` renamed |

## Commands (live verification — P3)

```text
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
→ ok 5 paths (pkg-000096)
--verify --check-dates → ok date-check
utc_now: 2026-09-26T12:06:30Z
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_gauth_03_verification_gate_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
→ 10 passed
Hard cut only — no SPA_VERIFY dual-read; no invent Railway service ids; §Актуальная точка not rewritten; make test OUT (REQ9-02)
```
