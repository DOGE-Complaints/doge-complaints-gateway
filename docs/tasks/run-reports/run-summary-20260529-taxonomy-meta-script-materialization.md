# Run summary — Taxonomy meta-script materialization (P1)

| Field | Value |
|-------|-------|
| Date | 2026-05-29 |
| Mode | P1 materialization (`Taxonomy_builder.plan.md` deliverables 1–5) |
| Scope | TC0–TC7 scaffolding: plan, CLI scripts, tests, bullrun, profiles verify |
| cycle_id | — (no operational cycle run; materialization only) |

## Delivered

- `.cursor/plans/Taxonomy_builder.plan.md` — TC0–TC7, hard rules, operator prompt
- `scripts/taxonomy_fetch_misses.py`, `taxonomy_classify_candidates.py`, `taxonomy_apply_gateway.py`, `taxonomy_apply_spa_i18n.py`
- `src/core/taxonomy/cycle_lib.py` — classify, YAML I/O, gateway patch helpers
- `docs/runtime-docs/appendix/taxonomy-decisions-schema.md`
- `docs/runtime-docs/appendix/taxonomy-update-process-ru.md` §3 — operator automation guide
- `docs/tasks/run-reports/taxonomy-cycles/README.md` — artifact layout
- `profiles.yaml` → `taxonomy` queueless profile; `builder_resolve_queue.py --project taxonomy --verify`

## TC7 gates (materialization)

| Check | Result |
|-------|--------|
| `builder_resolve_queue --project taxonomy --verify` | ok taxonomy verify (7 paths) |
| gateway unit `pytest -q --ignore=tests/smoke --ignore=tests/integration` | 477 passed |
| `test_supabase_required_tables.py` + `test_taxonomy_classify_candidates.py` | 17 passed |
| `spa-app npm test` | 76 passed |
| integration `test_supabase_dotenv_connectivity` | requires live `.env` + network (operator env) |

## Hard rules verified

- `label_translation_misses` ∉ `REQUIRED_READINESS_TABLES` — guard test green
- Taxonomy CLI scripts do not reference `REQUIRED_READINESS_TABLES` or `reproject_issue_i18n`
- `new_board_label` without manifest flag → `taxonomy_apply_gateway.py` exits non-zero
- Backfill write (TC6b) — not automated; operator runs `reproject_issue_i18n.py` manually after dry-run review

## Out of scope (unchanged)

- GW-L10N-04 public registry endpoint
- Auto-trigger / cron for taxonomy cycles
- `docs/tasks/run-reports/taxonomy-cycles/cycle-*` folders (created only on first operational cycle)

## Next operator step

```text
@.cursor/plans/Taxonomy_builder.plan.md
Taxonomy cycle TC0–TC7. cycle_id=YYYYMMDD. Claims из кода.
```
