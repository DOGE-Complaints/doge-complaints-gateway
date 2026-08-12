# BULLRUN Phase Log — TASK-M2-02-06-T01 (GAP-02)

## Phase 1 — Analysis
- [x] Подтверждён §16 GAP-02: один `title_hint` терял et/ru/en.

## Phase 2 — Decision
- [x] Расширение контракта: `title_hint_et|ru|en` опционально + сохранение совместимости с `title_hint`.

## Phase 3 — Implementation
- [x] `Narrative` / `StoryRecord` / parser / `services.create_story` / SQLite + Supabase + bootstrap + миграция.
- [x] `api-orchestrator.md`: пример и маппинг для GPT.

## Phase 4 — Verification
- [x] `pytest` (gateway): зелёный прогон с учётом skip live Supabase при дрейфе схемы.

## Phase 5 — Documentation
- [x] §16 в `data-model-vs-bootstrap-000-full-init-2026-05-08.md` обновлён; README таска; этот лог.
