# task-gw-cab-02-t07-audit-r1-backlog-story-sync

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** docs (audit follow-up)
- **Status:** 🟢 Done
- **Package:** pkg-000053 (audit follow-up; **run_mode override**, no pkg change)
- **Skill declared:** python-pro
- **Audit report:** [`docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md`](../../../../../../analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md)
- **Gap ID:** R1 (MEDIUM)

## Purpose
Устранить doc-drift в backlog-стори `GW-CAB-02`: сейчас она `⚪ Todo` с устаревшим body («Что наблюдаю» pre-impl, unchecked AC), хотя pipeline и код **Done (Awaiting Commits)** (pkg-000053, T01–T06).

## Code Facts (SSOT, verified)
1) Backlog meta `⚪ Todo (pass-2 углублён)` и stale pre-impl sections.
   - `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-02-current-draft-discovery.md:6`
2) Pipeline story **Done (Awaiting Commits)** + AC checked; gate PASS 2026-07-14.
   - `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-02-current-draft-discovery/STORY-GW-CAB-02-current-draft-discovery.md`
3) Audit R1: backlog glyph/body не синхронизированы с Done (рецидив CAB-01 R1).
   - `doge-complaints-gateway/docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md` §2 R1

## Gap
- **R1 (MEDIUM):** backlog-стори `GW-CAB-02` осталась pass-1/Todo при реализованной pass-2.

## AC/DoD
- [ ] Backlog meta-status → Done (Awaiting Commits) + SSOT pointer на pipeline/pkg-000053
- [ ] Удалены/свернуты устаревшие «Что наблюдаю сейчас» (pre-impl claims) и unchecked AC — заменены pointer на pipeline
- [ ] `cabinet-api/INDEX.md` синхронизирован при необходимости
- [ ] `bullrun-launch-index.md`: TASK-GW-CAB-02-T07 закрывает audit R1
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-cab-02-t07.md`](./acceptance-verification-gw-cab-02-t07.md) signed (Date post live-run only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-02-current-draft-discovery.md`
- `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/INDEX.md`
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md`

## Out of scope
- Runtime код / тесты / OpenAPI (уже в pkg-000053)

## Verification commands (post live-run only)
```bash
rg -n "Todo|pass-2|Что наблюдаю" doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-02-current-draft-discovery.md
rg -n "R1|GW-CAB-02" doge-complaints-gateway/docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md
```
