# Story acceptance gate — STORY-GW-TAX-01

- **Story:** Taxonomy persistence fidelity (per-axis, без потерь)
- **Package:** `pkg-000054-20260714-gw-tax-01-taxonomy-persistence-fidelity.yaml`
- **Result:** PASS
- **Date:** 2026-07-14T20:55:43Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Intake принимает per-axis таксономию; ось **не угадывается**, а берётся из контракта (D-TAX-1) | PASS | `parse_story_intake_request` + `narrative.taxonomy` in [`intake/contracts.py`](../../../../../../../../src/core/intake/contracts.py); `tests/test_gw_tax_01_taxonomy.py::test_intake_accepts_per_axis_taxonomy_and_derives_canonical_flat_labels` |
| Все метки (canonical/metadata_only/internal) персистятся в `story_labels` с disposition (D-TAX-3) | PASS | `StoryIntakeService.create_story` → `story_label_repository.save_labels`; migration `20260714_1200_gw_tax_01_story_labels.sql`; `test_persist_all_dispositions_on_submit` |
| Public read никогда не отдаёт `internal`-метки (§24) | PASS | `public_label_strings` / `canonical_labels_from_cluster(story_label_repository=…)`; `test_public_read_filter_excludes_internal_and_metadata_only` |
| Legacy плоские истории не ломаются (fallback) | PASS | `get_signals_for_story` falls back to `infer_signals_from_canonical`; `test_legacy_flat_labels_fallback_still_works`; empty `taxonomy: []` tolerant parse |
| Full offline suite green | PASS | `597 passed` — `pytest -q -m "not live_integration"` 2026-07-14T20:55:43Z |

## Grep invariant (per-axis axis not re-guessed)

Per-axis stored labels route through `signals_from_story_labels` when `story_label_repository.list_by_story` is non-empty — `test_per_axis_signals_do_not_reguess_axis_from_dictionaries` (`roads` on `service_object` → `civic_domain=unknown`, legacy infer → `roads`).

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration"
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
