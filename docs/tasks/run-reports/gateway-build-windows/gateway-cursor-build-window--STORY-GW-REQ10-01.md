---
generated_utc: 2026-09-28T17:13:25Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ10-01
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ10-01
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t01-db-distinct-inventory/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t02-fixture-sqlite-scan/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t03-closed-list-normalize-note/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t04-story-gate/README.md`

