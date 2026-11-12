# OP-gateway.process — SSOT mirror

**Working plan:** [`.cursor/plans/OP-gateway-req59-01-20261105.plan.md`](../../../../../.cursor/plans/OP-gateway-req59-01-20261105.plan.md)  
**Guide:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**NO agent ids in this file.**

## Model

- OP orchestrates only; BLD + VAL = exactly two Task subagents
- overnight=on · pause_after_story=false · auto_approve_plan=true
- halt only: стоп|stop|pause|halt
- P8 local no-push; stay `dev`
- Claims: Read/Glob only

## Overnight

| Rule | Behavior |
|------|----------|
| Wave halt | explicit stop only |
| P1.3b / P5b GATE | auto-approve |
| After DONE/BLOCKED | next QUEUED immediately |
| verify FAIL | BLOCKED → next |

## Constants

| Key | Value |
|-----|-------|
| builder_project | gateway |
| $tasksRoot | doge-complaints-gateway/docs/tasks |
| $planFile | .cursor/plans/Gateway_builder.plan.md |
| $verifyCmd | python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify |
| contract | docs/methodology/Zeya888-builder-queue/contracts/gateway-operator-contract.md |
| dashboard | doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md |
| skill | python-pro |
| hasUxPipeline | false |
| P1.3 | clean backlog_story |

## Queue

| # | Id | Path |
|---|----|------|
| 1 | REQ59-01 | doge-complaints-gateway/docs/tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md |

## Plan-sim + ROLE_LOCK

P1.3 / P5 = PLAN_DRAFT → auto GATE → PLAN_APPLY.  
Each Task prompt prepends ROLE_LOCK (reference §4.2).

## Phase script

0b/0c → P1.3a → GATE → P1.3b → P2 → P3 → P4 → [P5a→GATE→P5b→P6→P7] → P8 → STOP
