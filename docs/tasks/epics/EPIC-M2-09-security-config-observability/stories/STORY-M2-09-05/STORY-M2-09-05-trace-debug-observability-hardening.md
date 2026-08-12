# STORY-M2-09-05: Trace/debug observability hardening

## Meta
- Key: `STORY-M2-09-05`
- Parent Epic: [`../../../EPIC-M2-09-security-config-observability.md`](../../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: In Progress
- Stream: M2 Trace Observability
- Requirement reference: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Skill declared: `python-pro`

## Story Goal
Закрыть `GAP-TRACE-00..08` для сквозной DEBUG трассировки intake -> cluster -> issue с безопасным логированием и запуском через конфиг.

## AC / DoD
- [x] AC-TRACE-01: `LOG_LEVEL` применён к Python logging subsystem.
- [x] AC-TRACE-02: startup config log содержит ключевые runtime-поля.
- [x] AC-TRACE-03: intake/service/supabase trace покрывает create_story и save_story path.
- [x] AC-TRACE-04: cluster/geo/issue_create слои имеют DEBUG трассировку по ключевым этапам.
- [x] AC-TRACE-05: per-story файловый DEBUG log поддерживается через `LOG_DEBUG_DIR`.
- [x] AC-TRACE-06: PII safety соблюдён (`narrative_original_text` полностью не логируется).

## Nested tasks

| Order | Slug | Task folder |
|-------|------|-------------|
| 1 | primary | `task-m2-09-05-trace-observability-primary` |
| 2 | T01 | `task-m2-09-05-t01-gap-trace-00-loglevel-apply` |
| 3 | T02 | `task-m2-09-05-t02-gap-trace-00b-db-backend-supabase` |
| 4 | T03 | `task-m2-09-05-t03-gap-trace-01-startup-config-log` |
| 5 | T04 | `task-m2-09-05-t04-gap-trace-07-configure-logging-module` |
| 6 | T05 | `task-m2-09-05-t05-gap-trace-02-03-intake-supabase-trace` |
| 7 | T06 | `task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace` |
| 8 | T07 | `task-m2-09-05-t07-gap-trace-08-per-story-file-log` |

## Task Artifacts
- primary: [`./task-m2-09-05-trace-observability-primary/README.md`](./task-m2-09-05-trace-observability-primary/README.md)
- T01: [`./task-m2-09-05-t01-gap-trace-00-loglevel-apply/README.md`](./task-m2-09-05-t01-gap-trace-00-loglevel-apply/README.md)
- T02: [`./task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md`](./task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md)
- T03: [`./task-m2-09-05-t03-gap-trace-01-startup-config-log/README.md`](./task-m2-09-05-t03-gap-trace-01-startup-config-log/README.md)
- T04: [`./task-m2-09-05-t04-gap-trace-07-configure-logging-module/README.md`](./task-m2-09-05-t04-gap-trace-07-configure-logging-module/README.md)
- T05: [`./task-m2-09-05-t05-gap-trace-02-03-intake-supabase-trace/README.md`](./task-m2-09-05-t05-gap-trace-02-03-intake-supabase-trace/README.md)
- T06: [`./task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace/README.md`](./task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace/README.md)
- T07: [`./task-m2-09-05-t07-gap-trace-08-per-story-file-log/README.md`](./task-m2-09-05-t07-gap-trace-08-per-story-file-log/README.md)
- Acceptance (story): [`./task-m2-09-05-trace-observability-primary/acceptance-verification-STORY-M2-09-05.md`](./task-m2-09-05-trace-observability-primary/acceptance-verification-STORY-M2-09-05.md)
- Phase log (story): [`./task-m2-09-05-trace-observability-primary/BULLRUN-PHASE-LOG.md`](./task-m2-09-05-trace-observability-primary/BULLRUN-PHASE-LOG.md)
