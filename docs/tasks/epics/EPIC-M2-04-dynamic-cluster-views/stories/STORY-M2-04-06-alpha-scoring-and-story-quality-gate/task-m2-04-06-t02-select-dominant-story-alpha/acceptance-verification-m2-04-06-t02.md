# Acceptance verification — TASK-M2-04-06-T02

- **Task:** wire `select_dominant_story` to alpha
- **Result:** PASS
- **Evidence:** `extraction_policy.py` uses `alpha_score`; tests `test_select_dominant_story_*` in `test_alpha_score.py`
- **Commands:** `pytest tests/test_alpha_score.py tests/test_projection_canonical_derivation.py -q`
