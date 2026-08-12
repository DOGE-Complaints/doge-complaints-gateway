# Story acceptance gate — STORY-GW-RC-07

- **Story:** Hosted `/tallinn/issues` INTERNAL_ERROR regression (CF-B)
- **Package:** `pkg-000047-20260710-gw-rc-07-hosted-tallinn-issues-internal-error.yaml`
- **Result:** PASS
- **Date:** 2026-07-10

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `hosted-internal-error-evidence.md`: воспроизведение CF-B задокументировано. | PASS | T01 [`hosted-internal-error-evidence.md`](../task-gw-rc-07-t01-reproduce-and-collect-hosted-evidence/hosted-internal-error-evidence.md) |
| Root cause изолирован (T03) и исправлен (T04). | PASS | T03 [`per-row-read-probe.md`](../task-gw-rc-07-t03-per-row-read-probe-seven-incident-issues/per-row-read-probe.md); T04 [`fix-summary.md`](../task-gw-rc-07-t04-fix-hosted-read-path-root-cause/fix-summary.md) |
| Hosted `GET /tallinn/issues` отдаёт валидные карточки (не `INTERNAL_ERROR`). | PASS | Live curl 9 cards; [`tallinn-issues-live-response-2026-07-10.json`](./tallinn-issues-live-response-2026-07-10.json) |
| SEED-03 разблокирован для board-fill verify. | PASS | CF-B closed; bullrun SEED-03 hosted leg unblocked |

## Commands (live verification 2026-07-10)

```bash
curl -sS "https://dogestonia-tallinn.up.railway.app/tallinn/issues"
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
