# STORY-GW-REQ11-11 — Life-sim `stories.json` fixture contract v2 (Narrative-aligned)

## Meta
- **Key:** `STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-02T08:53:45Z · gate PASS · docs-only contract · pkg-000109
- **Тип:** fixtures / contract docs — on-disk pack `stories.json` v2 vs intake Narrative
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 GW-11-01/02 (scale locks stay; content contract expands)
- **decision_ref:** backlog REQ11-11 · scarcity analysis 2026-10-02 · REQ11-01 scale locks · Narrative intake · **07 removed**
- **Justification:** [`../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md); [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md)
- **Siblings:** soft REQ11-01 (6-key Done); successor implement **REQ11-12**; soft REQ11-10 (replay reads pack)
- **Skill declared:** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml`](../../../../gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml)
- **Git:** `dev`
- **Operator locks:** scale unchanged (200 / Gauss 8.5·σ2.0·[1,20] / langs 60/30/10 / 2026 curve); pack JSON **≠** dump of `StoryRecord`; flat v2 keys; no LLM; **do not reuse** REQ11-07; next keys **11**, then **12**
- **Зависит от:** soft REQ11-01 Done; scarcity analysis Present
- **Blocks:** STORY-GW-REQ11-12 (generator+adapter implement against this contract)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Contract note:** [`../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md)
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Эта story = **contract docs**; реализация = **12**
- **Scaffolded:** 2026-10-02T08:51:14Z
- **Completed:** 2026-10-02T08:53:45Z

## Nested tasks (pkg-000109)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-11-t01-fixture-v2-flat-keys-contract`](./task-gw-req11-11-t01-fixture-v2-flat-keys-contract/README.md) | ✅ Done |
| T02 | [`task-gw-req11-11-t02-out-of-fixture-and-scale-locks`](./task-gw-req11-11-t02-out-of-fixture-and-scale-locks/README.md) | ✅ Done |
| T03 | [`task-gw-req11-11-t03-mapping-note-fixture-to-narrative`](./task-gw-req11-11-t03-mapping-note-fixture-to-narrative/README.md) | ✅ Done |
| T04 | [`task-gw-req11-11-t04-compat-partial-vs-v2-pass`](./task-gw-req11-11-t04-compat-partial-vs-v2-pass/README.md) | ✅ Done |
| T05 | [`task-gw-req11-11-t05-story-gate`](./task-gw-req11-11-t05-story-gate/README.md) | ✅ Done |
| T06 | [`task-gw-req11-11-t06-audit-g2-as-of-done-ssot`](./task-gw-req11-11-t06-audit-g2-as-of-done-ssot/README.md) | ✅ Done (P6 G2 CLOSED 2026-10-02T08:58:23Z) |

---

## Goal

Зафиксировать **on-disk fixture contract v2** для pack `stories.json` и таблицу mapping **fixture → intake [`Narrative`](../../../../../src/core/intake/contracts.py)** так, чтобы successor (REQ11-12) мог эмитить/читать богатые строки без dump runtime `StoryRecord` и без LLM.

---

## Scope

1. **Layout lock (одна раскладка):** **flat keys** на строке `stories.json` (mirroring today’s adapter inputs + expansions). **Не** nest under `narrative` for v2 Pass (avoid dual layouts).
2. **Required join / schedule (compat with 01/10):**
   - `fixture_story_id`, `fixture_user_id`, `created_at`, `language`
3. **Narrative-aligned content (names = intake semantics; fixture may use flat aliases):**
   - Compat: `title`, `body` (keep; adapter today reads these)
   - i18n: `title_i18n`, `description_i18n`, `summary_i18n` — maps `et` / `ru` / `en`
   - `session_language`, `location_query`, `canonical_type`, `canonical_labels`
   - optional: `institution_i18n` (→ intake `institution`)
4. **Explicit out of fixture v2:**
   - `story_id`, lifecycle, `submitter_*`, `payload_hash`
   - invent taxonomy **axis IDs**
   - invent `gpt_signals` as fake classifier (omit from v2 AC unless later story)
5. **Compatibility:** old **6-key** rows still load via thin path (**Partial**); v2 rows = **Pass** for richness gates once 12 Done.
6. **Docs deliverable (P3 target path — name ≠ create here):** note under `docs/analysis/` named for mapping fixture v2 → Narrative (exact filename lock in P3, e.g. `note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-*.md`).

## Out of scope

