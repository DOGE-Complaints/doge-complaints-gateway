# Story acceptance gate — STORY-GW-RC-06

- **Story:** Гигиена hosted-данных: status-миграция + пустой контент (S1)
- **Package:** `pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml`
- **Result:** PASS
- **Date:** 2026-06-20

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| На hosted нет `doge_issues.status='promoted'` (все board-vocab). | PASS | T01 `post-migrate-status-check.md`; T04 curl — 0 promoted |
| Записи с пустым контентом либо ре-проджектнуты, либо явно помечены как test-seed/удалены. | PASS | T02 audit (0 recoverable); T03 `test-seed-disposition-decision.json` — delete 4 empty test-* |
| `GET /tallinn/issues` отдаёт валидные карточки; доска не пустая. | PASS | T04 `curl-verify-summary.md`, `tallinn-issues-live-response.json` |

## Commands (live verification — P3/P6 only)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
curl -s http://127.0.0.1:8000/tallinn/issues
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
