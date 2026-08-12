# Acceptance verification — GW-DRAFT-07 T04

- **Task:** task-gw-draft-07-t04-verify-ready-schema-db-ready
- **Result:** PASS
- **Date:** 2026-08-06T21:17:51Z

## Evidence

`GET https://dogestonia-tallinn.up.railway.app/ready` (post-redeploy `66629cac-…`):

```json
{
  "data": {
    "status": "ready",
    "db": {
      "backend": "supabase",
      "ready": true,
      "checks": {
        "connectivity": true,
        "schema": true,
        "columns": true,
        "columns_geo_admin": true,
        "columns_v2": true,
        "policy_probe": true
      }
    }
  },
  "trace_id": "e4c75f0f-7dda-41d3-b055-96ba790b12cb"
}
```

- `db.ready`: **true**
- `checks.schema`: **true**
- Traces parent AC #1
