# Story acceptance gate — STORY-GW-TAX-03

- **Story:** STORY-GW-TAX-03-align-story-labels-migration-text-fk
- **Package:** `pkg-000058-20260807-gw-tax-03-align-story-labels-migration-text-fk.yaml`
- **Result:** PASS
- **Date:** 2026-08-07T09:59:37Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Repo migration path для `story_labels` использует **text** FK на `stories(story_id)`, не UUID. | PASS | T02; [`20260714_1200_…sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) `story_id text` |
| Indexes `idx_story_labels_story` / `idx_story_labels_axis` сохранены или эквивалентны. | PASS | T02; same file CREATE INDEX |
| Комментарий/guard в SQL: UUID DDL несовместим с text `stories.story_id`. | PASS | T02; GUARD header in migration |
| Package INDEX отражает TAX-03 Done/Deferred закрытие dual-path. | PASS | T04; [`taxonomy-fidelity/INDEX.md`](../../../../../../backlog-stories/taxonomy-fidelity/INDEX.md) |
| DRAFT-07 **не** reopen; `REQUIRED_READINESS_TABLES` / FE / `/ready` gate **не** меняются ради этой стори. | PASS | T01–T05; `story_labels` still in [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py); no DRAFT-07 reopen; no FE/`src` readiness edits |

## Commands (live verification 2026-08-07)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
rg -n 'story_id text|UUID|ROW LEVEL SECURITY|story_labels_service_role' doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
rg -n 'TAX-03|Done|dual-path' doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/INDEX.md
rg -n 'story_labels' doge-complaints-gateway/src/core/infrastructure/db_supabase.py | head
```

**Live run:** verify ok 5 paths; migration text FK + RLS; INDEX Done; REQUIRED set unchanged; DRAFT-07 not reopened.

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
