# acceptance-verification — GW-SSR-11 t02

- **Result:** PASS
- **Date:** 2026-08-29T19:13:51Z
- **Package:** pkg-000070

## Evidence

Named sidecar via `DOGEIssue.to_public_dict(schema_card=…)` (`dto.py`) — no new required keys on the dataclass. Extractor `project_card_fields` (`card_fields.py`) filters `forbidden` / `node_private` even if listed. Wired at `IssueCreateService._to_public_payload` (`issue_create.py`). `SchemaRuntime.project` stays `NotImplementedError` (`runtime.py:68–72`). Public read remains `GET /node/issues` (`asgi_app.py:462`). `rg structured_payload` in `dto.py` empty.

## Commands

```bash
rg -n "structured_payload" doge-complaints-gateway/src/core/projection/dto.py
rg -n "NotImplementedError" doge-complaints-gateway/src/core/schema/runtime.py
rg -n "GET /node/issues|@app.get\\(\"/node/issues\"\\)" doge-complaints-gateway/src/core/api/asgi_app.py
```
