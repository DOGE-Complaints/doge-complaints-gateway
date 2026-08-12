# Acceptance verification — TASK-M2-02-12-T11

- **Task:** purge legacy-hint test stories + DROP `narrative_title_hint*` columns
- **Result:** Pass (data purge + repo migration); DROP on hosted pending SQL Editor / `psql` password
- **Preflight (2026-06-03):** PostgREST `content-range` **0-0/192** legacy-hint stories on `lvfrdtglpksmaywqlohj`
- **Purge applied (2026-06-03):** service-role PostgREST deletes — **192** stories, **5** issues (any_link), **3** candidates; post-purge hint count **0** (`*/0`)
- **Repo:** `supabase/migrations/20260603_1200_req46_title_hint_test_purge_and_column_drop.sql` (BEGIN/COMMIT, any_link, post-purge gate, DROP)
- **Hosted DROP:** columns still selectable (`narrative_title_hint` nullable) — run `ALTER TABLE … DROP COLUMN` block from migration file in SQL Editor (purge steps already executed; safe to run DROP-only)
- **Deploy order:** T12/T13 code deployed after data purge (2026-06-03)
