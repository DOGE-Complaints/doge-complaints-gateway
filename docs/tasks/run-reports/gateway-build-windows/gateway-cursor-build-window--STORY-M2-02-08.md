---
generated_utc: 2026-05-23T08:28:31Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000022-20260522-req42-gpt-signals-story-intake.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-02-08
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-02-08
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-08-gpt-signals-intake-persistence-req42/task-m2-02-08-t01-intake-contract-gpt-signals/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-08-gpt-signals-intake-persistence-req42/task-m2-02-08-t02-story-intake-service-signals-persist/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-08-gpt-signals-intake-persistence-req42/task-m2-02-08-t03-gpt-signals-intake-acceptance-tests/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-08-gpt-signals-intake-persistence-req42/task-m2-02-08-t04-runtime-openapi-api-reference/README.md`

