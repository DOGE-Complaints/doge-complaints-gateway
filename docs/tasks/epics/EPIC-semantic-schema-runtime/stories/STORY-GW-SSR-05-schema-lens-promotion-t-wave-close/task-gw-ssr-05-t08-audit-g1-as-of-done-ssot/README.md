# task-gw-ssr-05-t08-audit-g1-as-of-done-ssot

## Meta
- **Story:** [STORY-GW-SSR-05](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000065 (parent product Done); wave `run_mode=gw_ssr_05_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-05
- **Depends on:** T01–T07 Done
- **Audit ref:** [`audit-gw-ssr-05-schema-lens-promotion-t-wave-close-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-05-schema-lens-promotion-t-wave-close-2026-08-28.md) **G1**
- **Scaffolded:** 2026-08-28T15:07:56Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-05_gap_20260828T150610Z.plan.md` G1 TASKED follow_up=none

## Purpose
As-of-Done vs Historical split для persistent SSOT: backlog + pipeline SSR-05 §Verified / §Стыковка still present-tense pre-P3 (pack policy «Not found»; always civic gates; «сейчас всегда `self.gate_policy`»; CLUSTERED cite `:369`) **and** INDEX Promotion / knobs (`_create_issue` / `submit_for_review` always civic) + civic orchestrator «return None» + membership-vs-Issue «without Issue/`CLUSTERED`». Cite live mapper + per-call override + pack CLUSTERED. Без runtime pack/civic. Без identity handlers.

## Code Facts
- Pack mapper — [`pack_policy.py`](../../../../../../../src/core/schema/pack_policy.py) `promotion_gate_policy_from_pack`
- Optional command override — [`issue_create.py:36`](../../../../../../../src/core/application/issue_create.py) `gate_policy`; submit [`service.py:85`](../../../../../../../src/core/promotion/service.py) `effective_policy`
- Pack CLUSTERED — [`cluster_orchestrator.py:138–216`](../../../../../../../src/core/application/cluster_orchestrator.py) `_promote_pack_membership`; lifecycle [`:191`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic default / factory unchanged — [`gates.py:14`](../../../../../../../src/core/promotion/gates.py); [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py)
- Stale backlog §Verified — split applied (As-of-Done vs Historical) in [`STORY-GW-SSR-05`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- Stale backlog §Стыковка — As-of-Done cites `effective_policy` / CLUSTERED `:188–193`; Historical keeps always `self.gate_policy` / `:369`
- Stale pipeline copy — split applied (same) in [`pipeline`](../STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- INDEX Promotion / knobs + civic orchestrator + membership-vs-Issue — As-of-Done SSR-05 in [`INDEX.md:107–108,114,117`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- Product Status 🔵 Done; gate PASS 2026-08-28T15:00:08Z

## Acceptance / DoD
- [x] Backlog SSR-05 §Verified: Current (mapper exists; optional `gate_policy`; pack CLUSTERED after promote) vs Historical (pre-P3 «Not found» / always civic gates)
- [x] Backlog SSR-05 §Стыковка: As-of-Done (`effective_policy`; CLUSTERED cite `:188–193`) vs Historical (present-tense always `self.gate_policy`; cite `:369`)
- [x] Pipeline SSR-05 §Verified / §Стыковка: same split (keep in sync with backlog)
- [x] INDEX Promotion / knobs + civic orchestrator + membership-vs-Issue: As-of-Done pack promote (not revert to Historical-only)
- [x] No `src/` / civic enum / cron / pack runtime / identity handler edits
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-05-t08.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` (§Verified current state + §Стыковка)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md` (§Verified current state + §Стыковка)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` (Promotion / knobs / civic orchestrator / membership-vs-Issue seams)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- G3 identity 503 order-flake (WAIVED reason=out-of-DoD; D-SSR-3)
- Runtime pack promote / civic factory / `CLUSTERED` logic
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :108–111).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.
- SSR-05 extras: no new pkg; current.yaml stays pkg-000065; no second cron; no QRY.

## Verification commands
```bash
rg -n 'Not found|always civic|сейчас всегда `self.gate_policy`|:369' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md
rg -n 'promotion_gate_policy_from_pack|effective_policy|_promote_pack_membership' \
  doge-complaints-gateway/src/core/schema/pack_policy.py \
  doge-complaints-gateway/src/core/promotion/service.py \
  doge-complaints-gateway/src/core/application/cluster_orchestrator.py
rg -n 'always civic|всегда `self.gate_policy`|return None|without Issue' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
```
