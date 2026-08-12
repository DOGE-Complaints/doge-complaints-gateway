# BULLRUN Phase Log — TASK-M2-02-06-T04 (GAP-06)

## Phase 1 — Analysis
- [x] Подтверждено: `live_story_context.consistency_notes` не попадал в `StoryRecord`.

## Phase 2 — Decision
- [x] Persist в колонку `narrative_consistency_notes` (text).

## Phase 3 — Implementation
- [x] `StoryRecord`, `create_story`, SQLite/Supabase, DDL в bootstrap + миграция.

## Phase 4 — Verification
- [x] `test_story_intake_live_context_not_on_record.py` — assert персистенции.

## Phase 5 — Documentation
- [x] §16, README.
