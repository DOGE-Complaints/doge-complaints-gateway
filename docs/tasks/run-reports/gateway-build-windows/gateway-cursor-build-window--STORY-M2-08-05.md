---
generated_utc: 2026-05-16T07:11:49Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000014-20260515-req35-geo-scope-node-architecture.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-08-05
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-08-05

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t01-story-geo-snapshot-admin-levels/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t02-geo-provider-stubs-admin-fields/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t03-persistence-geo-snapshot-jsonb/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t04-config-cluster-geo-scope-and-filter/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t05-cluster-engine-geo-filter/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t06-intake-geo-scope-rejection/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-05-geo-scope-node-architecture-and-filtering/task-m2-08-05-t07-tests-req35-acceptance/README.md`
