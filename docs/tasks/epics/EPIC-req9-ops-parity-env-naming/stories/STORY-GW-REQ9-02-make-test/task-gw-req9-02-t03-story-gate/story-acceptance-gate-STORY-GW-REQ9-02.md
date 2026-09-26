# Story acceptance gate — STORY-GW-REQ9-02

- **Story:** Makefile `test` + `test-live` (REQ9 G7)
- **Package:** `pkg-000097-20260926-gw-req9-02-make-test.yaml`
- **Result:** PASS
- **Date:** 2026-09-26T12:22:28Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ902-01: `make test` exists and runs offline pytest with `-m "not live_integration"` | PASS | `Makefile:50–51`; live `make test` → 10 `live_integration` deselected |
| AC-GW-REQ902-02: `.PHONY` includes `test` | PASS | `Makefile:1` |
| AC-GW-REQ902-03: `make test-live` exists for live_integration suite | PASS | `Makefile:53–54`; collect-only 10/918; PHONY includes `test-live` |

## Commands (live verification — P3)

```text
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
→ ok 3 paths (pkg-000097)
--verify --check-dates → ok date-check
utc_now: 2026-09-26T12:22:28Z
cd doge-complaints-gateway && make -n test && make -n test-live
→ .venv/bin/python -m pytest -q -m "not live_integration"
→ .venv/bin/python -m pytest -q -m live_integration
make test → 886 passed, 18 skipped, 10 deselected; 4 failed (pre-existing MVP dirt: bootstrap/ssr — out of REQ9-02 AC)
Honesty: offline make test ≠ Railway/hosted verify; no invent CI/markers; serve/dev/simulate/check-env semantics unchanged beyond PHONY; §Актуальная точка not rewritten
```
