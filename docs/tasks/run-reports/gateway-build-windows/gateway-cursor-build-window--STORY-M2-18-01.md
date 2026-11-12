---
generated_utc: 2026-05-18T10:26:38Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
executed_utc: 2026-05-18
execution_result: PASS
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-18-01
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-18-01 — выполнено

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/task-m2-18-01-t01-zone-l-issue-projection-store-contract/README.md` — Done
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/task-m2-18-01-t02-zone-m-filter-projection-rows-contract/README.md` — Done
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/task-m2-18-01-t03-zone-j-clustering-pipeline-contract/README.md` — Done
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/task-m2-18-01-t04-zone-k-geo-propagation-contract/README.md` — Done
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/task-m2-18-01-t05-zone-n-e2e-sandbox-full-pipeline/README.md` — Done

**Story gate:** [`story-acceptance-gate-STORY-M2-18-01.md`](../../epics/EPIC-M2-18-cross-layer-contract-testing/stories/STORY-M2-18-01-cross-layer-contract-zones-j-n-req39/story-acceptance-gate-STORY-M2-18-01.md) — PASS (30 pytest).
