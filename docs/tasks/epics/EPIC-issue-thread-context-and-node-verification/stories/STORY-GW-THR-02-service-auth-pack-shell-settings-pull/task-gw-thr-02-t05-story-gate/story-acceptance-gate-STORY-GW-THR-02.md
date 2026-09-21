# Story acceptance gate — STORY-GW-THR-02

- **Story:** Service-auth active pack shell settings pull
- **Package:** `pkg-000094-20260921-gw-thr-02-service-auth-pack-shell-settings-pull.yaml`
- **Result:** PASS
- **Date:** 2026-09-21T20:48:13Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-THR02-01: service-auth pull returns verification + shell knobs for active pair | PASS | `GET /node/shell-settings` → `pack_shell_settings`; `test_shell_settings_happy_path_returns_capabilities` |
| AC-GW-THR02-02: no new public ThreadContext route; service-auth class | PASS | path not in `PUBLIC_ROUTES`; `require_public_content_service_auth`; `test_shell_settings_requires_service_auth` / wrong token 401 |
| AC-GW-THR02-03: no Story narrative bodies in settings | PASS | `assert_no_story_narrative`; happy-path blob bans story_body/original_text/thread_context |
| AC-GW-THR02-04: incomplete pack → fail-closed | PASS | `test_incomplete_pack_fail_closed` / `test_missing_sidecar_fail_closed` |
| AC-GW-THR02-05: public Issue get remains civic projection | PASS | `handlers.py` issue get unchanged; `test_public_issue_get_remains_civic_projection` |

## Commands (live verification — P3)

```text
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
→ ok 5 paths (pkg-000094)
utc_now: 2026-09-21T20:48:13Z
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_thr_01_pack_shell_required.py tests/test_gw_thr_02_settings_pull.py
→ 16 passed
HTTP path chosen (implement-wave): GET /node/shell-settings
§Актуальная точка not rewritten; no public ThreadContext route
```
