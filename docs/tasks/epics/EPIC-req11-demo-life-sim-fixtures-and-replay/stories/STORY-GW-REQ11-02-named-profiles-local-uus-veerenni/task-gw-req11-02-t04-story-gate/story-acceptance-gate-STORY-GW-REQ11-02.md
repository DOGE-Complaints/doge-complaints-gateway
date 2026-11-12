# Story acceptance gate — STORY-GW-REQ11-02

- **Story:** Named profiles: local + Uus Veerenni deploy
- **Package:** `pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml`
- **Result:** PASS
- **Date:** 2026-09-29T14:00:57Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1102-01: Profile `local` selectable with local-five URL/env refs (D3 / GW-11-03) | PASS | `tests/sandbox/profiles/local.json` + `index.json`; ports 8100/8000/8001/8080/5173; `select_profile("local")`; `test_ac01_*` |
| AC-GW-REQ1102-02: Profile Uus Veerenni deploy selectable with documented URL/env refs (D3) | PASS | `tests/sandbox/profiles/uus-veerenni.json`; `GATEWAY_URL` / `GATEWAY_API_TOKEN` env refs; documented_example_url from `.env.test.example`; `test_ac02_*` |
| AC-GW-REQ1102-03: Secrets stay in env; profile files only reference env names | PASS | `*_env` names only; `assert_no_secret_literals`; selection note [`note-gw-req11-02-profile-selection-2026-09-29.md`](../../../../../../analysis/note-gw-req11-02-profile-selection-2026-09-29.md); `test_ac03_*` |

## Commands (live verification 2026-09-29T14:00:57Z)

```text
--verify ok 4 (pkg-000101)
--verify --check-dates → ok date-check
.venv/bin/python -m pytest -q tests/test_gw_req11_02_named_profiles.py → 4 passed
utc_now: 2026-09-29T14:00:57Z
branch: dev
no fixtures/replay; no secrets in git; §Актуальная точка untouched
```
