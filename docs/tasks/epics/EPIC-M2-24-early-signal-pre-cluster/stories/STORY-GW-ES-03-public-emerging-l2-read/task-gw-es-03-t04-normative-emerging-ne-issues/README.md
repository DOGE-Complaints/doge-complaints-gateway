# task-gw-es-03-t04-normative-emerging-ne-issues

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** docs / contract
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** T01 (logic exists or designed); soft T00
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
Норматив Topic≠Issue / anti threshold / Emerging ≠ Issues projection; clustering gates unchanged (parent §33). Prepare contract assertions for T05.

## Code Facts
- Issues L3 source — `IssueProjectionReadStore.list_projections` / `GET /tallinn/issues`
- Emerging source — labels + exclude published (MVP rule) — **not** projections list
- Pulse topics disposition — [`is_public_label_disposition`](../../../../../../../../src/core/taxonomy/disposition.py) (reuse discipline for public labels if applicable)
- Cluster gates — do not edit `CLUSTER_MIN_SIZE` / promotion

## Acceptance / DoD
- [ ] Traces AC: Topic≠Issue; no threshold-gaming; clustering unchanged; response distinct from Issues (contract design)
- [ ] Normative notes in REQ/ADR and/or runtime-docs stub pointers (full OpenAPI = T06)
- [ ] Explicit «Emerging ≠ Issues list shape/source» for T05 tests
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t04.md` signed (Date post P3 verify only)

## Where to change
- T00 REQ/ADR normative section; optional short note in API_REFERENCE (full path docs = T06)
- Test plan bullets consumed by T05

## Out of scope
- Implementing pytest (T05); changing cluster math; spa UX

## Verification commands
```bash
rg -n 'Emerging|Topic|threshold|CLUSTER_MIN_SIZE' doge-complaints-gateway/docs/requirements/ doge-complaints-gateway/docs/runtime-docs/api-reference/ | head -30
```
