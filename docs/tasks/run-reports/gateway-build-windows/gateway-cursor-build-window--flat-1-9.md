---
generated_utc: 2026-06-19T21:10:00Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml
window_mode: flat_slice
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 9
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## Плоский срез 1–9 (как в --list)
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t01-adr-column-schema-and-view-decision/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t02-schema-migration-doge-issues-columns/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t03-write-path-save-projection-columnar/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t04-read-path-and-filters-columnar/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t05-three-backend-parity-supabase-sqlite-inmemory/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t06-issues-dashboard-view-columnar/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t07-data-migration-drop-payload-json/README.md`
8. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t08-contract-tests-and-reproject-script/README.md`
9. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t09-story-acceptance-gate/README.md`

