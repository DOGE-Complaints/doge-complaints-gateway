---
generated_utc: 2026-05-17T19:51:52Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000019-20260518-req24-tallinn-issues-read-api.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-06-06
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-06-06

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t01-issue-projection-read-store-protocol/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t02-inmemory-read-store-list-get/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t03-sqlite-supabase-read-store/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t04-factory-di-read-store-wiring/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t05-handlers-tallinn-issues-and-manual-create/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t06-routes-cors-public-tallinn-issues/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t07-extended-filters-geo-time-institution/README.md`
8. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/task-m2-06-06-t08-req24-acceptance-tests-and-openapi/README.md`
