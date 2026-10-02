# STORY-GW-REQ11-12 — Life-sim rich `stories.json` generator + adapter (v2)

## Meta
- **Key:** `STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🟢 Done (P3 2026-10-02T09:10:26Z · gate PASS · pkg-000110)
- **Тип:** fixtures / tooling — deterministic rich pack stories + replay adapter
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 load pipeline (richer жалобы into gateway)
- **decision_ref:** backlog REQ11-12 · REQ11-11 contract v2 Present · scarcity 2026-10-02 · no LLM · pack dir SSOT · **07 removed**
- **Justification:** [`../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md); contract [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md)
- **Siblings:** soft **REQ11-11** Done; soft REQ11-01 scale; soft REQ11-10 pack-wave replay
- **Skill declared:** `python-pro` · soft `test-master`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml`](../../../../gateway-active-packages/pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml)
- **Git:** `dev`
- **Operator locks:** deterministic templates **no LLM**; keep REQ11-01 scale locks; write under `life_sim_packs/<pack_id>/` (not flat sandbox SSOT); **do not reuse** REQ11-07; diversity Pass = **≥ N unique bodies via composed templates** at locked story count (prefer full uniqueness over ≥90% ratio when templates allow)
- **Зависит от:** soft **REQ11-11** Done (contract v2); soft REQ11-10 (replay still loads pack)
- **Blocks:** operator load richness Pass vs interview Partial (manual note)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** generator rewrite / adapter / pack regen / tests ниже — **acceptance targets** до P3; P1 scaffold **не** materialize код
- **Note:** **STORY-GW-REQ11-07 removed** — не путать с pack-gen; эта story = successor generator+adapter after **11**
- **Contract note:** [`../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md)
- **Scaffolded:** 2026-10-02T09:02:38Z

## Nested tasks (pkg-000110)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-12-t01-generator-v2-emit-scale-locks`](./task-gw-req11-12-t01-generator-v2-emit-scale-locks/README.md) | 🟢 Done |
| T02 | [`task-gw-req11-12-t02-diversity-composed-templates`](./task-gw-req11-12-t02-diversity-composed-templates/README.md) | 🟢 Done |
| T03 | [`task-gw-req11-12-t03-params-json-foci-defaults`](./task-gw-req11-12-t03-params-json-foci-defaults/README.md) | 🟢 Done |
| T04 | [`task-gw-req11-12-t04-adapter-prefer-v2-keep-thin`](./task-gw-req11-12-t04-adapter-prefer-v2-keep-thin/README.md) | 🟢 Done |
| T05 | [`task-gw-req11-12-t05-offline-tests-schema-diversity-roundtrip`](./task-gw-req11-12-t05-offline-tests-schema-diversity-roundtrip/README.md) | 🟢 Done |
| T06 | [`task-gw-req11-12-t06-pack-dir-ssot-ops-docs-partial-to-pass`](./task-gw-req11-12-t06-pack-dir-ssot-ops-docs-partial-to-pass/README.md) | 🟢 Done |
| T07 | [`task-gw-req11-12-t07-story-gate`](./task-gw-req11-12-t07-story-gate/README.md) | 🟢 Done |
| T08 | [`task-gw-req11-12-t08-audit-g1-as-of-done-ssot`](./task-gw-req11-12-t08-audit-g1-as-of-done-ssot/README.md) | 🟢 Done (P6 G1 CLOSED) |

---

## Goal

После Done **REQ11-11** — реализовать generator (+ adapter) так, чтобы **новый** pack `stories.json` был **diverse** и **Narrative-complete per v2**; артефакт писать/ссылать под `life_sim_packs/<pack_id>/`; offline gates на schema + diversity + adapter round-trip; REQ11-10 smoke still reads pack.

---

## Scope

1. **Generator:** extend/replace output of [`generate_dogestonia_life_sim_fixtures_v0_1.py`](../../../../../tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py) (or successor writing into pack dir): emit **v2** fields per REQ11-11; keep scale/lang/2026 locks from REQ11-01.
2. **Diversity (deterministic, no LLM):** composed templates so Pass = **≥ N unique `body` strings** at locked story count N (e.g. N≈1661 at seed of record) **via composed templates**. If full uniqueness infeasible without LLM, document template cardinality floor in P3 note and Fall back to measurable ≥90% unique — **prefer full uniqueness** as Pass when feasible.
3. **Pack params:** consume optional pack `params.json` when Present: `story_foci` / `node_social_direction` / `neighbourhood_tags` (and themes blurbs if Present); **defaults** when empty (civic templates) — same guiding semantics as load manual §4.
4. **Adapter:** update [`life_sim_story_to_intake_payload`](../../../../../tests/sandbox/life_sim_replay_lib.py) to **prefer** v2 `title_i18n` / `description_i18n` / `summary_i18n` / `location_query` / `canonical_*` / `session_language` / `institution_i18n` when Present; keep thin path for 6-key rows. **No invent** public HTTP APIs.
5. **Output path:** write under `tests/sandbox/life_sim_packs/<pack_id>/` (`stories.json` + companions as needed); do **not** treat flat `*_v0_1` sandbox JSON as SSOT for new packs.
6. **Offline tests:** schema presence (v2 keys); diversity gates; adapter round-trip → valid stash narrative shape; smoke that REQ11-10 pack reader still accepts pack.
7. **Ops docs:** load-manual / note — Partial (6-key blurbs) → **Pass** when v2 pack used (honest outcome vs interview).

