# Story acceptance gate — STORY-GW-REQ11-09

- **Story:** Operator threads seed after cluster (CLI + RU manual)
- **Package:** `pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml`
- **Result:** PASS
- **Date:** 2026-10-01T10:52:44Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1109-01 | PASS | Fail-closed exit 2 when `GET /node/issues` empty (live local + offline unit) |
| AC-GW-REQ1109-02 | PASS | CLI calls Present `closed_http_seed.seed_representative_issues` (file import) |
| AC-GW-REQ1109-03 | PASS | Actors from secrets by `fixture_user_id`; `refuse_service_token_as_actor` |
| AC-GW-REQ1109-04 | PASS | Handoff parse `issue_id`+`density`; Make `life-sim-seed-threads` Present |
| AC-GW-REQ1109-05 | PASS | RU manual Present; load-manual B-THR-CLI Closed |
| AC-GW-REQ1109-06 | PASS | No pack JSON mutate; offline 9 passed; K1 (API Bearer actors) |

## Leftover (documented, not FAIL)

- Live **full** seed after cluster: local `GET http://127.0.0.1:8000/node/issues` → `issues=[]` → fail-closed (expected until operator runs replay+cluster). No invent HTTP force-cluster.

## Commands (live verification 2026-10-01T10:52:44Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_09_seed_threads.py
GATEWAY_URL=http://127.0.0.1:8000 THREADS_URL=http://127.0.0.1:8001 \
  .venv/bin/python tests/sandbox/life_sim_seed_threads.py --dry-run  # exit 2 empty issues
```

SSOT дат: `guides/builder-artifact-dates.md`
