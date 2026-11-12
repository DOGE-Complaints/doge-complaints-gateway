---
generated_utc: 2026-10-15T12:00:35Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ57-03
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ57-03
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t01-sweep-eligible-query/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t02-sense-brief-cron-job/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t03-asgi-cron-wire/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t04-ready-no-alpha-overwrite/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t05-sweep-tests/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t06-story-gate/README.md`

