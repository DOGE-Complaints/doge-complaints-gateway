# BULLRUN — TASK-M2-02-12-T07

- [ ] SQL gate on production Supabase (`COUNT(*) WHERE narrative_title_hint* IS NOT NULL`) — **not run in this P3 window**
- [ ] Migration DROP columns — deferred
- [ ] `db_supabase.py` / `db_sqlite.py` cleanup — deferred

**Reason:** REQ §2.4 requires verified `0` rows on live `stories` before DROP; operator must run gate on Supabase, then re-open T07.
