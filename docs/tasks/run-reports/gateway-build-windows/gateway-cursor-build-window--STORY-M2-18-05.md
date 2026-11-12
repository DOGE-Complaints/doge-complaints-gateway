---
generated_utc: 2026-05-18T13:01:04Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-18-05
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-18-05

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-05-live-integration-ci-req41/task-m2-18-05-t20-gap41-05-live-integration-ci/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-05-live-integration-ci-req41/task-m2-18-05-t21-ac41-8-testing-architecture-doc/README.md`
