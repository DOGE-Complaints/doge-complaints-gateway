---
generated_utc: 2026-08-06T21:08:44Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000056-20260806-gw-draft-07-hosted-schema-blocks-browser-submit.yaml
window_mode: flat_slice
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 6
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## Плоский срез 1–6 (как в --list)
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t01-hosted-readiness-table-inventory/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t02-apply-story-labels-text-fk-ddl/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t03-redeploy-gateway-clear-deps-cache/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t04-verify-ready-schema-db-ready/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t05-browser-submit-smoke-and-evidence/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/task-gw-draft-07-t06-story-acceptance-gate/README.md`

