# OP-gateway.process.md — REQ9-01…02 wave

Mirror of working plan: [`.cursor/plans/OP-gateway-req9-01-02-20260926.plan.md`](../../../../../.cursor/plans/OP-gateway-req9-01-02-20260926.plan.md)

**Role:** Operator root orchestrate only. No product code. No invent AC. No push unless operator ordered.

## Model

- Titles: `OP-gateway` / `BLD-gateway` / `VAL-gateway`
- Delivery: subagent (exactly two agents: Builder + Validator)
- Overnight: on — auto-approve P1.3b/P5b GATE; no pause after story
- Wave halt ONLY on explicit `стоп|stop|pause|halt`
- Agent ids: **never** in this file — live only in `OP-gateway.session.yaml`

## Overnight non-stop

| Rule | Behavior |
|------|----------|
| Stop | operator `стоп`/`stop`/`pause`/`halt` only |
| P1.3a→b / P5a→b | OP auto-approve immediately |
| After P8/DONE/BLOCKED | next QUEUED story immediately |
| Verify FAIL | BLOCKED + next |
| P8 | local commit, **no push** |

## Constants (profile gateway)

| Variable | Value |
|----------|--------|
| `$builderProject` | `gateway` |
| `workspace_root` | `/Users/eslinko/Development/DOGEstonia` |
| `$tasksRoot` | `doge-complaints-gateway/docs/tasks` |
| `$planFile` | `.cursor/plans/Gateway_builder.plan.md` |
| `$verifyCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify` |
| contract | `docs/methodology/Zeya888-builder-queue/contracts/gateway-operator-contract.md` |
| dashboard (contract) | `doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md` |
| `$backlogIndex` | `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/INDEX.md` |
| skill | `python-pro` |
| P1.3 variant | clean `p13` (`hasUxPipeline: false`) |
| git stay | `dev` (SSR merged into local `dev` 2026-09-26; no return to semantic-schema-runtime) |
| P8 push | forbidden |

## Queue

| # | Id | Path | Status at wave start |
|---|----|------|----------------------|
| 1 | REQ9-01 | `…/STORY-GW-REQ9-01-example-env-and-spa-base-url.md` | QUEUED |
| 2 | REQ9-02 | `…/STORY-GW-REQ9-02-make-test.md` | QUEUED |

Constraints: hard cut SPA_BASE_URL; no dual-read SPA_VERIFY_*; make test offline + test-live; no invent CI/Railway service ids.

## Plan-sim + ROLE_LOCK

Variant 1: P1.3a/b and P5a/b = two calls; OP auto-approve overnight.

```text
ROLE_LOCK: Execute ONLY the fence below. RETURN_TO_ROOT: paths + ≤5 lines facts. Do not advance phases yourself.
```

## Phase script

| Step | Who | Action |
|------|-----|--------|
| 0 G0 | OP shell | stay branch; wave MD |
| 0b/0c | OP→agents | resume/spawn BLD+VAL |
| P1.3a | OP→BLD | console P1.3 + PLAN_DRAFT |
| GATE | OP auto | overnight |
| P1.3b | OP→BLD | PLAN_APPLY + verify |
| P2 | OP shell | `$verifyCmd` + `--write-build-window` |
| P3 | OP→BLD | console P3 `@attach` `$planFile` |
| P4 | OP→VAL | console P4 RO |
| P5a/b | OP→BLD | if gaps; auto-approve |
| P6 | OP→BLD | console P6 |
| P7 | OP→VAL | console P7 RO |
| P8 | OP→BLD | console P8 no push |

## Wave

[wave-20260926-req9-01-02.md](../operator-waves/wave-20260926-req9-01-02.md)
