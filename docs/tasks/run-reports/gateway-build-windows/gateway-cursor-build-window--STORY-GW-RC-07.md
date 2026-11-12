---
generated_utc: 2026-07-10T09:50:27Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000038-20260622-gw-rc-07-hosted-tallinn-issues-internal-error.yaml
window_mode: story_key
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-GW-RC-07
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## STORY-GW-RC-07
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t01-reproduce-and-collect-hosted-evidence/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t02-deploy-version-parity-vs-local-rc/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t03-per-row-read-probe-seven-incident-issues/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t04-fix-hosted-read-path-root-cause/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t05-story-acceptance-gate/README.md`

