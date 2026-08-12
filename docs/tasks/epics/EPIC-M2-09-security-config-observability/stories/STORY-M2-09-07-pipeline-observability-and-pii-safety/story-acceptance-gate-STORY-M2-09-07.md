# Story acceptance gate — STORY-M2-09-07

- **Story:** Pipeline observability and PII safety (REQ-37)
- **Package:** `pkg-000016-20260516-req37-pipeline-observability-pii-safety.yaml`
- **Result:** PASS
- **Date:** 2026-05-17

## AC checklist (REQ-37 §5)

| AC | Status | Evidence |
|----|--------|----------|
| `LOG_DEBUG_DIR` → `{story_id}.jsonl` | PASS | `test_story_debug_logger_writes_jsonl`, `test_intake_debug_jsonl_five_stages` |
| JSONL contains 5 stages | PASS | `test_intake_debug_jsonl_five_stages` — intake, geo, signals, cluster, promotion |
| Unset `LOG_DEBUG_DIR` → no files | PASS | `test_intake_no_debug_file_when_dir_unset`, `test_story_debug_logger_no_op_without_dir` |
| `redact_pii(True)` → `[REDACTED]` | PASS | `test_redact_pii_true_returns_redacted` |
| `redact_pii(False)` → full text | PASS | `test_redact_pii_false_returns_original` |
| PII story → no cleartext in embedding source | PASS | `test_embedding_source_redacts_pii_text` |
| `LOG_DEBUG_DIR` independent of `LOG_LEVEL` | PASS | `test_debug_jsonl_independent_of_log_level` |
| `gateway_resolve_queue.py --verify` ok 6 paths | PASS | pkg-000016 |

## Runtime files

- `src/core/redaction.py`, `src/core/api/logging.py` (re-export)
- `src/core/logging_setup.py` (`StoryDebugLogger`)
- `src/core/application/services.py`, `geo/service.py`, `profile/enrichment.py`, `cluster_orchestrator.py`
- `src/core/infrastructure/service_factory.py`, `example.env`
- `tests/test_req37_pipeline_observability_pii.py`

## Commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q
```
