# task-gw-es-02-t08-audit-r1-post-done-observation

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000059 (parent Done); wave `run_mode=gw_es_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-ES-02
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md`](../../../../../../analysis/audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md) **R1**
- **Scaffolded:** 2026-08-10T11:32:43Z
- **Closed:** 2026-08-10T11:45:42Z

## Purpose
Убрать present-tense pre-Done claims в backlog + pipeline §«Что наблюдаю»: «No public pulse», «ApiDependencies — нет pulse». Пометить блок historical **или** заменить post-Done verified таблицей (route + DI + service).

## Code Facts
- Stale backlog — [`STORY-GW-ES-02` backlog](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) §Что наблюдаю (No public pulse; нет pulse service)
- Stale pipeline — [`STORY-GW-ES-02-….md`](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) same section
- Fact: `PUBLIC_ROUTES` + `/tallinn/network-pulse` — [`asgi_app.py:65`](../../../../../../../../src/core/api/asgi_app.py)
- Fact: `network_pulse_service` — [`dependencies.py`](../../../../../../../../src/core/api/dependencies.py)
- Meta Status = Done (Awaiting Commits) gate PASS 2026-08-10T10:55:48Z

## Acceptance / DoD
- [x] Backlog + pipeline: §«Что наблюдаю» не утверждает отсутствие route/DI as current
- [x] Post-Done verified table **или** explicit «Контекст до реализации (исторический)» + post-Done block
- [x] Cite live paths: `GET /tallinn/network-pulse`, `NetworkPulseService`, `ApiDependencies.network_pulse_service`
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t08.md` signed (Date post P6 verify only)

## Where to change
- [`backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md`](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- [`STORY-GW-ES-02-public-network-pulse-l1-aggregates.md`](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) (pipeline)

## Out of scope
- gap-analysis (T09); epic/dashboard/REQ/openapi (T10); `src/` changes; audit working-doc body

## Verification commands
```bash
rg -n 'No public pulse|нет pulse service' \
  doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-02-public-network-pulse-l1-aggregates/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md
# present-tense absence claims should be gone or only under historical label
rg -n 'network-pulse|network_pulse_service' doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/dependencies.py
```
