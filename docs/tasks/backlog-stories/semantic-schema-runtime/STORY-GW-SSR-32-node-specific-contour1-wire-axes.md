# STORY-GW-SSR-32 — Node-specific Contour1 wire taxonomy axes

## Meta
- **Key:** `STORY-GW-SSR-32-node-specific-contour1-wire-axes`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** Done (Awaiting Commits) pkg-000089
- **Приоритет:** P1 — node-taxonomy wave (sequence **32**)
- **Тип:** implement (Contour1 normalize + intake tests)
- **Architecture SSOT:** [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md) (**D-SSR-11**)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md)
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** soft SSR-31 (e2e pack+wire); **code-parallel OK** with 31
- **Blocks:** soft SSR-33; uus GPT wire with custom axes
- **Parallel:** [GW-SSR-31](./STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **G32 PASS:** 2026-09-04T13:13:31Z

---

# Layer 1 — Постановка задачи

## Зачем простыми словами

Даже после открытия Contour2, intake отклонит историю, если GPT положит на `narrative.taxonomy` ось вроде `signal_type` — `normalize_axis` режет всё вне 13. Contour1 должен принимать **любую непустую** ось; civic по-прежнему использует только известный map → `SignalDimension` (остальное skip).

## Scope

- Open `normalize_axis` (strip/lower; no frozen membership).
- Tests: custom axis on wire parses; empty axis still fails; civic skip-unmapped regression.
- Call-site sanity (intake / story_labels only consumers of normalize for wire).

## Out of scope

- Contour2 loader (SSR-31).
- Docs wave (SSR-33).
- Extending `_AXIS_TO_SIGNAL_DIMENSION` / ClusterLens / vocabulary.py.
- Changing disposition enum.

## Short AC (Layer 1)

- [x] **AC-GW-SSR32-01:** Wire taxonomy with custom axis id accepted.
- [x] **AC-GW-SSR32-02:** Empty / non-string axis still rejected.
- [x] **AC-GW-SSR32-03:** Unmapped axis does not invent civic SignalDimension (skip path intact).

---

# Layer 2 — Реализация (техническая проработка)

## Verified as-built (pre-P3) → As-of-Done (post-P3 / G32)

| Fact | Evidence |
|------|----------|
| Contour1 normalize | **As-of-Done:** strip/lower only — [`axes.py`](../../../../src/core/taxonomy/axes.py) L24–31; no membership. **Historical (pre-P3):** L23–29 `Unsupported taxonomy axis` vs `TAXONOMY_AXIS_VALUES`. |
| Wire entry | [`parse_taxonomy_payload`](../../../../src/core/taxonomy/story_labels.py) L199–223 calls `normalize_axis` — **unchanged** |
| Intake | [`intake/contracts.py`](../../../../src/core/intake/contracts.py) uses `parse_taxonomy_payload` — **unchanged** |
| Civic skip | `story_labels.py` ~L185–188: `.get(axis)` → `continue` if None — **unchanged** |
| Export | [`taxonomy/__init__.py`](../../../../src/core/taxonomy/__init__.py) re-exports `TAXONOMY_AXIS_VALUES`, `normalize_axis` |
| Tests | **As-of-Done:** `test_gw_ssr_32_*` + tax_01 custom accept. **Historical:** tax_01 rejected unknown axis. |

## Target behaviour

```text
normalize_axis(raw):
  - must be non-empty str → strip → lower
  - return normalized
  - DO NOT check TAXONOMY_AXIS_VALUES

TAXONOMY_AXIS_VALUES:
  - remain in module as reference frozenset (tallinn / docs / SSR-28 content helpers)
  - optional: rename comment to "tallinn/civic reference axes (D-SSR-11); not wire reject SSOT"
```

## Touch list (P3)

| Path | Change |
|------|--------|
| [`src/core/taxonomy/axes.py`](../../../../src/core/taxonomy/axes.py) | Remove L27–28 membership check; update module comment |
| [`tests/`](../../../../tests/) | Add `test_gw_ssr_32_contour1_wire_axes.py` (or extend existing taxonomy intake tests): custom axis OK; `""` / `None` / int fail |
| Civic regression | Assert enrichment with only custom axes does not crash; mapped axes still fill dimensions (reuse existing fixture pattern if present) |

## Setup

- No env changes.
- Envelope fixtures: minimal `narrative.taxonomy` object with `{ "signal_type": [{"label": "problem", "disposition": "canonical"}] }` plus optional classic `topic_domain` for dual path.

## Concrete AC (P3 gate)

- [x] **AC-GW-SSR32-01:** `parse_taxonomy_payload` / intake path accepts axis not in `TAXONOMY_AXIS_VALUES`; labels persist with that axis string.
- [x] **AC-GW-SSR32-02:** Non-string / blank axis → ValueError / intake validation error (same class as today for empty).
- [x] **AC-GW-SSR32-03:** Story with only unmapped axes: civic signal fill does not raise; unmapped axes absent from civic dimension map (skip).
- [x] **AC-GW-SSR32-04:** Classic 13-axis wire samples still pass (no regression on tallinn-shaped taxonomy wire).

## DoD

- Pytest green; no ClusterLens change; arch-doc cited.

## Claims (Layer 2)

**As-of-Done:** Contour1 unlock + tests landed; G32 PASS 2026-09-04T13:13:31Z (pkg-000089); G1 CLOSED P6 2026-09-04T13:17:57Z.  
**Historical:** As-built membership reject verified pre-P3; implementation not started (pre-P3 claim).
