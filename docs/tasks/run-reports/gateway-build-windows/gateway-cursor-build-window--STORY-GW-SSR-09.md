---
generated_utc: 2026-08-29T18:11:22Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000067-20260829-gw-ssr-09-hosted-apply-and-pack-image.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-SSR-09
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-SSR-09
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-09-hosted-apply-and-pack-image/task-gw-ssr-09-t01-hosted-sql-binding-migration/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-09-hosted-apply-and-pack-image/task-gw-ssr-09-t02-omit-probe-ready-invariants/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-09-hosted-apply-and-pack-image/task-gw-ssr-09-t03-packs-visible-to-resolver/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-09-hosted-apply-and-pack-image/task-gw-ssr-09-t04-story-acceptance-gate/README.md`

