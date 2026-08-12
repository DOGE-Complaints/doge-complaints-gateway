# Story acceptance gate — STORY-GW-TAX-02

- **Story:** STORY-GW-TAX-02-clustering-axis-expansion
- **Package:** `pkg-000055-20260715-gw-tax-02-clustering-axis-expansion.yaml`
- **Result:** PASS
- **Date:** 2026-07-15T11:52:51Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Primary issue-ключ = composite `civic_domain + failure_pattern` (не одна ось); карточки предметнее («сфера: сбой») | PASS | `composite_primary_cluster_key`; default `CLUSTER_PRIMARY_LENS=composite_primary_micro`; T01 acceptance |
| Добавлены оси `service_object`, `deep_need`, `ecosystem_signal` (из `story_labels` per-axis) как линзы/фасеты | PASS | T02–T03; `tests/test_gw_tax_02_cluster_axis_expansion.py` |
| Per-lens `min_size`: composite-primary=8, богатые оси ниже; глобально не понижен | PASS | `CLUSTER_MIN_SIZE_BY_LENS` default composite=8; global default 5 unchanged; T04 acceptance |
| Демо-доска (v0_2) не опустела; existing cluster-тесты + full offline suite green | PASS | v0_2 composite buckets 9+9; `process_all_pending` ≥2 issues; **607 passed** offline |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration"
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
