# STORY-GW-SSR-28 — tallinn_civic/v1 taxonomy.json seed

## Meta
- **Key:** `STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — taxonomy-pack wave (sequence **28**)
- **Тип:** implement (pack data materialization)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Parent REQ:** 51
- **decision_ref:** backlog SSR-28
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000085-20260901-gw-ssr-28-tallinn-civic-taxonomy-json-seed.yaml`](../../../../gateway-active-packages/pkg-000085-20260901-gw-ssr-28-tallinn-civic-taxonomy-json-seed.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-26 Done (loader)
- **Blocks:** SSR-29
- **Scaffolded:** 2026-09-01T13:31:30Z
- **G28 PASS:** 2026-09-01T13:35:45Z · [`run-summary`](../../../../run-reports/run-summary-20260901-1335-gw-ssr-28-p3.md)

## Nested tasks (pkg-000085)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-28-t01-extract-inventory`](./task-gw-ssr-28-t01-extract-inventory/README.md) | Done |
| T02 | [`task-gw-ssr-28-t02-compose-taxonomy-json`](./task-gw-ssr-28-t02-compose-taxonomy-json/README.md) | Done |
| T03 | [`task-gw-ssr-28-t03-pack-manifest`](./task-gw-ssr-28-t03-pack-manifest/README.md) | Done |
| T04 | [`task-gw-ssr-28-t04-tests`](./task-gw-ssr-28-t04-tests/README.md) | Done |
| T05 | [`task-gw-ssr-28-t05-handoff-indicator`](./task-gw-ssr-28-t05-handoff-indicator/README.md) | Done |
| T06 | [`task-gw-ssr-28-t06-story-acceptance-gate`](./task-gw-ssr-28-t06-story-acceptance-gate/README.md) | Done · G28 |

## Зачем простыми словами

Seed real `taxonomy.json` for tallinn from GPT SSOT so SSR-26 loader + GPT copy-paste path work. No invent vocabulary.

## Scope / Out of scope

**In:** extract inventory; compose taxonomy.json; tallinn manifest key; tests; handoff; gate.

**Out:** legal/mobility seeds; invent keys; GPT UI copy; silent renames; SSR-29 product; §Актуальная точка rewrite.

## As-of-Done (P3 2026-09-01T13:35:45Z)

| Fact | Ref |
|------|-----|
| Tallinn `taxonomy_schema` | `pack.json` → `taxonomy.json` |
| Seed | 13 axes / 182 keys from GPT §4/§5/§6 via `tests/helpers/ssr28_gpt_taxonomy_extract.py` |
| Loader | `resolve_pack(tallinn_civic/v1).taxonomy` non-None |
| Handoff | `schema-packs/README.md` — byte-copy ready for SSR-29 / GPT-SSR-05; **gateway P3 does not edit GPT UI** |
| legal/mobility | still no `taxonomy_schema` |

## Target / AC

- [x] **AC-GW-SSR28-01…06** — see backlog story Target / AC · G28 PASS
