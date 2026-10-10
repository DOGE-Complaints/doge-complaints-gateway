---
generated_utc: 2026-10-10T15:57:38Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-REQ56-01
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-REQ56-01
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t01-d-s1-match-helper/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t02-post-fetch-filter-compose/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t03-asgi-handler-search-wire/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t04-unit-match-and-compose/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t05-asgi-handler-search-tests/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t06-story-gate/README.md`

