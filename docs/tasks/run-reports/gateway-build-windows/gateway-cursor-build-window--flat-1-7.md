---
generated_utc: 2026-07-11T07:46:39Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000049-20260711-gw-draft-05-dual-intake-contract-stash-vs-submit.yaml
window_mode: flat_slice
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 7
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## Плоский срез 1–7 (как в --list)
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t01-domain-stash-request-bridge-and-cleanup/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t02-handlers-stash-submit-intake-wiring/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t03-intake-v2-fixtures-stash-payload/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t04-contract-and-draft-regression-tests/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t05-runtime-openapi-stash-schema/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t06-runtime-docs-dual-path-ssot/README.md`
7. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/task-gw-draft-05-t07-backlog-index-sync/README.md`

