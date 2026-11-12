---
generated_utc: 2026-08-10T12:12:27Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000060-20260810-gw-es-03-public-emerging-l2-read.yaml
window_mode: flat_slice
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 8
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## Плоский срез 1–8 (как в --list)
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t00-path-payload-mvp-l2-rule-gate/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t01-emerging-signals-service/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t02-di-factory-api-deps/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t03-public-get-handler/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t04-normative-emerging-ne-issues/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t05-unit-http-issues-regression/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t06-runtime-docs-openapi/README.md`
8. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t07-story-acceptance-gate/README.md`

