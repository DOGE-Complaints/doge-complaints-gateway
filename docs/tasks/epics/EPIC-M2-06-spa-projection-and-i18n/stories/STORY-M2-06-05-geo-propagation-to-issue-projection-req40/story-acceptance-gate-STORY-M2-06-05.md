# Story acceptance gate — STORY-M2-06-05

- **Story:** Geo propagation to issue projection (REQ-40)
- **Package:** `pkg-000018-20260517-req40-geo-propagation-issue-projection.yaml`
- **Result:** PASS
- **Date:** 2026-05-17

## AC checklist (REQ-40 §7)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: geo in issue payload when dominant has geo | PASS | `test_req40_ac1_geo_present_in_issue_payload_when_dominant_has_geo` |
| AC-2: no `geo` key when stories lack geo | PASS | `test_req40_ac2_issue_payload_omits_geo_key_when_stories_have_no_geo` |
| AC-3: payload geo = dominant story (alpha_score) | PASS | `test_req40_ac3_payload_geo_matches_dominant_story_alpha_score` |
| AC-4: backward compat without geo | PASS | `test_req40_ac4_backward_compat_projection_without_geo_fields` |
| `gateway_resolve_queue.py --verify` ok 6 paths | PASS | pkg-000018 |

## Runtime files

- `src/core/projection/input.py`, `dto.py`, `mapper.py`, `extraction_policy.py`
- `src/core/application/issue_create.py`
- `tests/test_req40_geo_propagation.py`

## Commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q
```
