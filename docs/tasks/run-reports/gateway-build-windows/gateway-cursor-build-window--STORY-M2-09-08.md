---
generated_utc: 2026-05-28T11:55:08Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000025-20260528-req45-production-logging-noise-reduction.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-09-08
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-09-08
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-08-production-logging-noise-reduction-req45/task-m2-09-08-t01-logging-setup-stdout-stderr-split-and-httpx-httpcore-suppress/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-08-production-logging-noise-reduction-req45/task-m2-09-08-t02-logging-setup-tests-handler-split-update/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-08-production-logging-noise-reduction-req45/task-m2-09-08-t03-production-logging-docs-quickstart-guidance/README.md`

