---
generated_utc: 2026-08-29T19:10:16Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-SSR-11
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-SSR-11
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/task-gw-ssr-11-t00-pack-card-fields-contract/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/task-gw-ssr-11-t01-loader-card-allowlist/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/task-gw-ssr-11-t02-project-pack-issue-fields/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/task-gw-ssr-11-t03-tests-public-dict-no-dump/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-11-pack-declared-issue-projection/task-gw-ssr-11-t04-story-acceptance-gate/README.md`

