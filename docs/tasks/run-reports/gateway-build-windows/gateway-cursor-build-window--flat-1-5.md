---
generated_utc: 2026-08-07T09:59:11Z
builder_project: gateway
gateway_input_package: doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000058-20260807-gw-tax-03-align-story-labels-migration-text-fk.yaml
window_mode: flat_slice
artifact_kind: gateway_cursor_build_window
pkg_schema_version: 1
---

# Gateway Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `gateway_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --window-flat-start 1 --window-flat-end 5
```

После **последнего** README в **полной** story в пакете — **Story parent AC**; после всех story эпика — **Epic AC** — см. [`m2-epic-story-execution-pipeline.md`](../../m2-epic-story-execution-pipeline.md) (Gate: Story parent AC, Gate: Epic AC). Срез по плоскому диапазону (`--window-flat-*`) может обрезать story: не пропускайте story-gate.

## Плоский срез 1–5 (как в --list)
1. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/task-gw-tax-03-t01-inventory-dual-path/README.md`
2. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/task-gw-tax-03-t02-align-migration-text-fk/README.md`
3. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/task-gw-tax-03-t03-rls-grant-parity-bootstrap/README.md`
4. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/task-gw-tax-03-t04-docs-index-elegance-note/README.md`
5. `@doge-complaints-gateway/docs/tasks/epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/task-gw-tax-03-t05-story-acceptance-gate/README.md`

