# STORY-GW-SSR-29 — Taxonomy docs + operator copy-paste seam (GPT lockstep)

## Meta
- **Key:** `STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** Done (Awaiting Commits)
- **Приоритет:** P2 — taxonomy-pack wave capstone (sequence **29**)
- **Тип:** documentation + operator seam
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md)
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** [GW-SSR-26](./STORY-GW-SSR-26-taxonomy-json-pack-contract.md), [GW-SSR-28](./STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md) Done
- **Coordination:** [GW-SSR-27](./STORY-GW-SSR-27-geo-precision-instance-territory.md) T06 touches same manual — **one merge pass** if same package
- **Siblings (GPT):** [GPT-SSR-05](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-05-taxonomy-json-pack-copy-paste.md) · [GPT-SSR-06](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-06-inbound-validation-post-ssr-delta.md) · [GPT-SSR-09](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-09-use-case-audit-core-consume-json.md)
- **Analysis:** [`cross-project-node-model-portability-gap-2026-09-01.md`](../../../../../docs/analysis/cross-project-node-model-portability-gap-2026-09-01.md) G-TAX-01

## Зачем простыми словами

Loader (SSR-26) и seed (SSR-28) — техническая половина. Оператор и GPT backlog должны видеть **один процесс**: gateway `schema-packs/` = **SSOT**; GPT Instructions получают **byte-identical копию трёх JSON**. Без runbook wave 2 остаётся на бумаге; GPT-SSR-05 blocked on operator path.

Эта stori — **docs + cross-links + checklist**. Не переписывает GPT operator manual целиком (→ GPT-SSR-09 T05). **Не** implement code.

---

## Dual contour (must be explicit in manual)

| Concern | SSOT | Consumer |
|---------|------|----------|
| Per-axis labels on wire | OpenAPI `narrative.taxonomy` | Gateway intake → `story_labels` (GW-TAX-01) |
| Allowed keys + axis→signal | **`taxonomy.json` in pack dir** | GPT normalizer + operator copy |
| Payload validate | `payload.schema.json` | `SchemaRuntime.validate` |
| Content admission | GPT `inbound-validation.md` | GPT interview only |

**Critical:** docs must **not** imply wire envelope or GW-TAX-01 behavior changes.

---

## Verified as-built (2026-09-01)

| Fact | Evidence |
|------|----------|
| Manual pack layout | [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) — 3 JSON + §Taxonomy dual contour + §Operator copy-paste (SSR-29) |
| schema-packs README | [`schema-packs/README.md`](../../../../schema-packs/README.md) — cross-link manual §taxonomy / copy-paste |
| GPT pack README | [`GPT UI/instructions/schema-packs/README.md`](../../../../GPT%20UI/instructions/schema-packs/README.md) — operator step 4 |
| GPT active pair | `tallinn_civic/v1` |
| Gap G-TAX-01 | cross-project gap analysis |
| INDEX taxonomy wave | 26/28/29 Done (Awaiting Commits) when package executes |

---

## Scope / Out of scope

**In:**

| Artifact | Content |
|----------|---------|
| [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) | §layout 3 JSON; §taxonomy dual contour; §operator copy checklist; deprecation note for `story-label-taxonomy.md` SSOT |
| [`schema-packs/README.md`](../../../../schema-packs/README.md) | Cross-link manual §taxonomy (avoid duplicate full shape — SSR-26 owns tables) |
| [`INDEX.md`](./INDEX.md) | Taxonomy wave 26→28→29; GPT sibling links; Progress line when package Done |
| This story | Operator checklist (canonical copy) |

**Manual merge with SSR-27 (if same package execute):**

- SSR-27 T06 adds §three-level geo
- SSR-29 adds §taxonomy + §copy-paste
- Single edit pass — no contradictory layout bullets

**Out:**

- GPT operator manual full rewrite (`schema-pack-custom-model-operator-manual-ru.md` → GPT-SSR-09)
- spa / identity docs
- Implementation code (SSR-26/28)
- Geo pack block prose beyond cross-link (SSR-27 T06 owns geo §)
- Performing GPT file copy in gateway repo P3 (checklist only; handoff is operator/GPT-SSR-05)

---

## Operator checklist (canonical — publish in manual + this story)

1. **Edit SSOT** in gateway `schema-packs/<schema_id>/<schema_version>/` (taxonomy keys, canonical_keys, axis_to_signal_map).
2. **Copy three JSON byte-identical** to `GPT UI/instructions/schema-packs/<schema_id>/<schema_version>/`:
   - `pack.json`
   - `payload.schema.json`
   - `taxonomy.json`
3. **Verify checksum** (recommended):
   ```bash
   shasum -a 256 schema-packs/tallinn_civic/v1/{pack,payload.schema,taxonomy}.json \
     "GPT UI/instructions/schema-packs/tallinn_civic/v1/"*.json
   ```
4. **Update GPT** [`schema-packs/README.md`](../../../../GPT%20UI/instructions/schema-packs/README.md) active pair if id/version changed.
5. **Update GPT** `inbound-validation.md` §2 pointer to taxonomy JSON path (GPT-SSR-06 delta).
6. **Upload Custom GPT Instructions** — **no** Actions re-import if OpenAPI wire unchanged.

**Deprecation policy (document, don't delete GPT file):**

When operator copies JSON, GPT [`story-label-taxonomy.md`](../../../../GPT%20UI/instructions/story-label-taxonomy.md) is **no longer SSOT** for canonical keys — gateway pack + copy is SSOT. Final GPT-side deprecation decision: GPT-SSR-09.

**Lockstep (T04 / P3):** published verbatim in manual §Operator copy-paste — [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md).

---

## Подзадачи (детализация)

### T01 — Manual (primary deliverable)

Edit [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md):

**§Pack layout (update existing «Три пака на диске» / «Как добавить модель»):**

```text
schema-packs/<id>/<ver>/
  pack.json
  payload.schema.json
  taxonomy.json     ← when taxonomy_schema set in manifest (tallinn_civic/v1 post SSR-28)
