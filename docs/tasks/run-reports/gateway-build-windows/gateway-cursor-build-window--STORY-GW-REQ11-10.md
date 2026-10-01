---
generated_utc: 2026-10-01T11:33:07Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ11-10
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ11-10
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t01-fail-closed-pack-dir-readonly-stories/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t02-wave-state-checkpoint-resume/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t03-cli-make-reuse-replay-bearer/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t04-offline-unit-tests/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t05-ru-manual-replay-pack-wave/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t06-story-gate/README.md`

