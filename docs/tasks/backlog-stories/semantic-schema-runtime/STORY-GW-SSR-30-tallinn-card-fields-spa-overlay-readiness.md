# STORY-GW-SSR-30 — Tallinn `card_fields` for SPA overlay readiness

## Meta
- **Key:** `STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — pkg-000087 G30 PASS 2026-09-02T14:00:46Z
- **Приоритет:** 🟠 MED — data readiness for sibling spa overlay (spa-16 / SPA SSR-02)
- **Тип:** implement (pack data Declare) — **не** redesign projection
- **Parent REQ:** [51](../../../requirements/51-semantic-schema-runtime.md) SPA-003/004 · sibling [spa-16](../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md)
- **Gap ref:** [G-CARD-01](../../../../../docs/analysis/cross-project-node-model-portability-gap-2026-09-01.md)
- **Зависит от:** [SSR-11](./STORY-GW-SSR-11-pack-declared-issue-projection.md) Done (projection mechanism)
- **Sibling FE:** [STORY-SPA-SSR-api-requirements.md](../../../../spa-app/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-SPA-SSR-api-requirements.md) · [STORY-SPA-SSR-02](../../../../spa-app/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-SPA-SSR-02-schema-card-overlay.md)
- **Operator decision (2026-09-02):** **Declare** (не WAIVE). Механизм SSR-11 **не переделываем**. Не добавляем флаги show_on_card в `field_policy`.

## Зачем простыми словами

Gateway уже умеет класть named leaves в `issue.schema_card` на `GET /node/issues`, **если** pack объявил `card_fields`. У `tallinn_civic/v1` ключа нет → на Tallinn node public Issues остаются civic-only. SPA overlay (SSR-02) тогда нечему показывать, даже когда FE готов.

Нужно не новый механизм и не hardcode в SPA: **дописать allowlist в tallinn pack.json**. SPA остаётся абстрактным: рисует то, что пришло в `schema_card`.

---

## Архитектура (не переделываем)

```mermaid
flowchart LR
  Pack["tallinn pack.json card_fields"]
  Proj["project_card_fields SSR-11"]
  API["GET /node/issues schema_card"]
  SPA["SPA overlay SSR-02 later"]
  Pack --> Proj --> API --> SPA
