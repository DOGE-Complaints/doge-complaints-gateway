# task-gw-es-03-t09-audit-r2-g3-gap-matrix-public-y

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060 (parent Done); wave `run_mode=gw_es_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-ES-03
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-es-03-public-emerging-l2-read-2026-08-10.md`](../../../../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md) **R2** + **G3**
- **Scaffolded:** 2026-08-10T12:44:19Z
- **Closed:** 2026-08-11T09:53:23Z

## Purpose
Обновить gap-analysis inventory: L2 Emerging Public=**Y** с cite `GET /tallinn/emerging-signals` / REQ-50; G-ES-PUB-03 → Closed/Satisfied by ES-03. Закрыть **G3** (package INDEX опережает gap SSOT) выравниванием gap file с INDEX. Не reopen Issues L3 / Pulse L1.

## Code Facts
- Gap matrix L2 still Public=N — [`gap-analysis-…§3`](../../../../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md)
- G-ES-PUB-03 Open phrasing — same file §4
- INDEX already Public=Y / G-ES-PUB-03 Closed — [`INDEX.md`](../../../../backlog-stories/early-signal-pre-cluster/INDEX.md)
- Fact: public route — [`asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) `GET /tallinn/emerging-signals`
- REQ-50 Accepted — [`50-early-signal-emerging-l2-api.md`](../../../../../../requirements/50-early-signal-emerging-l2-api.md)
- ES-03 Done pkg-000060

## Acceptance / DoD
- [x] §3 L2 Emerging row Public=**Y** (or equivalent) + cite path / REQ-50
- [x] §4 G-ES-PUB-03 marked Closed/Satisfied by ES-03 (Awaiting Commits OK)
- [x] Related inventory lines that still say «no Emerging L2» updated or historical
- [x] G3 resolved: gap SSOT согласован с package INDEX (no INDEX↔gap contradiction)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-03-t09.md` signed (Date post P6 verify only)

## Where to change
- [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](../../../../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md)
- Optionally [`early-signal-pre-cluster/INDEX.md`](../../../../backlog-stories/early-signal-pre-cluster/INDEX.md) note if still inconsistent after gap fix

## Out of scope
- Story «Что наблюдаю» (T08); подзадачи/cites (T10); ES-03/Issues/Pulse runtime; inventing new paths

## Verification commands
```bash
rg -n 'Public today|G-ES-PUB-03|emerging-signals|Level 2|L2 Emerging' \
  doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/INDEX.md
```
