---
generated_utc: 2026-05-23T10:29:57Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000023-20260523-req43-institution-json-story-column.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-02-09
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-02-09
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t01-intake-contract-narrative-institution/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t02-story-record-and-intake-mapping/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t03-story-store-institution-json-persistence/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t04-issue-projection-institution-propagation/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t05-institution-intake-acceptance-tests/README.md`
6. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/task-m2-02-09-t06-runtime-docs-openapi-persistence-model/README.md`

## P3 outcome (2026-05-23)

- Verify: `ok 6 paths` (pkg-000023)
- Tests: `pytest -q tests/test_institution_intake.py` → **7 passed**
- Story gate: PASS — [`story-acceptance-gate-STORY-M2-02-09.md`](../../epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-09-institution-json-story-column-req43/story-acceptance-gate-STORY-M2-02-09.md)
- Fix during build: `advance_story_readiness` now copies `narrative_institution`; sqlite INSERT placeholder count aligned to 36 columns

