# Story acceptance gate — STORY-GW-SSR-17

- **Story:** Intake только активная схема ноды
- **Package:** `pkg-000074-20260830-gw-ssr-17-intake-active-schema-gate.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T14:45:34Z

## G17 (runbook §6.2)

| G17 check | Result | Evidence |
|-----------|--------|----------|
| civic HTTP **без** binding → 4xx (не civic persist) | PASS | `tests/test_gw_ssr_17_intake_active_schema.py` `test_http_absent_binding_is_4xx`; parse absent/`{}`/null |
| match `schema_binding` == `NODE_SCHEMA_*` → 202 | PASS | `test_http_match_is_202`; persist `test_match_validates_active_pack_and_persists` |
| mismatch id или version → 4xx | PASS | `test_http_mismatch_is_4xx`; `test_mismatch_id_or_version_raises` |
| GPT UI files не в diff | PASS | `git diff --name-only` — no GPT UI paths |
| `ClusterLens` members **ровно** baseline (10) | PASS | `src/core/cluster/types.py:10–22` |
| нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions` | PASS | `rg` `src/core/api/asgi_app.py` empty |
| pytest `test_gw_ssr_17_*` + `test_gw_ssr_03_*` зелёный | PASS | 22 passed (`-m "not live_integration"`) |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Нет `schema_binding` / empty object → 4xx, Story не сохраняется civic. | PASS | `contracts.py:227–241`, `:480–482`; G17 absent/`{}`/null |
| Другой `schema_id` или `schema_version` → 4xx. | PASS | `services.py:252–260`; G17 mismatch |
| Совпадение с `NODE_SCHEMA_*` → validate + persist binding. | PASS | `services.py:261–279` `SchemaRef(active_id, active_version)` |
| Существующие HTTP-тесты intake без binding зелёные **после** адаптации (binding + env), не «skip всех». | PASS | fixtures `active_node_schema_binding()`; req24 3× intake (pack min_size); req24+G17 45 passed |
| GPT UI files не в diff. | PASS | git name-only — no GPT UI |

## Commands (live verification 2026-08-30T14:45:34Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_17_*.py
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "schema-active|/schema-filter|story_dimensions" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
