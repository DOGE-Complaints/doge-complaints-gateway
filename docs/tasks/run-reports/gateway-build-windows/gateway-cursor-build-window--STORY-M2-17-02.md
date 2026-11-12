---
generated_utc: 2026-05-17T10:26:59Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000017-20260517-req38-data-integrity-issue-links.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-17-02
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-17-02

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38/task-m2-17-02-t01-living-issues-extend-e2e-test/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38/task-m2-17-02-t02-issue-story-links-story-index/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38/task-m2-17-02-t03-supabase-linkage-lookup-semantics/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38/task-m2-17-02-t04-arweave-txid-validation/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38/task-m2-17-02-t05-req38-acceptance-tests/README.md`
