# task-gw-cab-01-t07-audit-r1-backlog-story-sync

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** docs (audit follow-up)
- **Status:** 🟢 Done
- **Package:** pkg-000052 (audit follow-up; **run_mode override**, no pkg change)
- **Skill declared:** python-pro
- **Audit report:** [`docs/analysis/audit-gw-cab-01-story-activity-api-2026-07-13.md`](../../../../../../analysis/audit-gw-cab-01-story-activity-api-2026-07-13.md)
- **Gap ID:** R1 (MEDIUM)

## Purpose
Устранить doc-drift в backlog-стори `GW-CAB-01`: сейчас она выглядит как **pass-1 постановка** с «открытыми вопросами» и утверждениями `not implemented`, хотя pipeline и код уже **Done (Awaiting Commits)** (pkg-000052, T01–T06).

## Code Facts (SSOT, verified)
1) Backlog-стори всё ещё `⚪ Todo (pass-1)` и содержит «Открытые вопросы» и «Pass-2 (не здесь)`.
   - `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-01-story-activity-api.md`
2) Pipeline-стори отражает реальность: статус **🔵 Done (Awaiting Commits)** и решения D-CAB01-1..4 закрыты.
   - `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-01-story-activity-api/STORY-GW-CAB-01-story-activity-api.md`
3) Bullrun индекс фиксирует проблему как audit R1: backlog-стори устарела при реализованной pass-2.
   - `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md` (EPIC-M2-22 / GW-CAB-01 row содержит ⚠️ R1)
4) Audit SSOT: R1 описывает конкретно «glyph/status + body stale» и рекомендует синхронизацию backlog-стори.
   - `doge-complaints-gateway/docs/analysis/audit-gw-cab-01-story-activity-api-2026-07-13.md` §2 R1

## Gap
- **R1 (MEDIUM):** backlog-стори `GW-CAB-01` осталась в состоянии pass-1 (и содержит устаревшие утверждения), хотя реализация сделана.

## AC/DoD
- [x] Backlog-стори `STORY-GW-CAB-01-story-activity-api.md` больше не утверждает «не реализовано» там, где реализовано
- [x] Удалены/свернуты устаревшие секции «Открытые вопросы (решить в pass-2)» и «Pass-2 (не здесь)»
- [x] Вместо дублирования добавлен явный pointer на pipeline story + решения D-CAB01-1..4
- [x] Backlog meta-status отражает реальность (Done/Awaiting Commits) либо помечен как `superseded by pipeline copy` (без расхождения смыслов)
- [x] `bullrun-launch-index.md` обновлён: TASK-GW-CAB-01-T07 закрывает audit R1
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t07.md`](./acceptance-verification-gw-cab-01-t07.md) signed (Date post live-run only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-01-story-activity-api.md`
- `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/INDEX.md` (если статус/прогресс требует синхронизации)
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md`

## Out of scope
- Любые изменения runtime кода / тестов / OpenAPI (это уже выполнено в pkg-000052)

## Verification commands (post live-run only)
```bash
rg -n \"STORY-GW-CAB-01|pass-1|pass-2|Открытые вопросы\" doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/STORY-GW-CAB-01-story-activity-api.md
rg -n \"R1|GW-CAB-01\" doge-complaints-gateway/docs/analysis/audit-gw-cab-01-story-activity-api-2026-07-13.md
```