- Implementing generator or adapter (→ **REQ11-12**).
- LLM / inventing story texts.
- Changing UX of REQ11-08 / 09 / 10 CLIs.
- Regenerating existing pack JSON in this story.
- Reopening REQ11-01 Done as rewrite-in-place without successor.
- Dumping full `StoryRecord` into pack.

---

## Verified current state (As-of-Done P3 2026-10-02T08:53:45Z)

| Fact | Evidence |
|------|----------|
| Fixture contract v2 note Present | [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) |
| Flat layout + join + content keys | note §1–3 · AC-01 |
| Out-of-fixture + scale + ≠ StoryRecord | note §5–6 · AC-02/05 |
| Mapping table | note §4 · AC-03 |
| Compat Partial / v2 Pass | note §7 · AC-04 |
| Pack on disk still 6-key | `ls-20260930T0938Z-veerenni-yard-construction/stories.json` len 1661 |
| Gate | [`story-acceptance-gate-STORY-GW-REQ11-11.md`](./task-gw-req11-11-t05-story-gate/story-acceptance-gate-STORY-GW-REQ11-11.md) PASS |
| Run summary | [`run-summary-20261002-0853-gw-req11-11-p3.md`](../../../../run-reports/run-summary-20261002-0853-gw-req11-11-p3.md) |

## Verified current state (Historical scaffold 2026-10-02 / pre-P3)

| Fact | Evidence |
|------|----------|
| Pack rows = **6 keys** only | scarcity analysis §2; pack len 1661 |
| Generator emits 6-key + BLURBS | `generate_dogestonia_life_sim_fixtures_v0_1.py` |
| Adapter synthesizes thin Narrative | `life_sim_story_to_intake_payload` |
| Contract note / v2 SSOT | **Absent** (pre-P3) |
| REQ11-07 removed | INDEX / EPIC — do not reuse **07** |

### Mapping table (contract — documented in P3 note)

| Fixture v2 flat key | Intake Narrative / envelope |
|---------------------|------------------------------|
| `body` | `original_text` (and/or prefer `description_i18n[language]`) |
| `language` | `language` |
| `session_language` | `session_language` (default = `language` if absent) |
| `title` / `title_i18n` | `title` i18n map |
| `description_i18n` | `description` |
| `summary_i18n` | `summary` |
| `location_query` | `location_query` |
| `canonical_type` | `canonical_type` |
| `canonical_labels` | `canonical_labels` |
| `institution_i18n` | `institution` |
| `fixture_story_id` | `origin.conversation_id` (via adapter; not Narrative field) |
| `created_at` | backdate path (REQ11-04); not Narrative |

---

## Target / AC

- [x] **AC-GW-REQ1111-01:** Written fixture contract v2: required join keys + Narrative-aligned flat content keys; layout = **flat** (locked).
- [x] **AC-GW-REQ1111-02:** Explicit **out of fixture** list: no `story_id` / lifecycle / submitter / invent taxonomy axis IDs / invent `gpt_signals` in v2 AC.
- [x] **AC-GW-REQ1111-03:** Mapping table fixture → intake Narrative documented in named analysis note (P3 path).
- [x] **AC-GW-REQ1111-04:** Compatibility stated: 6-key rows = load Partial / thin adapter path; v2 = Pass richness once 12 implements.
- [x] **AC-GW-REQ1111-05:** Scale locks from REQ11-01 unchanged; pack ≠ `StoryRecord` dump restated.

## Code touchpoints (As-of-Done — cite only; no implement in this story)

- Contract note: `docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md` (**Present**)
- Generator (v0_1 6-key still on disk): `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py`
- Adapter (thin Partial path): `tests/sandbox/life_sim_replay_lib.py` → `life_sim_story_to_intake_payload`
- Intake: `src/core/intake/contracts.py` → `Narrative`
- Domain (out of fixture): `src/core/domain/contracts.py` → `StoryRecord`
- Pack example (6-key): `tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json`
- Load params (guiding, not schema SSOT): pack `params.json` / manual §4 (`story_foci`, `node_social_direction`, `neighbourhood_tags`)

### Historical (scaffold «named only» / pre-P3)

- Contract note under `docs/analysis/` — **Absent** (acceptance target only)

## Dependencies

- Soft: **REQ11-01** Done (scale + 6-key baseline).
- Soft: scarcity analysis Present.
- Soft: **REQ11-10** Done (replay must keep reading pack; contract must not break join keys).
