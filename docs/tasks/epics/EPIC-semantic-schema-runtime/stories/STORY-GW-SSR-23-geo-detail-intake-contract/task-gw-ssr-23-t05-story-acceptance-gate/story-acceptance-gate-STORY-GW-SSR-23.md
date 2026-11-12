# Story acceptance gate — STORY-GW-SSR-23

- **Story:** geo_detail wire + pack geo_intake
- **Package:** `pkg-000080-20260830-gw-ssr-23-geo-detail-intake-contract.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T20:40:50Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `geo_detail` парсится; invalid → IntakeValidationError. | PASS | `src/core/intake/contracts.py`; `tests/test_gw_ssr_23_geo_detail_intake.py` invalid pair / house XOR |
| `geo_intake.mode` управляет обязательностью. | PASS | `src/core/geo/intake_merge.py` `enforce_geo_intake_mode`; handlers + services |
| Optional omit зелёный; require_detail miss → 4xx. | PASS | `test_optional_omit_202`; `test_require_detail_miss_400` |
| Merge с `location_query` задокументирован и покрыт тестом. | PASS | README §geo_intake merge; `test_merge_client_district_wins` |
| README ключи; три packs с `geo_intake` (хотя бы optional). | PASS | `schema-packs/README.md`; three `pack.json` |

## G23 (runbook §6.2)

| G23 check | Result | Evidence |
|-----------|--------|----------|
| accept detail | PASS | `test_accept_geo_detail_202` → 202 |
| invalid/require miss → 4xx | PASS | invalid pair 400; `require_detail` miss 400 |
| optional omit → 202 | PASS | `test_optional_omit_202` |
| packs с `geo_intake` | PASS | `test_three_packs_have_geo_intake` |
| ClusterLens=10 | PASS | `test_clusterlens_still_ten_members` |

## Commands (live verification — P3)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python3.11 -m pytest -q -m "not live_integration" tests/test_gw_ssr_23_geo_detail_intake.py
# 12 passed 2026-08-30T20:40:50Z
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
