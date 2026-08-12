# Acceptance — TASK-GW-L10N-01-T07

- **Result:** PASS
- **Date:** 2026-06-15

| AC | Status | Evidence |
|----|--------|----------|
| dry-run no write | PASS | `test_reproject_dry_run_does_not_mutate_payload` |
| write updates per-locale title | PASS | `test_reproject_write_updates_per_locale_title_from_dominant_story` |
| idempotent re-run | PASS | `test_reproject_write_is_idempotent` |
| type preserved | PASS | `test_reproject_write_updates_per_locale_title_from_dominant_story` |

```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_reproject_issue_i18n.py
```
