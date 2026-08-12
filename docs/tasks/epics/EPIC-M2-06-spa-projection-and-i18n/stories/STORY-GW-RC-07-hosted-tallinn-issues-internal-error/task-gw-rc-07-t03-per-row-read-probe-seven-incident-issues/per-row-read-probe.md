# Per-row read probe — STORY-GW-RC-07 T03

**Date:** 2026-07-10

## Method

1. `GET /tallinn/issues` — enumerate all PUBLISHED rows (hosted).
2. `GET /tallinn/issues/{id}` — per-row isolated read for each id.

## List probe (hosted)

trace_id: `2bb6aaab-a340-492c-893a-af16c03c57cf`  
Count: **9** PUBLISHED

| # | issue_id | type | status | GET /{id} |
|---|----------|------|--------|-----------|
| 1 | `b549b663-ffaf-4840-a19b-56327fd12dff` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 2 | `06a0a818-6ac6-44a1-a419-4ca95258f007` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 3 | `bdc01a24-62ac-4498-88d3-9ca22cc18abd` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 4 | `fe389169-3d03-46a3-8f96-de5d7f133936` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 5 | `d75c3f76-9c8d-4e2d-91d8-fc0d33cd3228` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 6 | `345b6bf9-0037-4c9f-bcfa-20e2e648e6ca` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 7 | `3d50b062-6565-4fbf-877a-f29947d79d8f` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 8 | `d7810f2f-b951-4445-83c0-42ab13f00848` | INCIDENT | PUBLISHED | HTTP 200 OK |
| 9 | `test-7ef193be-dc51-4ddb-a582-24a6977dfd51` | IMPROVEMENT | PUBLISHED | HTTP 200 OK |

## Local read-path tests

```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py  # 26 passed (incl. gw_rc_03)
```

## Isolation conclusion (parent AC #2 — isolation leg)

- **No failing row** among 9 PUBLISHED issues on hosted (2026-07-10).
- Historical CF-B was **not** attributable to a single poisoned DB row at probe time.
- Root cause class: **deploy/runtime** (missing `columnar_storage` on hosted build per T02), not per-row payload corruption.
