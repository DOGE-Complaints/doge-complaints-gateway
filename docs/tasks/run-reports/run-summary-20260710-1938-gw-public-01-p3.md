# Run summary — GW-PUBLIC-01 P3 Execute

- **Story:** STORY-GW-PUBLIC-01 public issues regression gate (M-5)
- **Package:** pkg-000048-20260710-gw-public-01-public-issues-regression.yaml
- **Date:** 2026-07-10
- **Result:** PASS (offline)

## Tasks

| Task | Result | Evidence |
|------|--------|----------|
| T01 | PASS | `test_gw_public_01_t01_list_without_auth_returns_200` |
| T02 | PASS | `test_gw_public_01_t02_get_by_id_*` (200 + 404, not 401/403) |
| T03 | PASS | `test_gw_public_01_t03_post_story_drafts_without_service_token_401` |
| T04 | PASS | `test_gw_public_01_t04_post_tallinn_issues_without_service_token_401` (`@pytest.mark.gauth_raw_client`) |
| T05 | PASS | [`story-acceptance-gate-STORY-GW-PUBLIC-01.md`](../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-PUBLIC-01-public-issues-regression/task-gw-public-01-t05-story-acceptance-gate/story-acceptance-gate-STORY-GW-PUBLIC-01.md) |

## Verification

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py  # 5 passed
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"  # 568 passed
```

## Code delta

- `tests/test_gw_public_01_public_issues_regression.py` (new, 5 tests)
