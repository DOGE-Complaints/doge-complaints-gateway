# task-gw-rc-05-t03

## Meta
- **Story:** [STORY-GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000034
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
Обновить тесты, фиксирующие projection `promoted`→`PUBLISHED` (roundtrip :29/53, live :155); НЕ трогать candidate-assert (:133).

## Code Facts
- Roundtrip seed/assert `promoted` — [`test_spa_projection_supabase_roundtrip.py:29,53`](../../../../../../../tests/integration/supabase/test_spa_projection_supabase_roundtrip.py#L29)
- Live pipeline projection assert — [`test_supabase_live_full_pipeline_roundtrip.py:155`](../../../../../../../tests/integration/supabase/test_supabase_live_full_pipeline_roundtrip.py#L155)
- Candidate assert **do not touch** — [`test_supabase_live_full_pipeline_roundtrip.py:133`](../../../../../../../tests/integration/supabase/test_supabase_live_full_pipeline_roundtrip.py#L133) `candidate_rows` — `promoted` correct there

## Acceptance / DoD
- Traces parent AC: тесты, фиксировавшие projection `promoted`, обновлены; candidate-asserts не затронуты
- Projection seeds/asserts use `PUBLISHED` (board-vocab), not `promoted`
- Line :133 candidate_rows assert unchanged
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`tests/integration/supabase/test_spa_projection_supabase_roundtrip.py`](../../../../../../../tests/integration/supabase/test_spa_projection_supabase_roundtrip.py)
- [`tests/integration/supabase/test_supabase_live_full_pipeline_roundtrip.py`](../../../../../../../tests/integration/supabase/test_supabase_live_full_pipeline_roundtrip.py) — projection assert only (:155), not :133

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/integration/supabase/test_spa_projection_supabase_roundtrip.py tests/integration/supabase/test_supabase_live_full_pipeline_roundtrip.py -q
```
