---
generated_utc: 2026-05-08T11:03:32Z
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000008-20260508-m2-16.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-16-02
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-M2-16-02

1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/task-m2-16-02-remote-simulation-primary/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/task-m2-16-02-t01-simulation-runner/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/task-m2-16-02-t02-env-test-template/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/task-m2-16-02-t03-single-command-launch/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/task-m2-16-02-t04-geo-location-query-coverage/README.md`
