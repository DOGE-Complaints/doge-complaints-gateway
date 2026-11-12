# Story acceptance gate — STORY-GW-SSR-01

- **Story:** SchemaRuntime local-first + SCHEMA-005 pack load
- **Package:** `pkg-000061-20260828-gw-ssr-01-schema-runtime-pack-load.yaml`
- **Result:** PASS
- **Date:** 2026-08-28T13:18:56Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ3-01 / parent AC-001+013: SCHEMA-005 pack loads; valid payload without new domain field on `StoryRecord` / per-field parser / `stories` column / clustering engine change for that pack’s exact lens **declaration**. Parser-once FLOW-003 = **SSR-03**. | PASS | `LocalSchemaRuntime` + `schema-packs/legal_process/v1` + `mobility_observation/v1`; no `StoryRecord` / intake / `engine.py` edits |
| AC-GW-REQ3-04 / AC-004: violating payload rejected; no required value invented; distinguish at least unknown schema / unsupported version / invalid type / missing required / forbidden / invalid constraint / policy violation / profile incompatibility (RUNTIME-005). | PASS | `tests/test_gw_ssr_01_schema_runtime.py` typed errors; canonicalize does not invent `institution` |
| SEC-001: pack YAML/JSON cannot execute arbitrary Python/JS/shell. | PASS | `json.loads` only; `test_no_code_exec_from_pack_bytes` |
| SEC-002: limits against abusive recursion/nesting/oversized payload / cyclic `$ref` (as applicable). | PASS | `MAX_PAYLOAD_BYTES` / `MAX_NESTING_DEPTH`; `assert_schema_safe` cyclic + external `$ref` |
| Conceptual `LegacyM2StorySchema` named in code/docs (COMPAT-001). | PASS | `src/core/schema/legacy.py`; `INTAKE_SCHEMA_VERSION` unchanged |
| Packs live under `schema-packs/` (data); runtime under `src/core/schema/` (code) — **D-SSR-4**. | PASS | dirs on disk; `SCHEMA_PACKS_ROOT` hook |
| Tests §29 Unit that apply: schema resolution, JSON Schema validation, canonicalization, field-policy as represented in pack. | PASS | `tests/test_gw_ssr_01_schema_runtime.py` 20 passed |
| T07 extra: `ClusterLens` enum **не** изменён (`rg ClusterLens src/core/cluster/types.py`). | PASS | `test_clusterlens_baseline_unchanged`; types.py members unchanged |

## Commands (live verification 2026-08-28T13:18:56Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_01_*.py
# → 20 passed
rg -n 'class ClusterLens' -A 14 doge-complaints-gateway/src/core/cluster/types.py
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
