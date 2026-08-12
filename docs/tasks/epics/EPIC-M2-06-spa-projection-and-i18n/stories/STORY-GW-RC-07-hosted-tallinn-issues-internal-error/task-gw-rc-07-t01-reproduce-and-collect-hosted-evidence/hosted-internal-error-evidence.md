# Hosted INTERNAL_ERROR evidence — CF-B (STORY-GW-RC-07 T01)

**Date:** 2026-07-10  
**Verifier:** P3 execute (`run-summary-20260710-1028-gw-rc-07-p3`)

## Historical reproduction (audit 2026-06-22)

Source: [`audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §CF-B.

| Field | Value |
|-------|-------|
| Endpoint | `GET https://dogestonia-tallinn.up.railway.app/tallinn/issues` |
| HTTP status | 200 |
| Body | `{"error":{"code":"INTERNAL_ERROR",...}}` |
| trace_id (audit) | `d7581fb1-…` |
| DB state | 8 PUBLISHED rows (7 INCIDENT + legacy `test-7ef193be`) |
| `/ready` | green (schema + columns checks PASS) |

## Live re-verify (2026-07-10T10:28Z)

```bash
curl -sS "https://dogestonia-tallinn.up.railway.app/tallinn/issues"
curl -sS "https://dogestonia-tallinn.up.railway.app/ready"
```

| Field | Value |
|-------|-------|
| HTTP status | 200 |
| Body shape | `{"data":{"issues":[...]},"trace_id":"..."}` — **success envelope** |
| trace_id | `c4e19652-503b-4283-a488-1910c51cf9cc` |
| Issue count | **9** (8 INCIDENT + 1 IMPROVEMENT legacy) |
| `/ready` trace_id | `91b24844-a008-4206-a4ba-5544a78c08ec` |
| `/ready` db.checks | connectivity, schema, columns, columns_geo_admin, **columns_v2**, policy_probe — all `true` |

## Conclusion

- CF-B **reproduced historically** per audit §CF-B (INTERNAL_ERROR with 8 rows).
- **Current prod state (2026-07-10):** regression **not present** — list returns valid issue cards.
- T01 scope satisfied: reproduction documented + live re-verify captured.
