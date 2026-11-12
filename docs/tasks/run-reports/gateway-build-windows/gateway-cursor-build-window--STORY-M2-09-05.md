---
generated_utc: 2026-05-08T12:09:21Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000009-20260508-m2-09.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-09-05
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-09-05

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-trace-observability-primary/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t01-gap-trace-00-loglevel-apply/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t03-gap-trace-01-startup-config-log/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t04-gap-trace-07-configure-logging-module/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t05-gap-trace-02-03-intake-supabase-trace/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace/README.md`
8. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t07-gap-trace-08-per-story-file-log/README.md`
