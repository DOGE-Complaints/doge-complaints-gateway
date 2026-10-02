# Analysis — Life-sim pack `stories.json` schema scarcity

| Field | Value |
|-------|--------|
| **utc** | `2026-10-02` |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — verified code/docs only |
| **Pack under study** | [`tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json`](../tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json) |
| **Context** | Pack created in a dialog started from [`life-sim-demo-node-load-manual-ru.md`](../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) |

## 1. Scope

Question: why does this pack’s `stories.json` have so few fields and not match the gateway Story / intake data model? At which layer does the scarcity arise — generator script, prompt, plan, or a combination?

Out of scope: fixing the generator, enriching packs, or changing load prompts/plans.

## 2. Observed pack shape (verified)

| Fact | Evidence |
|------|----------|
| Root type | JSON **array**, length **1661** |
| Keys per story (all rows identical) | `fixture_story_id`, `fixture_user_id`, `language`, `created_at`, `title`, `body` — **exactly 6** |
| Sample | `title` and `body` both `"Waste bins overflow and smell."` |
| `title == body[:72]` | **1661 / 1661** |
| Unique `body` strings | **15** (hardcoded civic blurbs et/ru/en) |
| Companion `meta.json` | `seed: 20260929`, `schema_note: "on-disk life-sim fixtures; not a public API contract"`, scale locks matching REQ11-01 |
| Companion `users.json` | 200 rows × 3 keys: `fixture_user_id`, `display_name`, `preferred_language` |

Conclusion: this pack is **not** a serialized `StoryRecord`. It is the **REQ11-01 on-disk fixture** layout, placed under a dated pack directory.

## 3. Comparison: fixture vs intake vs persisted Story

### 3.1 On-disk life-sim fixture (pack / generator)

| Field | Present |
|-------|---------|
| `fixture_story_id` | yes |
| `fixture_user_id` | yes |
| `language` | yes |
| `created_at` | yes (ISO UTC string) |
| `title` | yes (truncated body) |
| `body` | yes (short blurb) |
| Geo / address | **no** |
| i18n title/description maps | **no** |
| taxonomy / labels / gpt_signals | **no** |
| institution / schema_binding / structured_payload | **no** |

### 3.2 Intake `Narrative` (product contract)

Source: [`src/core/intake/contracts.py`](../src/core/intake/contracts.py) `Narrative` — includes `original_text`, `language`, `title`/`description` (dict i18n), `session_language`, optional `location_query`, `canonical_type`, `canonical_labels`, `taxonomy`, `summary`, `institution`.

### 3.3 Persisted `StoryRecord` (domain)

Source: [`src/core/domain/contracts.py`](../src/core/domain/contracts.py) `StoryRecord` — `story_id`, envelope `schema_version`, `narrative_*`, submitter identity, lifecycle, timestamps, optional `geo`, origin, privacy, SSR binding / `structured_payload`, etc.

### 3.4 What the replay adapter fills

Source: [`life_sim_story_to_intake_payload`](../tests/sandbox/life_sim_replay_lib.py):

| Intake / later Story field | Source |
|----------------------------|--------|
| `narrative.original_text` | fixture `body` |
| `narrative.language` / `session_language` | fixture `language` |
| `narrative.title` / `description` (et/ru/en maps) | **synthesized** from same `title`/`body` string for all langs |
| `narrative.summary` | `{lang: body}` |
| `narrative.canonical_type` | hard-coded `"complaint"` |
| `narrative.canonical_labels` | `[]` |
| `narrative.location_query` | only if caller passes `location_query` (fixture has **no** geo field) |
| `origin.source` | `"simulation"` |
| `origin.conversation_id` | `fixture_story_id` |
| Submitter / lifecycle / geo snapshots | **not** in fixture; come from auth + gateway after stash→submit / backdate |

So: sparse pack → adapter expands to a **minimal** intake envelope → gateway persists a fuller `StoryRecord`. Field parity was never required at pack level.

## 4. Causal stack (ranked)

### Rank 1 — Generator script (primary)

[`tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py`](../tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py):

