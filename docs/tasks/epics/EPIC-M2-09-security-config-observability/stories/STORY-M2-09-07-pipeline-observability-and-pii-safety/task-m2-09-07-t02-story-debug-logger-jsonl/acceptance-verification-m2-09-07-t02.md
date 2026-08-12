# Acceptance verification — TASK-M2-09-07-T02

- **Task:** `StoryDebugLogger` JSONL per story
- **Result:** PASS
- **Evidence:** `src/core/logging_setup.py` — `{debug_dir}/{story_id}.jsonl`, JSON Lines format; `example.env` comment
- **Commands:** `pytest tests/test_req37_pipeline_observability_pii.py -q -k jsonl`
