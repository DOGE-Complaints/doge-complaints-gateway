---
generated_utc: 2026-05-17T08:07:43Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000016-20260516-req37-pipeline-observability-pii-safety.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-09-07
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-09-07

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t01-redact-pii-api-logging/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t02-story-debug-logger-jsonl/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t03-services-intake-debug-logger/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t04-geo-signals-debug-stages/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t05-cluster-promotion-debug-stages/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-07-pipeline-observability-and-pii-safety/task-m2-09-07-t06-tests-req37-acceptance/README.md`
