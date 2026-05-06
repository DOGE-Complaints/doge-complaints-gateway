# Acceptance verification — task-m2-17-01-living-issues-primary

## AC checklist
- [x] Gap закрыт и подтвержден командами проверки.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```

## Verification performed
- `pytest -q tests/test_issue_promotion_service.py tests/test_issue_create_service.py tests/test_e2e_story_cluster_issue_pipeline.py tests/test_process_linkage_sqlite.py` -> `17 passed`.
- `pytest -q tests/test_story_cluster_orchestrator.py tests/test_embedding_policy_versioning.py tests/test_unit_branch_closure_by_layer.py tests/test_unit_domain_flows_supabase_wave.py` -> `21 passed`.