```

| Слой | Роль | As-built |
|------|------|----------|
| Pack SSOT | `card_fields[]` — какие dotted paths **разрешены** на публичную карточку | Loader [`_parse_card_fields`](../../../../src/core/schema/resolver.py); README row |
| Gateway extract | `project_card_fields(payload, allowlist, field_policy)` | [`card_fields.py`](../../../../src/core/projection/card_fields.py) — skip `forbidden`/`node_private`; only present leaves |
| Public Issue | Optional sidecar `schema_card[<dotted-path>]` | [`dto.py`](../../../../src/core/projection/dto.py) `to_public_dict`; wire [`issue_create.py`](../../../../src/core/application/issue_create.py) `_schema_card_for_stories` |
| SPA | Display-only; keys verbatim; labels `schemaRuntime.cardField.<path>` | SPA SSR-02 / PRODUCT-BRIEF — **не** читает pack.json |

**Civic base** (id, status, title, type, labels, …) остаётся базой карточки. Overlay — secondary «Additional details» (mockup M141).

**Не делаем:** свойства show_on_card внутри `field_policy`; dump `structured_payload`; `GET /schema-active`; pack.json в браузере.

---

## Verified current state (2026-09-02)

| Fact | Evidence |
|------|----------|
| Mechanism Done | SSR-11 pkg-000070; `project_card_fields`; tests `test_gw_ssr_11_*` |
| tallinn `pack.json` | **As-of-Done (SSR-30):** MVP `card_fields` = `signals.desired_outcome` / `affected_group` / `service_object` — [`pack.json`](../../../../schema-packs/tallinn_civic/v1/pack.json). **Historical (pre-P3):** key absent (G-CARD-01 gateway half). |
| Payload / field_policy | `signals.*` и `geo.*` уже есть — **новые payload-поля не нужны** |
| Absent allowlist = civic form | README; legal/mobility still absent. **As-of-Done tallinn:** `test_tallinn_civic_mvp_card_fields_present` + `test_gw_ssr_30_*`. **Historical:** `test_tallinn_civic_absent_card_fields_is_civic_form` |
| SPA `schema_card` in `src/` | 0 matches — SPA SSR-02 |
| M141 example paths | `signals.desired_outcome`, `signals.affected_group`, `signals.service_object` |

---

## Scope / Out of scope

**In:**

- Record **Declare** in this story + INDEX.
- Materialize MVP `card_fields` in [`schema-packs/tallinn_civic/v1/pack.json`](../../../../schema-packs/tallinn_civic/v1/pack.json).
- Tests / loader smoke that tallinn exposes non-empty `card_fields`.
- Docs: INDEX; brief cross-link spa api-req / G-CARD-01.
- Handoff notes: GPT byte-copy `pack.json` (SSR-29); SPA L10N keys for listed paths.

**Out:**

- SPA overlay UI / typedef / map (SPA SSR-01…03).
- Change SSR-11 projection algorithm / `field_policy` shape.
- Invent dotted paths outside tallinn payload schema.
- Reproject all historical Issues (residual).
- Fix first-hit story selection in `_schema_card_for_stories` (residual).
- WAIVE path (cancelled by operator decision).

---

## Tallinn pack declare (MVP allowlist)

**Добавить** в `tallinn_civic/v1/pack.json`:

```json
"card_fields": [
  "signals.desired_outcome",
  "signals.affected_group",
  "signals.service_object"
]
```

| Path | Почему в MVP |
|------|----------------|
| `signals.desired_outcome` | M141; optional in field_policy; в payload schema |
| `signals.affected_group` | M141 |
| `signals.service_object` | M141 |

**Явно exclude (документировать, не класть в allowlist):**

| Path / group | Почему |
|--------------|--------|
| все `geo.*` | Публичный geo уже через `Issue.geo`; street/house — SEC-004 |
| `signals.canonical_type` | Дубль civic `type` |
| `signals.civic_domain`, `signals.failure_pattern` | Сильный overlap с labels / clustering narrative → шум на card |
| любой `forbidden` / `node_private` | SSR-11 и так отфильтрует; не list |

**Residual expand (не MVP):** `signals.need`, `signals.ecosystem_signal`, `signals.civic_weight` — later pack revision, тот же механизм.

Новых ключей в `payload.schema.json` / новых строк `field_policy` для MVP **не требуется**.

---

## Подзадачи (будущий P3)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T00** | Decision | Meta/INDEX: Declare locked; WAIVE N/A | Re-open WAIVE without operator |
| **T01** | Pack | Add MVP `card_fields` to tallinn `pack.json` | Change legal/mobility; invent paths |
| **T02** | Tests | Update `test_tallinn_civic_absent_card_fields_is_civic_form` → expect present list; optional `test_gw_ssr_30_*` load + project_card_fields smoke | Change `project_card_fields` logic |
| **T03** | Docs | INDEX row 30; spa api-req note: Tallinn Declare (not civic-only forever) | SPA overlay implementation |
| **T04** | Handoff | Operator copy updated `pack.json` → GPT `instructions/schema-packs/tallinn_civic/v1/` (SSR-29); list L10N ids for SPA | Commit GPT without operator review |
| **T05** | Gate | `resolve_pack(tallinn)` → `card_fields` == MVP tuple; ClusterLens=10; no HTTP invent | Backfill all Issues |

---

## Target / AC

- [x] **AC-GW-SSR30-01:** Operator decision **Declare** recorded here and in INDEX (WAIVE N/A).
- [x] **AC-GW-SSR30-02:** `tallinn_civic/v1/pack.json` contains MVP `card_fields` above; every path exists in pack payload / `field_policy` and is not `forbidden` / `node_private`.
- [x] **AC-GW-SSR30-03:** Loader exposes non-empty `SchemaContext.card_fields` for tallinn; Issues **MAY** include non-empty `schema_card` when leaves resolve (SSR-11 unchanged).
- [x] **AC-GW-SSR30-04:** N/A (WAIVE cancelled).
- [x] **AC-GW-SSR30-05:** No new public HTTP; no `structured_payload` on public Issue; no `field_policy` shape change.
- [x] **AC-GW-SSR30-06:** Residuals documented: backfill, first-hit story order, SPA L10N, allowlist expand.

---

## Pitfalls / residuals

| Topic | As-built | SSR-30 stance |
|-------|----------|---------------|
| `_schema_card_for_stories` | First story in `story_ids` with non-empty card wins | Document only; no fix |
| Existing Issue rows | Pack change does not rewrite stored projections | Residual: reproject script or «new Issues only» |
| SPA L10N | Need `schemaRuntime.cardField.signals.*` for each path | Sibling ADMIN-SSR-05 / SPA SSR-02 |
| GPT SSOT copy | Updated `pack.json` should be byte-copied | SSR-29 checklist |
| Test `absent_card_fields` | **Historical:** asserted tallinn has no key · **As-of-Done:** flipped to `test_tallinn_civic_mvp_card_fields_present` (+ `test_gw_ssr_30_*`) | Done at P3; G1 SSOT sync P6 |

---

## Dependencies

- SSR-11 Done.
- Unblocks live Tallinn data path for SPA SSR-02 (FE still separate).
- Does not block SPA AC-SPA-CARD-01 for packs without `card_fields` (legal/mobility remain civic-only until their owners declare).

## Границы

- Не активировать P3 без этой deep-spec.
- Не подменять SPA FE stories.
- Не invent bbox / schema-metadata routes.
- Не переписывать `field_policy` под show_on_card.
