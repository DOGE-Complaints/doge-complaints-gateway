---
generated_utc: 2026-09-21T20:19:31Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000093-20260921-gw-thr-01-active-pack-verification-and-shell-knobs.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-THR-01
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-THR-01
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t01-shell-capability-contract/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t02-fail-closed-active-pack/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t03-migrate-activatable-packs/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t04-tests-pack-shell-required/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t05-story-gate/README.md`

