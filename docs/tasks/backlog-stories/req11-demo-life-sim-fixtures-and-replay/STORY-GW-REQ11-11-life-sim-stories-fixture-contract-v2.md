# STORY-GW-REQ11-11 — Life-sim `stories.json` fixture contract v2 (Narrative-aligned)

## Meta
- **Key:** `STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-02T08:53:45Z · gate PASS · P6 G2 CLOSED 2026-10-02T08:58:23Z · backlog kept
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- **Тип:** fixtures / contract docs — on-disk pack `stories.json` v2 vs intake Narrative
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 GW-11-01/02 (scale locks stay; content contract expands)
- **Justification:** [`analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md); [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md)
- **Siblings:** soft REQ11-01 (6-key Done); successor implement **REQ11-12**; soft REQ11-10 (replay reads pack)
- **Skill declared (future P3):** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator locks:** scale unchanged (200 / Gauss 8.5·σ2.0·[1,20] / langs 60/30/10 / 2026 curve); pack JSON **≠** dump of `StoryRecord`; **do not reuse** REQ11-07; next keys **11**, then **12**
- **Зависит от:** soft REQ11-01 Done; scarcity analysis Present
- **Blocks:** STORY-GW-REQ11-12 (generator+adapter implement against this contract)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** note path / mapping table ниже — **acceptance targets** до P3; этот файл **не** materialize generator/adapter/pack regen
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Эта story = **contract docs**; реализация = **12**
- **Scaffolded:** 2026-10-02T08:45:00Z

---

## Goal

Зафиксировать **on-disk fixture contract v2** для pack `stories.json` и таблицу mapping **fixture → intake [`Narrative`](../../../../src/core/intake/contracts.py)** так, чтобы successor (REQ11-12) мог эмитить/читать богатые строки без dump runtime `StoryRecord` и без LLM.

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

## Verified current state (As-of-Done P3 2026-10-02T08:53:45Z · P6 G2 2026-10-02T08:58:23Z)

| Fact | Evidence |
|------|----------|
| Fixture contract v2 note **Present** | [`note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md`](../../../analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) |
| Flat layout + join + content keys | note §1–3 · AC-01 |
| Out-of-fixture + scale + ≠ StoryRecord | note §5–6 · AC-02/05 |
| Mapping table fixture → Narrative | note §4 · AC-03 |
| Compat: 6-key **Partial** / v2 **Pass** (once 12) | note §7 · AC-04 |
| Pack on disk still **6-key** | `ls-20260930T0938Z-veerenni-yard-construction/stories.json` len **1661**; keys `body,created_at,fixture_story_id,fixture_user_id,language,title` |
| Gate / run-summary | pipeline gate PASS 2026-10-02T08:53:45Z · [`run-summary-20261002-0853-gw-req11-11-p3.md`](../../run-reports/run-summary-20261002-0853-gw-req11-11-p3.md) |
| REQ11-01 scale locks Done | [`STORY-GW-REQ11-01-…`](./STORY-GW-REQ11-01-fixtures-users-stories-scale.md) |
| REQ11-07 removed | INDEX / EPIC — do not reuse **07** |

## Verified current state (Historical — scaffold / pre-P3 2026-10-02)

| Fact | Evidence |
|------|----------|
| Pack rows = **6 keys** only | [`analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](../../../analysis/analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md) §2; pack len 1661 |
| Generator emits 6-key + BLURBS | [`generate_dogestonia_life_sim_fixtures_v0_1.py`](../../../../tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py) — `title` = `body[:72]` |
| Adapter synthesizes thin Narrative | [`life_sim_story_to_intake_payload`](../../../../tests/sandbox/life_sim_replay_lib.py) — copies `title`/`body` into all-lang maps |
| Intake Narrative fields | [`src/core/intake/contracts.py`](../../../../src/core/intake/contracts.py) `Narrative` |
| StoryRecord ≠ fixture | [`src/core/domain/contracts.py`](../../../../src/core/domain/contracts.py); scarcity §3.3 |
| Contract note / v2 SSOT | **Absent** (pre-P3; mapping table was backlog target only) |
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
- Pack example (6-key Historical content): `tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json`
- Load params (guiding, not schema SSOT): pack `params.json` / manual §4 (`story_foci`, `node_social_direction`, `neighbourhood_tags`)

### Historical (scaffold «named only» / pre-P3)

- Contract note path under `docs/analysis/` — **Absent** (acceptance target only)
- Mapping table — backlog-only until P3 note

## Dependencies

- Soft: **REQ11-01** Done (scale + 6-key baseline).
- Soft: scarcity analysis Present.
- Soft: **REQ11-10** Done (replay must keep reading pack; contract must not break join keys).

## Related

- Pipeline: [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md)
- Successor: [`STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md`](./STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- Epic: [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- INDEX: [`./INDEX.md`](./INDEX.md)
