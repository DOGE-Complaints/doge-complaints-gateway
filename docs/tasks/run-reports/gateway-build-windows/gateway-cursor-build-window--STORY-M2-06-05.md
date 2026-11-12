---
generated_utc: 2026-05-17T19:23:04Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000018-20260517-req40-geo-propagation-issue-projection.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-06-05
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-06-05

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t01-projection-input-geo-fields/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t02-doge-issue-geo-subobject/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t03-mapper-geo-projection/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t04-extraction-policy-geo-snapshot/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t05-issue-create-bridge-dominant-geo/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/task-m2-06-05-t06-req40-acceptance-tests/README.md`
