# Story acceptance gate — STORY-GW-SSR-22

- **Story:** Civic geo-gate hardening
- **Package:** `pkg-000079-20260830-gw-ssr-22-civic-geo-gate-hardening.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T20:07:21Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| При активном `geo_scope` и `geo_service is None` intake **не** проходит молча. | PASS | `handlers.py:258–260` `IntakeValidationError("geo unavailable")`; test_scope_plus_no_geo_service_does_not_accept → 400 |
| Без `geo_scope` поведение geo-agnostic сохраняется (как REQ-35 optional). | PASS | test_no_scope_plus_no_geo_service_still_accepts → 202; req35 without location → 202 |
| Тесты покрывают fail path и optional path. | PASS | `tests/test_gw_ssr_22_civic_geo_gate.py` + req35 **11 passed** |
| `ClusterLens` = 10; нет `GET /schema-active`. | PASS | `types.py:10–22` 10 members; `rg schema-active` asgi_app empty |

## G22 (runbook §6.1)

| G22 check | Result | Evidence |
|-----------|--------|----------|
| scope+no service не accept | PASS | 400 / geo unavailable |
| optional/no-scope path зелёный | PASS | 202; req35 no-location 202 |
| ClusterLens=10 | PASS | `types.py:10–22` |
| нет полного geo_detail wire (это 23) | PASS | no `geo_detail`/`geo_intake` parse in this pkg |

## Commands (live verification 2026-08-30T20:07:21Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_22_civic_geo_gate.py tests/test_req35_geo_scope_and_filter.py
rg -n "geo_service is None" src/core/api/handlers.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
