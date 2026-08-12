# Acceptance — TASK-GW-GAUTH-01-T01

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Политика «оба слоя» — inventory matrix complete (D-GAUTH-2) | PASS | [`public-content-write-path-inventory.md`](./public-content-write-path-inventory.md) — 3 POST routes; intake + tallinn/issues = public content; telemetry excluded |
| All `@app.post` in `asgi_app.py` listed | PASS | `rg '@app\.(post|put|patch|delete)' src/core/api/asgi_app.py` → 3 POST |
