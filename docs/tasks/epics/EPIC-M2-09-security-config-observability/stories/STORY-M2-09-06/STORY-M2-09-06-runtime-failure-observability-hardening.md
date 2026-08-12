# STORY-M2-09-06: Runtime failure observability and log diagnostics hardening

## Meta
- Key: `STORY-M2-09-06`
- Parent Epic: [`../../../EPIC-M2-09-security-config-observability.md`](../../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: In Progress
- Stream: M2 Runtime Log Diagnostics
- Requirement reference: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Analysis reference: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

## Story Goal
Закрыть `GAP-LOG-01..05` для точной локализации runtime падений по логам intake -> cluster -> issue без повторного воспроизведения инцидента.

## AC / DoD
- [x] AC-LOG-01: глобальные runtime исключения логируются структурно с `trace_id/story_id/stage/stack`.
- [x] AC-LOG-02: cron run имеет коррелируемые start/end события и агрегированные метрики цикла.
- [x] AC-LOG-03: ошибки persistence слоя (Supabase) фиксируются в унифицированном событии с HTTP-диагностикой.
- [x] AC-LOG-04: intake завершает pipeline единым outcome событием по story.
- [x] AC-LOG-05: shutdown источник (`SIGINT`/`SIGTERM`/other) логируется явно.

## Nested tasks

| Order | Slug | Task folder |
|-------|------|-------------|
| 1 | primary | `task-m2-09-06-log-observability-primary` |
| 2 | T01 | `task-m2-09-06-t01-gap-log-01-global-exception-trace` |
| 3 | T02 | `task-m2-09-06-t02-gap-log-02-cron-run-correlation` |
| 4 | T03 | `task-m2-09-06-t03-gap-log-03-supabase-request-failed` |
| 5 | T04 | `task-m2-09-06-t04-gap-log-04-story-pipeline-outcome` |
| 6 | T05 | `task-m2-09-06-t05-gap-log-05-shutdown-reason` |

## Task Artifacts
- primary: [`./task-m2-09-06-log-observability-primary/README.md`](./task-m2-09-06-log-observability-primary/README.md)
- T01: [`./task-m2-09-06-t01-gap-log-01-global-exception-trace/README.md`](./task-m2-09-06-t01-gap-log-01-global-exception-trace/README.md)
- T02: [`./task-m2-09-06-t02-gap-log-02-cron-run-correlation/README.md`](./task-m2-09-06-t02-gap-log-02-cron-run-correlation/README.md)
- T03: [`./task-m2-09-06-t03-gap-log-03-supabase-request-failed/README.md`](./task-m2-09-06-t03-gap-log-03-supabase-request-failed/README.md)
- T04: [`./task-m2-09-06-t04-gap-log-04-story-pipeline-outcome/README.md`](./task-m2-09-06-t04-gap-log-04-story-pipeline-outcome/README.md)
- T05: [`./task-m2-09-06-t05-gap-log-05-shutdown-reason/README.md`](./task-m2-09-06-t05-gap-log-05-shutdown-reason/README.md)
- Acceptance (story): [`./task-m2-09-06-log-observability-primary/acceptance-verification-STORY-M2-09-06.md`](./task-m2-09-06-log-observability-primary/acceptance-verification-STORY-M2-09-06.md)
- Phase log (story): [`./task-m2-09-06-log-observability-primary/BULLRUN-PHASE-LOG.md`](./task-m2-09-06-log-observability-primary/BULLRUN-PHASE-LOG.md)