- Docstring: *“Fixture schema is on-disk only — no invent public API field names for intake.”*
- Story construction writes only the six keys above; `title: body[:72]`; body from `BLURBS[lang]` (5 lines × 3 langs = 15).
- Goals of generation: **scale** (200 users, ~1661 stories), **lang mix**, **2026 date curve** — not narrative richness or StoryRecord isomorphism.

`meta.json` in the pack matches this generator (`seed` 20260929, same `schema_note` / `relation_to_canvas`). Pack content is that fixture output under `life_sim_packs/<pack_id>/`.

### Rank 2 — REQ11-01 intentional contract

[`STORY-GW-REQ11-01-fixtures-users-stories-scale.md`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md):

- AC locked on scale / langs / calendar curve.
- Explicit: *“No invent public APIs (`fixture_*` keys on-disk only).”*
- Success was never “pack JSON ≡ StoryRecord columns.”

### Rank 3 — Replay adapter (amplifies, does not invent richness)

Adapter maps the six fixture keys into intake narrative fields. It does **not** invent geo, taxonomy, or gpt_signals from the pack. Scarcity in → minimal narrative out (plus defaults).

### Rank 4 — Prompt / plan / load manual (non-causes of schema; policy),

| Artifact | Role re story fields |
|----------|----------------------|
| [`life-sim-node-load-run.md`](../../../docs/methodology/Zeya888-builder-queue/prompts/architect/life-sim-node-load-run.md) | Interview `story_foci`; warns Partial if foci ≠ Present fixtures; **does not emit** rich story JSON |
| [`Life_sim_load.plan.md`](../../../.cursor/plans/Life_sim_load.plan.md) | Orchestrates wipe / 08 / 10 / 09; **does not define** fixture schema |
| Load manual §4 / §4.5 | `story_foci` = guiding; Present fixtures/generator = load source; Partial on mismatch |

Interview params do **not** drive a second generator that writes Story-shaped JSON. After **STORY-GW-REQ11-07 removed**, there is no pack-gen story that materializes interview-rich texts into pack files.

### Rank 5 — Operator CLIs 08 / 09 / 10 (orthogonal)

- **08** provision: Auth users from pack `users.json` + wave-state — does not author story fields.
- **10** replay: submits existing pack `stories.json` — does not enrich schema.
- **09** threads: seeds issues after cluster — does not touch story fixture shape.

## 5. Combination answer

| Layer | Creates scarcity? |
|-------|-------------------|
| Generator (REQ11-01) | **Yes — root cause** |
| REQ11-01 AC / “on-disk only” policy | **Yes — intentional** |
| Replay adapter | **Preserves** scarcity into a thin intake map |
| Prompt / plan / manual | **No** field authorship; allow Partial when interview ≫ blurbs |
| Dialog that created the pack dir | Likely **copied/regenerated** generator output into `life_sim_packs/…`; did not invent a StoryRecord dump |
| Story / intake **product model** | Different layer — filled after submit, not mirrored in pack |

**Combination:** scarcity = **generator + intentional fixture contract**, with **adapter** as the bridge and **docs/prompt** documenting Partial rather than requiring field parity.

## 6. Implications for operators

- Expect **short repeated civic blurbs**, not unique LLM narratives per row.
- Expect **no geo / taxonomy / signals** in pack JSON; add them only via product intake paths or a **future** explicit enrich/gen wave (not Present).
- If interview `story_foci` / `node_social_direction` are richer than the 15 blurbs → treat load as **Partial** per manual/prompt (honest outcome).
- Comparing pack JSON to `StoryRecord` / full `Narrative` will always look “poor” until a new fixture contract is designed and implemented.

## 7. Related paths

- Generator: `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py`
- Adapter: `tests/sandbox/life_sim_replay_lib.py` → `life_sim_story_to_intake_payload`
- Pack: `tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/`
- Story AC: `docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-*.md`
- Load SSOT: `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md`
- **Backlog successor (richness):** [`STORY-GW-REQ11-11`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) (fixture contract v2) → [`STORY-GW-REQ11-12`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) (generator+adapter); **07 removed** — do not reuse
