# STORY-GW-SSR-30 — Tallinn `card_fields` for SPA overlay readiness

## Meta
- **Key:** `STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — SPA overlay data readiness (sequence **30**)
- **Тип:** implement (pack data Declare) — **не** redesign projection
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Parent REQ:** 51 · spa-16 sibling
- **decision_ref:** backlog SSR-30 · Operator 2026-09-02 **Declare locked** (WAIVE N/A)
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000087-20260902-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness.yaml`](../../../../gateway-active-packages/pkg-000087-20260902-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-11 Done
- **Feeds:** SPA SSR-02 live Tallinn `schema_card`; GPT byte-copy `pack.json` (SSR-29)
- **Scaffolded:** 2026-09-02T13:56:06Z
- **G30 PASS:** 2026-09-02T14:00:46Z · [`run-summary`](../../../../run-reports/run-summary-20260902-1400-gw-ssr-30-p3.md)

## Nested tasks (pkg-000087)

| ID | Folder | Status |
|----|--------|--------|
| T00 | [`task-gw-ssr-30-t00-declare-decision-lock`](./task-gw-ssr-30-t00-declare-decision-lock/README.md) | Done |
| T01 | [`task-gw-ssr-30-t01-tallinn-card-fields-mvp`](./task-gw-ssr-30-t01-tallinn-card-fields-mvp/README.md) | Done |
| T02 | [`task-gw-ssr-30-t02-tests-card-fields-present`](./task-gw-ssr-30-t02-tests-card-fields-present/README.md) | Done |
| T03 | [`task-gw-ssr-30-t03-index-spa-docs-note`](./task-gw-ssr-30-t03-index-spa-docs-note/README.md) | Done |
| T04 | [`task-gw-ssr-30-t04-gpt-spa-handoff`](./task-gw-ssr-30-t04-gpt-spa-handoff/README.md) | Done |
| T05 | [`task-gw-ssr-30-t05-story-acceptance-gate`](./task-gw-ssr-30-t05-story-acceptance-gate/README.md) | Done · G30 |
| T06 | [`task-gw-ssr-30-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-30-t06-audit-g1-as-of-done-ssot/README.md) | Done · G1 CLOSED |

## Зачем простыми словами

Declare MVP `card_fields` on tallinn pack so SSR-11 can project named leaves into `schema_card` for SPA overlay. No SSR-11 redesign; no SPA FE in this pkg.

## MVP allowlist (tallinn only)

```json
"card_fields": [
  "signals.desired_outcome",
  "signals.affected_group",
  "signals.service_object"
]
```

## As-of-Done (P3 2026-09-02T14:00:46Z)

| Fact | Ref |
|------|-----|
| Declare locked; WAIVE N/A | Meta + INDEX row 30 |
| tallinn `pack.json` MVP `card_fields` | `schema-packs/tallinn_civic/v1/pack.json` |
| Tests present + smoke | `test_gw_ssr_11_card_fields_loader.py`; `test_gw_ssr_30_tallinn_card_fields.py` (9 passed with SSR-11 loader suite) |
| spa-16 Declare note | `spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md` |
| GPT / SPA L10N handoff | `schema-packs/README.md` SSR-30 paragraph |
| Residuals | no historical backfill; first-hit story order unchanged; legal/mobility still civic-only |

## Handoff (operator)

1. Byte-copy gateway `schema-packs/tallinn_civic/v1/pack.json` → GPT `instructions/schema-packs/tallinn_civic/v1/pack.json` (SSR-29 checklist; no GPT commit from this pkg).
2. SPA L10N ids: `schemaRuntime.cardField.signals.desired_outcome`, `schemaRuntime.cardField.signals.affected_group`, `schemaRuntime.cardField.signals.service_object`.

## Scope / Out of scope

**In:** Declare lock; tallinn `pack.json` MVP; tests flip absent→present; INDEX/spa note; GPT/SPA handoff; G30 gate.

**Out:** SPA overlay UI; SSR-11 / `field_policy` shape; invent paths; legal/mobility seed; ClusterLens change; §Актуальная точка rewrite; historical Issue backfill.

## Target / AC

- [x] **AC-GW-SSR30-01…06** — see backlog · G30 PASS
