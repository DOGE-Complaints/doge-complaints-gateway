# task-gw-ssr-35-t08-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for backlog/INDEX/T01 SSOT (G1)

## Meta
- **Story:** [STORY-GW-SSR-35](../STORY-GW-SSR-35-schema-root-url-pack-refresh.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000092 (parent product AC Done); wave `run_mode=gw_ssr_35_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-SSR-35
- **Depends on:** T01–T07 Done (product AC / G35 PASS)
- **Audit ref:** [`audit-gw-ssr-35-schema-root-url-pack-refresh-2026-09-07.md`](../../../../../../analysis/audit-gw-ssr-35-schema-root-url-pack-refresh-2026-09-07.md) **G1**
- **Scaffolded:** 2026-09-07T08:58:54Z
- **Completed:** 2026-09-07T08:58:54Z
- **Gate Date:** 2026-09-07T08:58:54Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-35_gap_20260907T085854Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog/INDEX/T01 Code Facts still present-tense «no URL / deferred / later». Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen product code unless drift.

## Code Facts
1. Audit G1 — backlog §Verified / Meta / AC checkboxes + INDEX D-SSR-12 deferred prose + T01 Code Facts stale.
2. Live product — `SCHEMA_ROOT_URL` / `SCHEMA_PACK_REFRESH` in `schema.py` + `remote_fetch.py`; G35 PASS; 12 tests.
3. **As-of-Done (P6):** SSOT split — G1 CLOSED 2026-09-07T08:58:54Z.
4. Pointer stays pkg-000092; G35 PASS 2026-09-07T08:54:22Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 / deferred only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Meta/AC Claims): As-of-Done vs Historical
- [x] INDEX D-SSR-12 / deferred prose aligned (35 shipped)
- [x] T01 Code Facts As-of-Done
- [x] T07 product gate **не** reopen
- [x] Product code/tests/manuals not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000092
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-35-t08.md` signed

## Where to change
- Backlog SSR-35 §Verified / Meta / AC checkboxes
- INDEX D-SSR-12 + deferred rows
- T01 README Code Facts
- Bullrun T08 row + P5/P6 registry (P6)

## Out of scope
Product reopen; invent registry; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000092 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|SCHEMA_ROOT_URL' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md
rg -n 'SSR-35 later|deferred' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md || true
```
