---
generated_utc: 2026-08-28T13:41:57Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000062-20260828-gw-ssr-02-structured-payload-persist.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-SSR-02
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-SSR-02
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t00-parent-persist-field-map/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t01-story-record-optional-fields/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t02-payload-hash/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t03-sqlite-alter-upsert/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t04-lifecycle-copy-replace/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t05-supabase-row-select/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t06-migration-bootstrap-alter/README.md`
8. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t07-unit-tests/README.md`
9. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-02-structured-payload-persist/task-gw-ssr-02-t08-story-acceptance-gate/README.md`

