# Note — GW-REQ11-11 life-sim `stories.json` fixture contract v2 → intake Narrative

| Field | Value |
|-------|--------|
| **utc** | `2026-10-02T08:52:55Z` |
| **Story** | STORY-GW-REQ11-11 · AC-GW-REQ1111-01…05 |
| **Package** | pkg-000109 |
| **Method** | disk facts only; docs contract — no generator/adapter implement (→ REQ11-12) |
| **Scarcity ref** | [`analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md`](./analysis-life-sim-pack-stories-schema-scarcity-2026-10-02.md) |

## Verdict

**Fixture contract v2** for on-disk pack `stories.json` is **flat keys only** (no nest under `narrative`). Join keys stay compatible with REQ11-01/10. Narrative-aligned content keys are named for intake semantics so REQ11-12 can emit/read rich rows **without** dumping runtime `StoryRecord` and **without** LLM. Current pack remains **6-key Partial** via thin adapter.

---

## 1. Layout lock (AC-01)

| Rule | Lock |
|------|------|
| Shape | JSON **array** of objects |
| Key layout | **Flat** on each row |
| Forbidden for v2 Pass | Nesting content under a `narrative` object (dual layouts) |

---

## 2. Required join / schedule keys (AC-01 · compat 01/10)

| Fixture flat key | Role |
|------------------|------|
| `fixture_story_id` | Stable fixture id; adapter → `origin.conversation_id` |
| `fixture_user_id` | Join to pack `users.json` / secrets Bearer (08/10) |
| `created_at` | ISO UTC; backdate path REQ11-04 (not a Narrative field) |
| `language` | Story language code (`et`/`ru`/`en`) |

Disk today (6-key pack): all four Present on every row of `ls-20260930T0938Z-veerenni-yard-construction/stories.json` (len **1661**; keys verified 2026-10-02).

---

## 3. Narrative-aligned content keys (AC-01)

Names mirror intake [`Narrative`](../src/core/intake/contracts.py); values stay **on-disk fixture**, not API invent.

| Fixture v2 flat key | Required? | Notes |
|---------------------|-----------|-------|
| `title` | yes (compat) | Thin path today; keep |
| `body` | yes (compat) | Thin path today; keep |
| `title_i18n` | v2 richness | map `et` / `ru` / `en` |
| `description_i18n` | v2 richness | map `et` / `ru` / `en` |
| `summary_i18n` | v2 richness | map `et` / `ru` / `en` |
| `session_language` | v2 | default = `language` if absent |
| `location_query` | v2 | optional string |
| `canonical_type` | v2 | e.g. civic type string |
| `canonical_labels` | v2 | list/tuple of label strings |
| `institution_i18n` | optional | → intake `institution` i18n map |

---

## 4. Mapping table fixture → Narrative / envelope (AC-03)

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

### Thin adapter today (6-key Partial — cite only)

[`life_sim_story_to_intake_payload`](../tests/sandbox/life_sim_replay_lib.py): `body`→`original_text`; `language`→`language`/`session_language`; synthesizes all-lang `title`/`description` from same strings; `canonical_type="complaint"`; `canonical_labels=[]`; `location_query` only if caller arg.

---

## 5. Explicit out of fixture v2 (AC-02)

**Do not** put in pack `stories.json` v2 AC:

| Out | Why |
|-----|-----|
| `story_id` | Runtime `StoryRecord` id — gateway-assigned |
| lifecycle / `lifecycle_status` | Domain persistence |
| `submitter_*` | Auth/session after provision — not fixture dump |
| `payload_hash` | Domain/runtime |
| Invent taxonomy **axis IDs** / invent `taxonomy` axis structure | No invent in v2 AC |
| Invent `gpt_signals` as fake classifier | Omit from v2 AC unless later story |

---

## 6. Scale locks + pack ≠ StoryRecord (AC-05)

Unchanged from REQ11-01:

| Lock | Value |
|------|-------|
| Users | **200** |
| Stories/user | Gaussian mean **8.5**, σ **2.0**, clamp **[1, 20]** |
| Langs | **60% et / 30% ru / 10% en** |
| Calendar | **2026**; breakpoint **2026-09-30**; mass ~**25%** pre / ~**75%** post |

Pack JSON is **not** a dump of [`StoryRecord`](../src/core/domain/contracts.py) (`story_id`, submitter, lifecycle, `payload_hash`, geo snapshots, SSR binding, etc.). Confirmed scarcity §3.3.

---

## 7. Compatibility (AC-04)

| Row class | Load / richness |
|-----------|-----------------|
| **6-key** (today) | **Partial** — thin adapter path keeps working; join keys intact for REQ11-10 replay |
| **v2** (flat + Narrative-aligned content) | **Pass** richness gates **once REQ11-12** implements generator+adapter |

This note does **not** implement generator or adapter.

---

## 8. What is not claimed

- No pack regeneration in REQ11-11
- No change to UX of REQ11-08 / 09 / 10 CLIs
- No reuse of removed REQ11-07 number
- No invent public HTTP field names beyond on-disk fixture contract
- Successor implement = **STORY-GW-REQ11-12**

## Consumer handoff

REQ11-12: emit v2 flat rows + teach adapter to prefer fixture i18n / `location_query` / `canonical_*` when Present; keep 6-key thin path for Partial.