## Out of scope

- Live full fill / Identity Auth / threads seed.
- LLM story authorship.
- Inventing intake/submit HTTP.
- Changing 08/09 UX (except cross-link notes if needed).
- Implementing in the same turn as this backlog story (**name ≠ create**).
- Dumping `StoryRecord` / invent `gpt_signals` / invent taxonomy axis IDs (per 11 out-of-fixture).

---

## Verified current state (As-of-Done P3 2026-10-02T09:10:26Z · P6 G1 2026-10-02T09:15:08Z)

| Fact | Evidence |
|------|----------|
| Generator v2 + CLI **Present** | [`life_sim_stories_v2_lib.py`](../../../../../tests/sandbox/life_sim_stories_v2_lib.py) · [`generate_life_sim_pack_stories_v2.py`](../../../../../tests/sandbox/generate_life_sim_pack_stories_v2.py) |
| Unique bodies | **1661/1661** (full uniqueness; no LLM) |
| Adapter prefer v2 + thin 6-key | [`life_sim_story_to_intake_payload`](../../../../../tests/sandbox/life_sim_replay_lib.py); fail-closed Present |
| Contract v2 | REQ11-11 **Done** · [`note-gw-req11-11-…`](../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) Present |
| Ref pack v2 | `life_sim_packs/ls-20261002T0906Z-veerenni-v2-rich/` (+ `params.json`) |
| Offline tests | `test_gw_req11_12_…` + REQ11-10 → **15 passed** |
| Load-manual Partial→Pass | [`life-sim-demo-node-load-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) |
| Gate / run-summary | gate PASS 09:10:26Z · [`run-summary-20261002-0910-gw-req11-12-p3.md`](../../../../run-reports/run-summary-20261002-0910-gw-req11-12-p3.md) |
| Replay pack-wave | REQ11-10 Done |

## Verified current state (Historical — scaffold / P1 2026-10-02)

| Fact | Evidence |
|------|----------|
| Generator = 6-key + ~15 BLURBS | [`generate_dogestonia_life_sim_fixtures_v0_1.py`](../../../../../tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py) |
| Unique bodies in pack | **15** / 1661 — scarcity analysis §2 |
| Adapter thin synthesis only | [`life_sim_story_to_intake_payload`](../../../../../tests/sandbox/life_sim_replay_lib.py) (pre prefer-v2) |
| Contract v2 | REQ11-11 Done · note Present |
| Pack dir layout | `life_sim_packs/<pack_id>/` + `params.json` per load manual |
| Legacy 6-key pack | `ls-20260930T0938Z-veerenni-yard-construction` — Partial |

---

## Target / AC

- [x] **AC-GW-REQ1112-01:** Generator (or successor) emits fixture **v2** fields per REQ11-11; scale/lang/2026 locks preserved.
- [x] **AC-GW-REQ1112-02:** Diversity Pass — **≥ N unique bodies** via composed templates at locked N **or** documented floor + ≥90% with rationale; **no LLM**.
- [x] **AC-GW-REQ1112-03:** Optional `params.json` foci/tags consumed when Present; empty → defaults.
- [x] **AC-GW-REQ1112-04:** Adapter prefers v2 i18n / `location_query` / labels / session / institution; 6-key thin path remains.
- [x] **AC-GW-REQ1112-05:** Offline tests: schema, diversity, adapter round-trip; REQ11-10 pack read smoke.
- [x] **AC-GW-REQ1112-06:** New/reference pack under `life_sim_packs/<pack_id>/`; load-manual note Partial→Pass when v2 pack used.

## Code touchpoints (As-of-Done)

- v2 lib/CLI: `tests/sandbox/life_sim_stories_v2_lib.py` · `generate_life_sim_pack_stories_v2.py`
- Adapter: `tests/sandbox/life_sim_replay_lib.py` → `life_sim_story_to_intake_payload`
- Ref pack: `tests/sandbox/life_sim_packs/ls-20261002T0906Z-veerenni-v2-rich/`
- Offline: `tests/test_gw_req11_12_stories_v2_generator_adapter.py`
- REQ11-10 CLI/Make (smoke)
- Manual: `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md`

### Historical (scaffold / pre-P3)

- `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py` (6-key BLURBS; not SSOT for new packs)
- Legacy pack `ls-20260930T0938Z-veerenni-yard-construction`

## Dependencies

- Soft **REQ11-11** Done (contract + mapping note).
- Soft REQ11-01 scale locks.
- Soft REQ11-10 Done (replay).

## Related

- Backlog: [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- Predecessor: [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- Scarcity: [`../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md)
- Epic / INDEX: [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md) · [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
