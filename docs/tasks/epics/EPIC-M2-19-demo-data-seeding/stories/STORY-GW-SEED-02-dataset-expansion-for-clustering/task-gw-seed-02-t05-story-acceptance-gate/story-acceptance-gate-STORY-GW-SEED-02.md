# Story acceptance gate — STORY-GW-SEED-02

- **Story:** Расширение датасета для кластеризации (≥8 на кластер)
- **Package:** `pkg-000037-20260622-gw-seed-02-dataset-expansion-for-clustering.yaml`
- **Result:** PASS
- **Date:** 2026-06-22

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Расширенный canvas создан отдельным файлом; v0_1 не изменён. | PASS | T02 — `dogestonia_simulation_canvas_v0_2.json`; `acceptance-verification-gw-seed-02-t02.md` |
| По ≥N темам набирается ≥8 историй с общими метками (N согласовано в T01). | PASS | T01 `cluster-target-matrix.md` N=2, 9+9; T02 canvas |
| На прогоне формируются проекции issue (локально подтверждено). | PASS | T03 `cluster-verify-summary.md` — 2 issues; `tests/test_gw_seed_02_cluster_density.py` |
| Зафиксировано ожидаемое наполнение доски. | PASS | T04 `expected-board-fill-matrix.md` — 2 expected cards |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_seed_02_cluster_density.py
# 4 passed (2026-06-22)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
