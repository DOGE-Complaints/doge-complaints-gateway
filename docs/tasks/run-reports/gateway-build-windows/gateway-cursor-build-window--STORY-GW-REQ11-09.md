---
generated_utc: 2026-10-01T10:48:30Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ11-09
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ11-09
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t01-fail-closed-empty-issues-gate/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t02-cli-make-thin-wrapper/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t03-secrets-actors-handoff-seed/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t04-offline-unit-tests/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t05-ru-manual-threads-seed/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t06-story-gate/README.md`

