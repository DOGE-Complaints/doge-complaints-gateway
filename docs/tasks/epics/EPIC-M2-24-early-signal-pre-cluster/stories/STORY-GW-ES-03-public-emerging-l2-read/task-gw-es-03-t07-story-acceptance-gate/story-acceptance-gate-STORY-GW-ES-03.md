# Story acceptance gate — STORY-GW-ES-03

- **Story:** Public Emerging L2 read (derived, ≠ Issues)
- **Package:** `pkg-000060-20260810-gw-es-03-public-emerging-l2-read.yaml`
- **Result:** PASS
- **Date:** 2026-08-10T12:17:38Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| T00: path+payload named outside story file alone | PASS | REQ-50 `GET /tallinn/emerging-signals` + §3 payload + §4 MVP rule |
| MVP rule: label freq; exclude published-linked; runtime-docs | PASS | `emerging_signals.py`; API_REFERENCE Emerging section |
| No `EmergingSignal` table/migration | PASS | no emerging DDL; ephemeral derived service |
| Service on ApiDependencies / factory — not cabinet dig | PASS | `get_emerging_signals_service` + deps field; handler uses deps only |
| Public GET; path in PUBLIC_ROUTES | PASS | `asgi_app.py`; HTTP smoke |
| Response distinct from `GET /tallinn/issues` | PASS | shape tests + HTTP comparison |
| Topic ≠ Issue; no threshold-gaming; clustering unchanged | PASS | REQ-50 + unit asserts; no cluster gate edits |
| No PII in payload | PASS | unit asserts no submitter/narrative |

## Commands (live verification 2026-08-10)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_03_emerging_signals.py tests/test_gw_es_02_network_pulse.py tests/test_gw_public_01_public_issues_regression.py
# → ok 8 paths; check-dates ok; 16 passed
```

SSOT дат: `guides/builder-artifact-dates.md`
