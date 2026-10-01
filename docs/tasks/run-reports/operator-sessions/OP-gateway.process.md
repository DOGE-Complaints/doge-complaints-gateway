# OP-gateway.process — mirror working plan (REQ11-10)

> **Working plan:** [`.cursor/plans/OP-gateway-req11-10-20261001.plan.md`](../../../../../.cursor/plans/OP-gateway-req11-10-20261001.plan.md)  
> **Session:** [OP-gateway.session.yaml](./OP-gateway.session.yaml)  
> **Wave:** [wave-20261001-req11-10.md](../operator-waves/wave-20261001-req11-10.md)  
> **No agent ids in this file.**

## Model

- Titles: `OP-gateway` / `BLD-gateway` / `VAL-gateway`
- Delivery: exactly two Task subagents; verbatim fences; no operator paste
- OP: orchestrate only — no product code, no invent AC, no push unless ordered
- Claims: Read/Glob only ([analysis.mdc](../../../../../.cursor/rules/analysis.mdc))

## Overnight

| Правило | Поведение |
|---------|-----------|
| Стоп | только `стоп` / `stop` / `pause` / `halt` |
| P1.3a→b / P5a→b | OP auto-approve |
| После P8 / DONE | next QUEUED (none after 10) |
| BLOCKED | fact in wave → next |
| P8 | local, **no push**; secrets never committed |

## Constants (gateway profile)

| Variable | Value |
|----------|--------|
| `$builderProject` | `gateway` |
| `$tasksRoot` | `doge-complaints-gateway/docs/tasks` |
| `$planFile` | `.cursor/plans/Gateway_builder.plan.md` |
| `focus_folder` | `doge-complaints-gateway` |
| `pipeline_doc` | `doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md` |
| `$verifyCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify` |
| contract | `docs/methodology/Zeya888-builder-queue/contracts/gateway-operator-contract.md` |
| dashboard | `doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md` |
| skill | `python-pro` |
| P1.3 | clean (`hasUxPipeline: false`) |
| stay | `dev` only |

## Queue

| # | Id | Path | Notes |
|---|----|------|-------|
| 1 | REQ11-10 | `…/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md` | pack-wave replay жалоб |

Queue count: **1**. mode: sequential. input_mode: backlog_story.

## Plan-sim + ROLE_LOCK

Variant 1: P1.3a/b and P5a/b = two Builder calls; overnight auto-approve.

```text
ROLE_LOCK: Execute ONLY the fence below. RETURN_TO_ROOT: paths + ≤5 lines facts. Do not advance phases yourself.
```

## Phase script

0 G0 stay `dev` → 0b/0c resume → P1.3a/b → P2 → P3 → P4 → P5a/b → P6 → P7 → P8 (no push) → STOP (queue exhausted).
