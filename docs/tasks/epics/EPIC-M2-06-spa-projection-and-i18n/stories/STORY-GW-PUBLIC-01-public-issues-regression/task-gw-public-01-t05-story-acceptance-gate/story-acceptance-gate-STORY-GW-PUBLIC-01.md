# Story acceptance gate — STORY-GW-PUBLIC-01

- **Story:** Регресс-гарантия публичности issues (M-5)
- **Package:** `pkg-000048-20260710-gw-public-01-public-issues-regression.yaml`
- **Result:** PASS
- **Date:** 2026-07-10

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| T01–T02: read routes публичны | PASS | T01–T02 acceptance; `test_gw_public_01_public_issues_regression.py` |
| T03–T04: write routes закрыты без service auth | PASS | T03–T04 acceptance; contrast on story-drafts + tallinn/issues |
| Тесты в offline-сюите (без сети), зелёные | PASS | 568 passed `-m "not live_integration"`; module 5/5 |

## Commands (offline verification 2026-07-10)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
