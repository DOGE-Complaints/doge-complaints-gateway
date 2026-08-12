# task-gw-es-03-t08-audit-r1-post-done-observation

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060 (parent Done); wave `run_mode=gw_es_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-ES-03
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-es-03-public-emerging-l2-read-2026-08-10.md`](../../../../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md) **R1**
- **Scaffolded:** 2026-08-10T12:44:19Z
- **Closed:** 2026-08-11T09:53:23Z

## Purpose
Убрать present-tense pre-Done claims в backlog + pipeline §«Что наблюдаю»: «No public emerging route»; Meta Gap «L2 Public=N»; §Зачем «публичного L2 read нет». Пометить блок historical **или** заменить post-Done verified таблицей (route + DI + service).

## Code Facts
- Stale backlog — [`STORY-GW-ES-03` backlog](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md) §Что наблюдаю / Meta Gap / §Зачем
- Stale pipeline — [`STORY-GW-ES-03-….md`](../STORY-GW-ES-03-public-emerging-l2-read.md) same class of claims
- Fact: `PUBLIC_ROUTES` + `/tallinn/emerging-signals` — [`asgi_app.py:67`](../../../../../../../../src/core/api/asgi_app.py)
- Fact: `emerging_signals_service` — [`dependencies.py`](../../../../../../../../src/core/api/dependencies.py); service [`emerging_signals.py`](../../../../../../../../src/core/application/emerging_signals.py)
- Meta Status = Done (Awaiting Commits) gate PASS 2026-08-10T12:17:38Z; REQ-50 Accepted

## Acceptance / DoD
- [x] Backlog + pipeline: §«Что наблюдаю» / Meta Gap / §Зачем не утверждают отсутствие Emerging route/DI as current
- [x] Post-Done verified table **или** explicit «Контекст до реализации (исторический)» + post-Done block
- [x] Cite live paths: `GET /tallinn/emerging-signals`, `EmergingSignalsService`, `ApiDependencies.emerging_signals_service`
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-03-t08.md` signed (Date post P6 verify only)

## Where to change
- [`backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md`](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md)
- [`STORY-GW-ES-03-public-emerging-l2-read.md`](../STORY-GW-ES-03-public-emerging-l2-read.md) (pipeline)

## Out of scope
- gap-analysis (T09); подзадачи/cites polish (T10); `src/` changes; audit working-doc body

## Verification commands
```bash
rg -n 'No public emerging|публичного L2 read нет|L2 Public=N' \
  doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/STORY-GW-ES-03-public-emerging-l2-read.md
# present-tense absence claims should be gone or only under historical label
rg -n 'emerging-signals|emerging_signals_service' doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/dependencies.py
```
