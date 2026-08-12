# Acceptance verification — TASK-M2-02-12-T12

- **Task:** remove title_hint from persistence layer
- **Result:** Pass
- **Evidence:** no `narrative_title_hint` in `src/`; `required_columns_ready()` without hint; `required_stories_narrative_extension_columns_ready()` without hint_et/ru/en; `000_full_init.sql` without hint columns; hosted `columns_ready=True` after T11 data purge
- **Commands:** `python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration` → **443 passed**
