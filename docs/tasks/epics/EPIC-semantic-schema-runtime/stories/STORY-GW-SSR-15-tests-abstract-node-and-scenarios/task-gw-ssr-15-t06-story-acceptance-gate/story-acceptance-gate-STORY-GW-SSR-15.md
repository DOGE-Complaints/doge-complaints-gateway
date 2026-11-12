# Story acceptance gate — STORY-GW-SSR-15

- **Story:** Tests: `/node/*` naming + scenario spectrum
- **Package:** `pkg-000072-20260829-gw-ssr-15-tests-abstract-node-and-scenarios.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T19:47:15Z

## G15 (runbook §6.7)

Pytest paths `/node/…`; сценарии civic / pack / Pulse≠issues / 404 `/tallinn/issues`. Rename req24 done. T-dual included (SSR-10 Done). Full offline `pytest -q -m "not live_integration"` run.

| G15 check | Result | Evidence |
|-----------|--------|----------|
| полный offline pytest | PASS | T07 isolation 2026-08-29T19:57:04Z: **exit 0**; **745 passed**, 12 skipped smoke (hosted GATEWAY_URL skip; not hosted proof), 10 deselected live_integration |
| публичные URL в pytest = `/node/…`; единственные `/tallinn/issues` — негатив 404 | PASS | `rg '@app.get("/tallinn'` empty; `rg 'client.(get\|post)("/tallinn'` = `test_gw_ssr_15_scenarios.py:100` 404 only |
| сценарии 1–3 и 5; T-dual include | PASS | `tests/test_gw_ssr_15_scenarios.py` |
| `ClusterLens` baseline; нет filter HTTP | PASS | `types.py:10–22` still 10; `rg story_dimensions\|/schema-filter` asgi empty |
| не `live_integration` как proof | PASS | marker `-m "not live_integration"`; smoke skips not used as proof |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Публичные URL в pytest = `/node/…`. | PASS | T01 path rewrite; G15 rg |
| Сценарии 1–3 и 5 зелёные; 4 по правилу T-dual. | PASS | `test_gw_ssr_15_scenarios.py`; T-dual include |
| Файл req24 без `tallinn` в имени | PASS | `tests/test_req24_issues_read_api.py` |
| Не live_integration. | PASS | G15 command `-m "not live_integration"` |

## Commands (live verification 2026-08-29T19:47:15Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration"
rg -n '@app.get\("/tallinn' tests --glob '*.py'
rg -n 'client\.(get|post)\("/tallinn' tests --glob '*.py'
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

- **G15 suite (T07):** exit 0; 745 passed / 12 skipped / 10 deselected (2026-08-29T19:57:04Z). Identity-service **not** rewritten (D-SSR-3). Isolation only.
- **Smoke:** 12 skipped (hosted `GATEWAY_URL` ≠ localhost). Not live_integration proof; not hosted G15 proof.
- SSR-06/07/12 not started. SSR-01…05 / 08–11 / 13 / 14 not reopened. Pie T-wave unchanged. bullrun §«Актуальная точка» unchanged. `gateway-mvp-dashboard.md` unchanged. pkg-000072 immutable. No alias 200. Geo `settlement:tallinn` stay.
