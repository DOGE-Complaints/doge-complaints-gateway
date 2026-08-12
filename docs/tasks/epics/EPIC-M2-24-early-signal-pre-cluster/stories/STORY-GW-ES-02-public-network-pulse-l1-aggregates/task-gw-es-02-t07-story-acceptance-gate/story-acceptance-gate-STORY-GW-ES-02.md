# Story acceptance gate — STORY-GW-ES-02

- **Story:** Public Network Pulse L1 aggregates
- **Package:** `pkg-000059-20260810-gw-es-02-public-network-pulse-l1-aggregates.yaml`
- **Result:** PASS
- **Date:** 2026-08-10T10:55:48Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| T00: follow-on REQ/ADR names path + payload | PASS | REQ-49 `GET /tallinn/network-pulse` + §3 payload |
| `NetworkPulseService` exists; `stories_collected` on `list_stories` | PASS | `src/core/application/network_pulse.py` |
| MVP dims languages/areas/topics/recent_7d | PASS | service + tests |
| Wired via ApiDependencies / factory — not intake dig | PASS | `dependencies.py` + `service_factory.py`; handler uses `network_pulse_service` |
| Public GET returns envelope; path in PUBLIC_ROUTES | PASS | `asgi_app.py`; HTTP smoke |
| Topic ≠ Issue; no «N Stories until Issue»; no PII / Voices | PASS | payload keys + unit asserts |
| `/metrics` not used for Pulse | PASS | separate route; metrics untouched |
| `GET /tallinn/issues` unchanged | PASS | ES-02 + PUBLIC-01 regression |

## Commands (live verification 2026-08-10)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_02_network_pulse.py tests/test_gw_public_01_public_issues_regression.py
# → ok 8 paths; 9 passed
```

SSOT дат: `guides/builder-artifact-dates.md`
