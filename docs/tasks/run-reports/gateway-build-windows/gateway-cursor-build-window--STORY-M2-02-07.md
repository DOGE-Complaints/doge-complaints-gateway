---
generated_utc: 2026-05-15T09:29:01Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000012-20260513-req33-multilingual-intake-v2.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-02-07
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-02-07

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/task-m2-02-07-t01-intake-contract-v2-parse-and-validation/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/task-m2-02-07-t02-domain-storyrecord-v2-fields/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/task-m2-02-07-t03-api-raw-body-idempotency-sha256/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/task-m2-02-07-t04-persistence-stories-v2-columns/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-07-multilingual-intake-contract-v2/task-m2-02-07-t05-tests-and-wire-contract-docs/README.md`
