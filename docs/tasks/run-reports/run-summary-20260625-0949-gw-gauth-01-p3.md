# run-summary-20260625-0949-gw-gauth-01-p3

**Date:** 2026-06-25  
**Story:** STORY-GW-GAUTH-01 — two-layer auth on public content writes  
**Package:** pkg-000039  
**Epic:** EPIC-M2-20  
**Mode:** explicit (YAML default + build window flat 1–5)  
**Result:** PASS (T01–T05)

## Executed items

| Task | Outcome | Evidence |
|------|---------|----------|
| T01 | Done | [`public-content-write-path-inventory.md`](../epics/EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-01-two-layer-auth-on-submit/task-gw-gauth-01-t01-inventory-public-content-write-paths/public-content-write-path-inventory.md) |
| T02 | Done | `_PUBLIC_CONTENT_WRITE_DEPS` on intake + tallinn/issues |
| T03 | Done | `ServiceTokenAuth.mandatory` + `build_service_auth_from_env` policy |
| T04 | Done | `tests/test_gw_gauth_01_two_layer_auth_contract.py` (6 tests) |
| T05 | Done | gate PASS [`story-acceptance-gate-STORY-GW-GAUTH-01.md`](../epics/EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-01-two-layer-auth-on-submit/task-gw-gauth-01-t05-story-acceptance-gate/story-acceptance-gate-STORY-GW-GAUTH-01.md) |

## Verification (live)

```
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify → ok 5 paths (pkg-000039)
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py → 6 passed
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q -m 'not live_integration' → 534 passed, 12 skipped
```

## Code scope

- `src/core/api/security.py` — mandatory service auth, user token stub
- `src/core/api/asgi_app.py` — two-layer deps on public writes
- `src/core/api/handlers.py` — ops routes `mandatory=False`
- `src/core/config/schema.py` — SERVICE_API_TOKEN policy note
- `tests/conftest.py` — gauth headers + TestClient auto-inject
- `tests/test_gw_gauth_01_two_layer_auth_contract.py` — contract suite
- `tests/simulation_runner.py` — Bearer + X-User-Token

## Out of scope (next stories)

- GW-GAUTH-02 introspection
- GW-GAUTH-03 verification_required 403
- GW-GAUTH-04 authoritative sub
