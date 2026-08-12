# Expected board fill matrix — STORY-GW-SEED-02 T04 (recalc GW-TAX-02 composite-primary)

- **Date:** 2026-06-22 (recalc note 2026-07-15: composite-primary key)
- **Canvas:** `tests/sandbox/dogestonia_simulation_canvas_v0_2.json`
- **Clustering env:** `CLUSTER_MIN_SIZE=8`, `CLUSTER_PRIMARY_LENS=composite_primary_micro`, `CLUSTER_MIN_SIZE_BY_LENS` composite=8; cron enabled on hosted (SEED-03)
- **T03 actuals:** 2 issue projections from 18 stories ([`cluster-verify-summary.md`](../task-gw-seed-02-t03-local-clustering-and-promotion-verify/cluster-verify-summary.md))

## Expected issue cards (after full v0_2 load + clustering)

| scenario_group | cluster theme | civic_domain | failure_pattern | district | stories in canvas | expected issues on board |
|----------------|---------------|--------------|-----------------|----------|-------------------|--------------------------|
| environment | C1-waste-kalamaja | waste | maintenance_gap | Kalamaja | 9 | **1** |
| infrastructure | C2-roads-lasnamae | roads | broken_infrastructure | Lasnamäe | 9 | **1** |

**Composite-primary key:** `civic_domain + failure_pattern + geographic_district` (district geo filter in SEED-02 offline tests).

**Total expected board cards (minimum):** **2** issue projections from a clean v0_2-only load.

## Notes for SEED-03

- Board read: `GET /tallinn/issues` ([`handlers.py`](../../../../../../../src/core/api/handlers.py))
- v0_1-only load (130 stories) does **not** guarantee ≥8/cluster — max observed **6** on hosted ([`analysis-clustering-seed-data-investigation-2026-06-22.md`](../../../../../../analysis/analysis-clustering-seed-data-investigation-2026-06-22.md))
- Set `SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_2.json` for clustering demo ([`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md))
