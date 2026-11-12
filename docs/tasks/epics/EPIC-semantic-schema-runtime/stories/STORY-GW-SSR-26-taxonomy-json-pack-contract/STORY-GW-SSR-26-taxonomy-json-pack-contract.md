# STORY-GW-SSR-26 — taxonomy.json pack contract + loader

## Meta
- **Key:** `STORY-GW-SSR-26-taxonomy-json-pack-contract`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — taxonomy-pack wave (sequence **26**)
- **Тип:** implement (pack contract + loader)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../../../requirements/51-semantic-schema-runtime.md)
- **decision_ref:** backlog SSR-26
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract/STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000083-20260901-gw-ssr-26-taxonomy-json-pack-contract.yaml`](../../../../gateway-active-packages/pkg-000083-20260901-gw-ssr-26-taxonomy-json-pack-contract.yaml)
- **Git:** только `semantic-schema-runtime` — [INDEX §Git branch](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Зависит от:** SSR-25 ([pipeline](../STORY-GW-SSR-25-geo-detail-clustering-docs/STORY-GW-SSR-25-geo-detail-clustering-docs.md)); G25 PASS
- **Blocks:** SSR-28, SSR-29
- **Parallel:** SSR-27 (orthogonal — not this pkg)
- **Scaffolded:** 2026-09-01T12:55:39Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 | SCHEMA-005 loader / pack vocabulary contour |
| Decision | backlog SSR-26 | Contour2 pack taxonomy.json |

- **Разблокирует:** GPT-SSR-05 path exists; SSR-28 seed; SSR-29 docs
- **Не reopen:** SSR-01…25 product; T-wave G3 historical
- **Не трогаем:** ClusterLens; wire `narrative.taxonomy` / GW-TAX-01; tallinn seed; bullrun §«Актуальная точка»

## Nested tasks (pkg-000083)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-26-t00-contract-readme`](./task-gw-ssr-26-t00-contract-readme/README.md) |
| T01 | [`task-gw-ssr-26-t01-types-taxonomy-pack`](./task-gw-ssr-26-t01-types-taxonomy-pack/README.md) |
| T02 | [`task-gw-ssr-26-t02-loader-parse-taxonomy`](./task-gw-ssr-26-t02-loader-parse-taxonomy/README.md) |
| T03 | [`task-gw-ssr-26-t03-requiredness-tests-matrix`](./task-gw-ssr-26-t03-requiredness-tests-matrix/README.md) |
| T04 | [`task-gw-ssr-26-t04-tests-file`](./task-gw-ssr-26-t04-tests-file/README.md) |
| T05 | [`task-gw-ssr-26-t05-story-acceptance-gate`](./task-gw-ssr-26-t05-story-acceptance-gate/README.md) |
| T06 | [`task-gw-ssr-26-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-26-t06-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Ввести **`taxonomy.json`** в каталог pack + loader. Gateway pack dir = SSOT для GPT copy-paste. Wire `narrative.taxonomy` **не** меняется. Tallinn seed → SSR-28.

## Scope / Out of scope

**In:** README contract; `TaxonomyPack` types; `_parse_taxonomy_pack` + `load_pack` wire; requiredness tests via tmp_path; `tests/test_gw_ssr_26_taxonomy_loader.py`; gate.

**Out:** tallinn official seed (SSR-28); taxonomy docs/operator seam (SSR-29); replace `vocabulary.py`; wire taxonomy changes; ClusterLens extend; geo (SSR-27).

## Verified current state

### As-of-Done (SSR-26 pkg-000083 / G26 PASS 2026-09-01T13:00:37Z)

| Fact | Ref |
|------|-----|
| README `taxonomy_schema` + `taxonomy.json` | [`schema-packs/README.md:11,33,35–46`](../../../../../schema-packs/README.md) |
| `TaxonomyPack` + `SchemaContext.taxonomy` | [`contracts.py:89–122`](../../../../../src/core/schema/contracts.py) |
| `_parse_taxonomy_pack` + `load_pack` wire | [`resolver.py:250–412`](../../../../../src/core/schema/resolver.py), [`:515`](../../../../../src/core/schema/resolver.py) |
| Tests file (6) | [`test_gw_ssr_26_taxonomy_loader.py`](../../../../../tests/test_gw_ssr_26_taxonomy_loader.py) |
| Official packs: no `taxonomy_schema` → `taxonomy is None` | `schema-packs/*/v1/pack.json`; legal/mobility/tallinn |
| Orphan tallinn `taxonomy.json` not auto-loaded | file exists; manifest without key |
| `ClusterLens` = 10 | [`types.py:10–22`](../../../../../src/core/cluster/types.py) |

### Historical (pre-P3 / P1 scaffold)

| Fact | Ref (then) |
|------|------------|
| `SchemaContext` has no `taxonomy` | `contracts.py:89–100` |
| `load_pack` ends dual + card_fields | `resolver.py:344–345` |
| README no taxonomy keys | `schema-packs/README.md` |
| No `test_gw_ssr_26_*` | tests/ |

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T00** | README | layout + `taxonomy_schema` | frozen dialect / full manual |
| **T01** | Types | `TaxonomyPack` + `SchemaContext.taxonomy` | ClusterLens / axes change |
| **T02** | Loader | `_parse_taxonomy_pack` + wire | tallinn seed |
| **T03** | Tests matrix | requiredness / invalid / dup | official tallinn seed |
| **T04** | Tests file | `test_gw_ssr_26_taxonomy_loader.py` | SSR-28 tallinn load test |
| **T05** | Gate | AC-GW-SSR26-01…05 + invariants | start 27/28/29 |

## Target / AC

- [x] **AC-GW-SSR26-01:** README documents `taxonomy_schema` + `taxonomy.json`
- [x] **AC-GW-SSR26-02:** Loader exposes taxonomy on `SchemaContext` when declared
- [x] **AC-GW-SSR26-03:** legal/mobility load with `taxonomy is None`
- [x] **AC-GW-SSR26-04:** Invalid / duplicate → loader error (test-backed)
- [x] **AC-GW-SSR26-05:** ClusterLens + GW-TAX-01 wire unchanged
