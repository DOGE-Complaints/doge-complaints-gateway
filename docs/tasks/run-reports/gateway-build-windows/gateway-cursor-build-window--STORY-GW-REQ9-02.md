---
generated_utc: 2026-09-26T12:19:50Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ9-02
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ9-02
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t01-make-test-offline/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t02-make-test-live/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t03-story-gate/README.md`

