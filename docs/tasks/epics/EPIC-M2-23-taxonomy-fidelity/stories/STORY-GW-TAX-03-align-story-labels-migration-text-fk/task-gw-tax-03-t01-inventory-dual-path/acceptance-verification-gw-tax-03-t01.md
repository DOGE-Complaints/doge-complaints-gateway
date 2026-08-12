# Acceptance verification — GW-TAX-03 T01

- **Task:** task-gw-tax-03-t01-inventory-dual-path
- **Result:** PASS
- **Date:** 2026-08-07T09:59:37Z

## Evidence — dual-path inventory (pre-T02)

| Источник | `story_labels.story_id` | Ref / evidence |
|----------|-------------------------|----------------|
| Repo migration TAX-01 (pre-T02) | **UUID** | `rg` line 3: `story_id UUID NOT NULL REFERENCES stories(story_id)` |
| Bootstrap | **text** | `000_full_init.sql:86-87` `create table … story_labels` / `story_id text` |
| SQLite auto-DDL | **TEXT** | `db_sqlite.py:385-390` |
| Peer `story_signals` | **text** | `20260523_1200_req42_story_signals.sql:4` |
| Hosted Public Node | **text** (post DRAFT-07) | execution/elegance audits 2026-08-07; DRAFT-07 **not** reopened |

**Verdict:** dual-path confirmed; T02–T03 edit migration only.
