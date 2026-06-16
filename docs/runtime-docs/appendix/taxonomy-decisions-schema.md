# Taxonomy decisions manifest schema

SSOT for `taxonomy-decisions.yaml` produced by taxonomy cycle scripts (TC2–TC3) and consumed by apply scripts (TC4–TC5).

Related: [`taxonomy-update-process-ru.md`](./taxonomy-update-process-ru.md), [`.cursor/plans/Taxonomy_builder.plan.md`](../../../../.cursor/plans/Taxonomy_builder.plan.md).

## Top-level fields

| Field | Required | Description |
|-------|----------|-------------|
| `cycle_id` | yes | `YYYYMMDD` identifier matching run folder |
| `thresholds.min_miss_count` | yes | Minimum miss count for non-ignore classification (default `3`) |
| `decisions` | yes | List of per-key decisions |

## Decision entry

| Field | Required | Description |
|-------|----------|-------------|
| `label_key` | yes | Canonical token from telemetry (lowercase snake_case) |
| `action` | yes | One of: `map`, `translate_only`, `ignore`, `pending`, `new_board_label` |
| `target_label` | for `map`, `new_board_label` | Governed SPA / `DOGEIssueLabel` value |
| `spa_label` | optional | Explicit SPA dictionary key (auto-set for `translate_only`) |
| `locales` | yes | Locales needing translation, e.g. `[et, ru, en]` |
| `auto` | yes | `true` if set by classifier; `false` after interview |
| `reason` | yes | Human-readable classification rationale |
| `new_board_label` | for new enum | Must be `true` to allow `DOGEIssueLabel` + `AVAILABLE_LABELS` extension |
| `translations` | optional | `{ et: "…", ru: "…", en: "…" }`; placeholder RU/ET ok with TODO copy |

## Actions and apply targets

| Action | Gateway (`taxonomy_apply_gateway.py`) | SPA (`taxonomy_apply_spa_i18n.py`) |
|--------|--------------------------------------|-------------------------------------|
| `ignore` | skip | skip |
| `pending` | skip (must resolve in TC3) | skip |
| `translate_only` | skip | patch `dictionaries.js` |
| `map` | add `_CANONICAL_TO_SPA_LABEL` line | skip (unless also needs translation) |
| `new_board_label` | add `DOGEIssueLabel` + mapping | `labelKeys.js` + `dictionaries.js` |

## Classification rules (TC2 auto-heuristic)

1. Invalid pattern `^[a-z][a-z0-9_]{1,48}$` → `ignore`
2. `miss_count < thresholds.min_miss_count` → `ignore`
3. Key in live `_CANONICAL_TO_SPA_LABEL` or `DOGEIssueLabel` values → `translate_only`
4. Else → `pending` (operator interview in TC3)

**Important:** Telemetry records **missing SPA translation**, not missing backend mapping. If mapping exists, action is `translate_only`, not `map`.

## Example

```yaml
cycle_id: "20260615"
thresholds:
  min_miss_count: 3
decisions:
  - label_key: sidewalk
    action: map
    target_label: infrastructure
    locales: [et, ru, en]
    auto: false
    reason: operator mapped new canonical token
  - label_key: roads
    action: translate_only
    spa_label: infrastructure
    locales: [et, ru]
    auto: true
    reason: canonical token already mapped in _CANONICAL_TO_SPA_LABEL
  - label_key: xy
    action: ignore
    locales: [en]
    auto: true
    reason: miss_count below threshold (3)
```

## Scripts

| Script | Phase |
|--------|-------|
| `scripts/taxonomy_fetch_misses.py` | TC1 |
| `scripts/taxonomy_classify_candidates.py` | TC2 |
| `scripts/taxonomy_apply_gateway.py` | TC4 |
| `scripts/taxonomy_apply_spa_i18n.py` | TC5 |
