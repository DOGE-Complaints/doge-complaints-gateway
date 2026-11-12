# acceptance-verification — GW-SSR-15 t06

- **Result:** PASS
- **Date:** 2026-08-29T19:47:15Z
- **Package:** pkg-000072

## Evidence

Story gate PASS. G15 product: public pytest URLs `/node/…`; only `/tallinn/issues` leftover = T05 404; scenarios 1–3+5 + T-dual include; ClusterLens 10; no filter HTTP; not live_integration proof.

Full offline: **744 passed**, 12 skipped (smoke `GATEWAY_URL` / server — not G15 proof), 10 deselected (`live_integration`). Known T-wave FAIL `test_missing_identity_config_returns_503` (D-SSR-3; identity-service not rewritten) — documented in gate, not this story.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration"
# → 744 passed, 1 failed (known identity 503), 12 skipped, 10 deselected
```
