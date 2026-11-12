# STORY-GW-SSR-33 — Node-specific taxonomy: docs, setup, usage, test hygiene

## Meta
- **Key:** `STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** Done (Awaiting Commits) pkg-000090 · G33 PASS 2026-09-04T13:28:42Z
- **Приоритет:** P1 — node-taxonomy wave (sequence **33**)
- **Тип:** docs / operator setup / cross-test inventory (no loader logic)
- **Architecture SSOT:** [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) (**D-SSR-11**)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md)
- **Skill declared:** code-documenter
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** **SSR-31 + SSR-32** Done (wording must match shipped behaviour)
- **Blocks:** operator onboarding clarity for node taxonomy; GPT-SSR-15 invert handoff
- **Parallel:** none (after 31+32)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

# Layer 1 — Постановка задачи

## Зачем простыми словами

После смены runtime (31/32) документация и операторские инструкции всё ещё говорят «ровно 13 осей». Нужен единый пакет: README, manual, setup/usage, инвентарь тестов, и явный handoff что GPT Pack Builder meta (GPT-SSR-15) надо **инвертировать**, иначе meta снова затолкает lockstep.

## Scope

- Rewrite Contour2 axes contract in pack README + operator manual taxonomy sections.
- Operator setup/usage: how to author node axes; tallinn = exemplar.
- Cross-story test inventory (what 31 vs 32 own).
- INDEX already lists wave — keep sync; point to arch-doc.
- Note gap handoff must link arch + 31…33 (edit may already exist from planning wave — verify/align).
- Sibling: document that GPT-SSR-15 must be superseded/inverted (do **not** edit GPT file in this story unless operator expands scope).

## Out of scope

- Resolver / `normalize_axis` code (31/32).
- uus pack.json civic/exact repair.
- Implementing GPT meta schema changes.

## Short AC (Layer 1)

- [x] **AC-GW-SSR33-01:** README no longer requires set-equality to 13.
- [x] **AC-GW-SSR33-02:** Manual describes node-defined axes + Contour1/2 dual contour under D-SSR-11.
- [x] **AC-GW-SSR33-03:** Test inventory documents 31/32 ownership.
- [x] **AC-GW-SSR33-04:** GPT-SSR-15 conflict recorded for GPT wave.

---

# Layer 2 — Реализация (техническая проработка)

## Verified as-built (pre-docs P3) → As-of-Done (post-P3 / G33)

| Doc / area | Evidence |
|------------|----------|
| [`schema-packs/README.md`](../../../../schema-packs/README.md) | **As-of-Done:** axes node-defined (D-SSR-11); lockstep only negated. **Historical:** L44 must ∈ frozen set / equal all 13. |
| Manual [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) | **As-of-Done:** §D-SSR-11 dual contour + Authoring 1–6 + GPT-SSR-15 invert note. **Historical:** SSR-29 dual contour without node-axes authoring. |
| SSR-26 / SSR-29 stories | Done AC text may still say lockstep 13 — **Historical** story bodies; prefer README+manual+INDEX (not rewritten). |
| GPT-SSR-15 | Sibling invert recorded on gateway (INDEX/manual); GPT wave executes — **As-of-Done** handoff only. |
| Gap handoff | **As-of-Done:** taxonomy lockstep obsolete; Contour2/1 As-of-Done. **Historical:** taxonomy listed as load blocker. |

## Touch list (P3)

| Path | Change |
|------|--------|
| [`schema-packs/README.md`](../../../../schema-packs/README.md) | Replace axes row; mention D-SSR-11 / arch-doc; keep dispositions / internal / maps |
| [`docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) | Taxonomy dual-contour chapter: node axes; Contour1 open; civic skip; tallinn exemplar; setup steps |
| [`INDEX.md`](./INDEX.md) | Node-taxonomy section already expected from planning — ensure arch link + 31–33 status |
| Optional appendix stub | Short «Authoring node taxonomy» subsection in manual (not new REQ) |
| This story body | Test inventory table below — keep as living checklist |

## Operator setup / usage (must land in manual)

1. Choose axes for the node (domain language).
2. Fill `canonical_keys` + `axis_to_signal_map` consistently.
3. Set `taxonomy_schema` in pack.json when Contour2 needed.
4. Wire GPT taxonomy may use same axis ids (after SSR-32).
5. Do not invent ClusterLens ids from axis names.
6. Copy tallinn taxonomy only as starting point — trim/extend freely.

## Test inventory (hygiene)

| Area | Owner story | Notes |
|------|-------------|-------|
| Contour2 load N-axes / structural fails | SSR-31 | `test_gw_ssr_26_*` / `test_gw_ssr_31_*` / SSR-28 seed content |
| Contour1 wire custom axis | SSR-32 | `test_gw_ssr_32_*` |
| Docs-only | SSR-33 | No pytest required beyond link/grep sanity if desired |
| uus pack.json readiness/civic | **Not** 31–33 | Separate repair |

## Concrete AC (P3 gate)

- [x] **AC-GW-SSR33-01:** README `taxonomy.json` table: axes = node-defined; no «must equal all 13»; link arch-doc.
- [x] **AC-GW-SSR33-02:** Manual §taxonomy updated for D-SSR-11 (Contour1 open + Contour2 pack-owned + civic skip + tallinn exemplar + setup steps).
- [x] **AC-GW-SSR33-03:** INDEX node-taxonomy section lists 31–33 + arch-doc + D-SSR-11.
- [x] **AC-GW-SSR33-04:** Explicit note (INDEX or manual or this story Related): GPT-SSR-15 must be superseded/inverted to free axes + structural checks (gateway wins).
- [x] **AC-GW-SSR33-05:** Gap handoff [`uus-veerenni-…-2026-09-04.md`](../../../analysis/uus-veerenni-civic-v1-gateway-load-blockers-handoff-2026-09-04.md) links arch + SSR-31…33 and treats taxonomy lockstep as obsolete post-31 (verify on Done).

## DoD

- Docs consistent with shipped 31/32; no code changes in 33 unless typo in comments; analysis.mdc — no invented APIs.

## Claims (Layer 2)

**As-of-Done:** Docs wave landed; G33 PASS 2026-09-04T13:28:42Z (pkg-000090); G1 CLOSED P6 2026-09-04T13:34:49Z.  
**Historical:** README L44 lockstep verified pre-P3; docs P3 not started until after 31/32 runtime.
