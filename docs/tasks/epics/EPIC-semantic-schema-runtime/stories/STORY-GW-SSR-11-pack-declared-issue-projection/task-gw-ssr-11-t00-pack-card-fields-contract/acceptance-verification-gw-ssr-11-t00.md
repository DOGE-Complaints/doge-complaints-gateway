# acceptance-verification — GW-SSR-11 t00

- **Result:** PASS
- **Date:** 2026-08-29T19:13:51Z
- **Package:** pkg-000070

## Evidence

Loader key `card_fields` (array of dotted paths, optional) on `SchemaContext` (`contracts.py`). Absent/`[]` = civic form. Wire sidecar on `GET /node/issues` is named `schema_card` (flat dotted-path keys), not a payload dump. Documented in `schema-packs/README.md` (SCHEMA-005 this-loader-only). REQ-09 `type`/`status` stay civic required keys on `DOGEIssue`.

## Commands

```bash
rg -n "card_fields" doge-complaints-gateway/schema-packs/README.md \
  doge-complaints-gateway/src/core/schema/contracts.py
rg -n "GET /node/issues|@app.get\\(\"/node/issues\"\\)" doge-complaints-gateway/src/core/api/asgi_app.py
```
