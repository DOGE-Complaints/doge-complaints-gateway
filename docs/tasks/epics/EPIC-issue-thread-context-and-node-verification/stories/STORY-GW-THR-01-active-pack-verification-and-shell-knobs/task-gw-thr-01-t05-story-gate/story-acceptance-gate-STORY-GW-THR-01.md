# Story acceptance gate — STORY-GW-THR-01

- **Story:** Active pack verification policy + shell knobs
- **Package:** `pkg-000093-20260921-gw-thr-01-active-pack-verification-and-shell-knobs.yaml`
- **Result:** PASS
- **Date:** 2026-09-21T20:29:51Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-THR01-01: verification policy capabilities on active pack | PASS | sidecar entries `verification.validation_type` + `verification.integration_name`; uus=`phone`/`uus_phone_sms`; `test_warehouse_activatable_packs_resolve_with_shell_caps` |
| AC-GW-THR01-02: shell knobs capabilities on same pack | PASS | max_depth, reaction enables/max, Topic-guarded min_overlap, media allowlist in `shell_capabilities.json` |
| AC-GW-THR01-03: missing caps → fail-closed; no silent defaults | PASS | `test_missing_shell_sidecar_fail_closed`; `test_incomplete_capabilities_fail_closed_no_silent_defaults`; boot ConfigError with BOOT_SOFT=0 |
| AC-GW-THR01-04: no mandated concrete pack JSON key strings | PASS | caps in sidecar `shell_capabilities.json`; pack.json has no `threads`/`verification` blocks (`test_pack_json_has_no_invented_threads_key_block`) |
| AC-GW-THR01-05: activatable packs migrated; no legacy knobs-optional | PASS | all tracked warehouse packs have sidecar; resolve requires it |

## Commands (live verification — P3)

```text
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
→ ok 5 paths (pkg-000093)
utc_now: 2026-09-21T20:29:51Z
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_thr_01_*.py
→ 7 passed
§Актуальная точка not rewritten; no public ThreadContext route invented
```
