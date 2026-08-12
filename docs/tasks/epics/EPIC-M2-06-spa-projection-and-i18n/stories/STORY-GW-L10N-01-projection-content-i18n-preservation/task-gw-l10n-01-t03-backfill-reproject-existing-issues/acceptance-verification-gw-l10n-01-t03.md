# Acceptance — TASK-GW-L10N-01-T03

- **Result:** PASS
- **Date:** 2026-06-15

| AC | Status | Evidence |
|----|--------|----------|
| one-off reproject script | PASS | `doge-complaints-gateway/scripts/reproject_issue_i18n.py` |
| dry-run mode | PASS | `--dry-run` flag |
| run order note | PASS | script module docstring |

Run after deploy:
```bash
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --dry-run
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py
```
