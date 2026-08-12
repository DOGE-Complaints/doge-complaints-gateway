# Story acceptance gate — STORY-M2-02-09

- **Story:** institution_json story column + intake (REQ-43)
- **Package:** `pkg-000023-20260523-req43-institution-json-story-column.yaml`
- **Result:** PASS
- **Date:** 2026-05-23

## AC checklist (REQ-43 §5)

| AC | Status | Evidence |
|----|--------|----------|
| Intake with valid `narrative.institution` → HTTP 202 | PASS | `test_intake_with_institution_returns_202_and_persists_sqlite` |
| `stories.institution_json` persisted | PASS | sqlite `get_story` → `narrative_institution` |
| Intake without institution → NULL column | PASS | `test_intake_without_institution_leaves_column_null` |
| Incomplete i18n institution → HTTP 400 | PASS | `test_intake_invalid_institution_returns_400`, `test_parse_incomplete_institution_raises` |
| `payload_json.institution` i18n dict on promotion | PASS | `test_bridge_projection_institution_roundtrip_from_dominant_story` |
| Runtime docs + OpenAPI + persistence model | PASS | T06 — `API_REFERENCE.md`, `openapi.yaml`, `story-persistence-model.md` |

## Verification command

```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py
```

**Outcome:** 7 passed (2026-05-23 P3).
