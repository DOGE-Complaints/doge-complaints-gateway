# Story acceptance gate — STORY-GW-RC-05

- **Story:** Канонизация status (write board-vocab + read-канонизация + контракт-тест)
- **Package:** `pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml`
- **Result:** PASS
- **Date:** 2026-06-20

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| После write-fix реальный create→extend кладёт в `doge_issues.status` board-vocab (PUBLISHED), не `promoted`. | PASS | T01 `issue_create.py:334`; T04 `test_gw_rc_05_status_vocabulary_contract.py::test_create_then_extend_writes_board_status_not_candidate_promoted` |
| `GET /tallinn/issues` отдаёт `status ∈ {NEW,IN_REVIEW,PUBLISHED}` даже для legacy `promoted` (read-канонизация). | PASS | T02 `canonicalize_status_on_read` + `get_projection` merge; `test_gw_rc_05_status_canonical_on_read.py` |
| Контракт-тест гоняет **реальный** пайплайн (не happy-seed) и ловит невалидный status. | PASS | T04 `test_gw_rc_05_status_vocabulary_contract.py` create→extend |
| Тесты, фиксировавшие projection `promoted`, обновлены; candidate-asserts не затронуты. | PASS | T03 integration tests; `:133` candidate assert unchanged |
| Тест-суит без регрессий. | PASS | `522 passed in 165.33s` — live run 2026-06-20 |

## Commands (live verification 2026-06-20)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_05_status_canonical_on_read.py tests/test_gw_rc_05_status_vocabulary_contract.py -q
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
