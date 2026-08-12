# Backend handoff — FE contract guarantee (GW-RC-03 T04)

**Date:** 2026-05-29  
**Audience:** spa-app team  
**Story:** STORY-GW-RC-03 / D-RC-4

## What the backend guarantees (read path)

For `GET /tallinn/issues` and `GET /tallinn/issues/{id}`, each issue object **always** includes:

| Field | Guarantee |
|-------|-----------|
| `id` | From DB column `issue_id` (column-as-truth, RC-01) |
| `status` | From DB column `status` (RC-01) |
| `type` | Canonical UPPERCASE enum (`IMPROVEMENT`, `SERVICE_REQUEST`, `INCIDENT`) even when legacy payload stored lowercase (RC-02) |
| `created_at` | From DB column (RC-01 / audit T07) |
| `labels`, `title`, `summary`, `description` | From payload (required contract keys per REQ-24) |

Regression coverage: [`tests/test_gw_rc_03_contract_guarantee.py`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py) — seeds incomplete legacy payload (no `id`/`status`, lowercase `type`) and asserts valid list/get response.

## Optional fields (data-only, not guaranteed for legacy rows)

`institution`, `geo`, `original_locale`, `arweave_txid`, `image_txid`, `image_hash` — present when stored in payload; legacy rows may omit them until re-project. See [`legacy-audit-five-records.md`](../task-gw-rc-03-t02-legacy-sql-audit-five-live-records/legacy-audit-five-records.md).

## FE action (out of scope for gateway)

- Enable `assertIssue` / contract tests on the gateway read path when ready.
- Live contract script: `npm run test:contract:live` in spa-app should pass once deployed with RC-01/02/03.

## References

- [`interview-issues-read-contract-2026-06-19.md`](../../../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) — D-RC-4
- [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) — issues read endpoints
