# acceptance-verification — GW-SSR-03 t03

- **Result:** PASS
- **Date:** 2026-08-28T14:13:05Z
- **Package:** pkg-000063

## Evidence

`StoryIntakeService.create_story` calls `LocalSchemaRuntime.resolve` + `validate` before `save_story`; `SchemaRuntimeError` → `IntakeValidationError`; factory wires `LocalSchemaRuntime()`.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_03_optional_v2_semantic_wire.py::test_invalid_structured_payload_rejected_not_silent
```