```

**§Taxonomy dual contour** — table from this story Meta section + mermaid optional.

**§Operator copy-paste** — 6-step checklist above.

**§Как добавить модель** — step 4: optional `taxonomy.json` when civic copy-paste needed.

**Gate:** grep manual for `taxonomy.json`, `dual contour`, `byte-identical`

**Не:** rewrite full manual; не duplicate SSR-26 README shape tables verbatim

---

### T02 — schema-packs README cross-link

After SSR-26 T00, add in README:

> See [manual §taxonomy](../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) for operator copy-paste.

**Gate:** link resolves; no second full shape table

---

### T03 — Gateway INDEX hygiene

Update [`INDEX.md`](./INDEX.md):

- Taxonomy-pack table: 26/28/29 status → Done **only when package executes**
- Progress line: taxonomy 0/3 → 3/3 when Done
- Cross-links: GPT-SSR-05, GPT-SSR-06, GPT-SSR-09, gap analysis

**Не:** mark Done in INDEX before builder package complete

---

### T04 — Checklist in story

This file §Operator checklist = canonical; manual must mirror steps 1–6.

---

### T05 — Cross-repo handoff indicator

Document expected GPT-side files after operator copy (paths for GPT-SSR-05 verification):

| Gateway SSOT | GPT mirror path |
|--------------|-----------------|
| `doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json` | `GPT UI/instructions/schema-packs/tallinn_civic/v1/pack.json` |
| same dir `payload.schema.json` | same |
| same dir `taxonomy.json` | same |

GPT-SSR-05/08/09 P3 unblocked **after** gateway files on disk + operator copy (or CI diff story later).

**Не:** commit GPT JSON from gateway bot without operator review (product policy)

---

## Target / AC

- [x] **AC-GW-SSR29-01:** Manual describes three-file layout and taxonomy dual contour.
- [x] **AC-GW-SSR29-02:** Operator copy-paste checklist in manual **and** this story (steps 1–6).
- [x] **AC-GW-SSR29-03:** Gateway INDEX links GPT-SSR-05 and GW-SSR-26/28/29 wave.
- [x] **AC-GW-SSR29-04:** Deprecation note for GPT `story-label-taxonomy.md` as SSOT when JSON copied.
- [x] **AC-GW-SSR29-05:** No claim that wire envelope or GW-TAX-01 behavior changes.
- [x] **AC-GW-SSR29-06:** Manual geo § (SSR-27) and taxonomy § coexist without contradiction (when both land).

---

## Cross-story integration

| Shared artifact | Owners | Merge rule |
|-----------------|--------|------------|
| `schema-packs-node-data-model-ru.md` | SSR-27 T06 + SSR-29 T01 | One manual PR pass |
| `schema-packs/README.md` | SSR-26 T00 + SSR-27 T00 + SSR-29 T02 | Cross-links only in 29 |
| `INDEX.md` | SSR-29 T03 | Progress when package Done |
| `pack.json` tallinn | SSR-28 taxonomy_schema + SSR-27 geo blocks | Parallel-safe keys |

---

## Verification gates (docs-only story)

- [x] Every AC has file path (manual section heading, INDEX row, this story checklist)
- [x] Manual grep: no phrase «wire taxonomy moved to payload»
- [x] Links to GPT stories resolve from gateway repo relative paths
- [x] `mobility/legal taxonomy` documented as «tallinn first» residual

---

## Dependencies

- GW-SSR-26 Done (contract text in README)
- GW-SSR-28 Done (`tallinn_civic/v1/taxonomy.json` exists for example paths)
- Feeds GPT-SSR-05 T04, GPT-SSR-09 operator policy

---

## Residual

- Automated `diff` gateway vs GPT JSON in CI — tooling story
- mobility/legal pack copy-paste when those GPT overlays exist
- GPT `data-model.md` §6 Residual include removal — GPT-SSR-09

---

## Pitfalls (from dry-run)

1. **INDEX marked Done** while code/docs reverted — INDEX status follows **builder package**, not draft PR.
2. **GPT README still 2-file** after gateway 3-file — operator step 4 mandatory.
3. **Duplicating SSR-26 loader tables** in manual — link instead; manual = operator prose.
