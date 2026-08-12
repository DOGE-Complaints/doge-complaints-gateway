# Hosted readiness checklist — T01

**Date:** 2026-06-21  
**Target:** `https://dogestonia-tallinn.up.railway.app`

| Check | Status | Evidence |
|-------|--------|----------|
| `GET /ready` → `db.ready=true` | PASS | [`hosted-ready-response.json`](./hosted-ready-response.json) |
| `db.backend=supabase` | PASS | same artifact |
| Columnar columns (`db.checks.columns=true`) | PASS | RC-04 migrations already applied; no 1200/1210/1220 apply needed |
| `DB_BACKEND=supabase` on Railway | PASS | inferred from `/ready` backend field |
| `CLUSTER_CRON_ENABLED=true` | PASS (R1) | Code default `true` ([`schema.py:216-218`](../../../../../../../src/core/config/schema.py#L216-L218)); Railway env var not queried in P3 — operator should confirm in Railway Variables if clustering stalls |

**Migrations skipped:** `/ready` green with `columns=true` before loader runs.
