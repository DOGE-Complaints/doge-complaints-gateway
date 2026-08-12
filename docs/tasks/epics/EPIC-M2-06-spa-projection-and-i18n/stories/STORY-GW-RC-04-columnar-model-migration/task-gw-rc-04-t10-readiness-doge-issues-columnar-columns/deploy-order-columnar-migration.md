# Deploy order — GW-RC-04 columnar migration (audit G1)

Hosted Supabase **must** have columnar schema before gateway code that reads `COLUMNAR_ROW_SELECT` is deployed.

## Required migration order

1. `supabase/migrations/20260619_1200_gw_rc_04_doge_issues_columnar_columns.sql` — add columnar columns
2. `supabase/migrations/20260619_1210_gw_rc_04_issues_dashboard_columnar.sql` — rewrite view (optional for API, required for SPA direct-read)
3. `supabase/migrations/20260619_1220_gw_rc_04_backfill_drop_payload_json.sql` — backfill + DROP `payload_json`

Then deploy gateway application code.

## Readiness signal

After deploy, `/ready` with `db_backend=supabase` checks `doge_issues` columnar columns via `required_columns_ready()` (GW-RC-04 T10).

## Rollback note

After step 3, `payload_json` is dropped — rollback to pre-columnar code without matching DB restore is not supported.
