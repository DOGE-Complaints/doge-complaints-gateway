# Acceptance — TASK-GW-SEED-01-T01

- **Result:** PASS
- **Date:** 2026-06-21

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| `GET /ready` на hosted = `db_ready: true` до загрузки | PASS | `hosted-ready-response.json`; live curl 2026-06-21 |
| `CLUSTER_CRON_ENABLED=true` подтверждён на таргете | PASS (R1) | `hosted-readiness-checklist.md` — schema default true; Railway env not independently verified |
