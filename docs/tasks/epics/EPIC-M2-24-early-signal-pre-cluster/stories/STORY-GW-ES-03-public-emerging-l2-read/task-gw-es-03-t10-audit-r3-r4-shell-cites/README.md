# task-gw-es-03-t10-audit-r3-r4-shell-cites

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060 (parent Done); wave `run_mode=gw_es_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-ES-03
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-es-03-public-emerging-l2-read-2026-08-10.md`](../../../../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md) **R3** + **R4**
- **Scaffolded:** 2026-08-10T12:44:19Z
- **Closed:** 2026-08-11T09:53:23Z

## Purpose
(1) **R3:** синхронизировать backlog §Подзадачи с pipeline pkg-000060 **T00–T07** (сейчас backlog lists T00–T05). (2) **R4:** обновить stale line cites (`asgi_app.py:427` Issues; `handlers.py:772–776` cabinet dig) на live номера (verify при P6).

## Code Facts
- Backlog подзадачи incomplete — [`STORY-GW-ES-03` backlog §Подзадачи](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md)
- Pipeline/bullrun T00–T07 — story folder task-* + pkg-000060
- Stale Issues cite — backlog/pipeline `asgi_app.py:427` (Issues list moved post Pulse/Emerging)
- Stale cabinet dig cite — `handlers.py:772–776` (shifted after emerging handler insert)
- Live Issues GET — grep `@app.get("/tallinn/issues")` in [`asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py)
- Live cabinet dig — grep StoryActivity / dig pattern in [`handlers.py`](../../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- [x] Backlog §Подзадачи lists T00–T07 aligned with pipeline (IDs + one-line purpose)
- [x] Stale absolute line cites refreshed (or replaced with stable anchors / symbols)
- [x] No invent new product scope; docs-only
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-03-t10.md` signed (Date post P6 verify only)

## Where to change
- [`backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md`](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md)
- Optionally pipeline [`STORY-GW-ES-03-public-emerging-l2-read.md`](../STORY-GW-ES-03-public-emerging-l2-read.md) if same stale cites present

## Out of scope
- post-Done observation rewrite (T08); gap-analysis Public=Y (T09); `src/` / OpenAPI; ES-07/ES-08 implementation

## Verification commands
```bash
rg -n 'Подзадачи|T00|T07|asgi_app.py:427|handlers.py:772' \
  doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/STORY-GW-ES-03-public-emerging-l2-read.md
rg -n '@app.get\("/tallinn/issues"\)|StoryActivityService|issue_create_service\.issue_story_link' \
  doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py
```
