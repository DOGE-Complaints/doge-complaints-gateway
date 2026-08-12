# task-gw-tax-01-t09-audit-r1-backlog-story-sync

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** docs (audit follow-up)
- **Status:** 🔵 Done
- **Package:** pkg-000054 (audit follow-up; **run_mode override**, no pkg change)
- **Skill declared:** python-pro
- **Audit report:** [`docs/analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md`](../../../../../../analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md)
- **Gap ID:** R1 (MEDIUM) — **Closed**

## Purpose
Устранить doc-drift в backlog-стори `GW-TAX-01`: сейчас она `⚪ Todo` с устаревшим body («Что наблюдаю» pre-impl, unchecked AC), хотя pipeline и код **Done (Awaiting Commits)** (pkg-000054, T01–T08, gate PASS 2026-07-14).

## Code Facts (SSOT, verified)
1) Backlog meta `⚪ Todo (pass-2 углублён … ждёт активации + GPT-TAX-01)` и stale pre-impl sections.
   - `doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md:6`
2) Pipeline story **Done (Awaiting Commits)** + AC checked; gate PASS 2026-07-14.
   - `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md:7`
3) Audit R1: backlog glyph/body не синхронизированы с Done (рецидив status-drift).
   - `doge-complaints-gateway/docs/analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md` §2 R1

## Gap
- **R1 (MEDIUM):** backlog-стори `GW-TAX-01` осталась pass-2/Todo при реализованной pass-2 (pkg-000054 Done). **Closed** 2026-07-15.

## AC/DoD
- [x] Backlog meta-status → Done (Awaiting Commits) + SSOT pointer на pipeline/pkg-000054
- [x] Удалены/свернуты устаревшие «Что наблюдаю сейчас» (pre-impl claims) и unchecked AC — заменены pointer на pipeline
- [x] `taxonomy-fidelity/INDEX.md` §Verified-факты синхронизирован (post-impl pointer, не pre-impl «story_labels нет»)
- [x] `bullrun-launch-index.md`: TASK-GW-TAX-01-T09 закрывает audit R1
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-01-t09.md`](./acceptance-verification-gw-tax-01-t09.md) signed (Date post live-run only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md`
- `doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/INDEX.md`
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md`

## Out of scope
- Runtime код / тесты / OpenAPI (уже в pkg-000054)
- GPT-TAX-01 producer (G1, cross-repo GPT UI)

## Verification commands (post live-run only)
```bash
rg -n "Todo|pass-2|Что наблюдаю" doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md
rg -n "R1|GW-TAX-01" doge-complaints-gateway/docs/analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md
```
