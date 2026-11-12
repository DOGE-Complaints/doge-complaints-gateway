---
generated_utc: 2026-05-08T13:03:38Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000010-20260508-m2-09.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-09-06
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-09-06

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-log-observability-primary/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-t01-gap-log-01-global-exception-trace/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-t02-gap-log-02-cron-run-correlation/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-t03-gap-log-03-supabase-request-failed/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-t04-gap-log-04-story-pipeline-outcome/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/task-m2-09-06-t05-gap-log-05-shutdown-reason/README.md`
