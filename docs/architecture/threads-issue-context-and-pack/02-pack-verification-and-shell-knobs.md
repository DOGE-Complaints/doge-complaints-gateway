# Pack verification policy + shell knobs materialize

| Field | Value |
|-------|--------|
| **Parent** | [`00-overview.md`](./00-overview.md) |
| **REQ** | [`../../requirements/52-issue-thread-context-and-node-verification.md`](../../requirements/52-issue-thread-context-and-node-verification.md) AC-GW-THR-03/05 |
| **Recorded** | 2026-09-21T19:10:35Z |

---

## 1) As-is (verified)

| Fact | Path |
|------|------|
| Active pack = env pair | Runtime manuals / `NODE_SCHEMA_*` |
| Pack root | `SCHEMA_PACKS_ROOT` or in-tree `schema-packs/` |
| Verification / `threads.*` blocks in tracked packs | **Not found** (grep empty under `schema-packs/`) |
| Uus Veerenni target type | phone (REQ `52` §2) — integration name still to materialize |

---

## 2) Target

Active pack for the node **must carry** (this wave), as capabilities — **exact JSON key names remain Open** (do not invent strings here):

1. **Verification policy:** validation type (`phone` or `eID`) + integration name (D4, D28). Landing is not this home.
2. **Shell knobs:** max depth; per-reaction enables; `max_reactions_per_actor`; Topic-guarded defaults (parent §8.2); media-type allowlist within §9.

Pack Builder UX is optional polish — **not** a gate on live materialize (REQ `52` §2).

Uus Veerenni example: type = phone + named phone integration; outward user flag remains identity’s opaque boolean.

---

## 3) Fail-closed

If the active pack omits mandatory shell capabilities:

- Do **not** invent product defaults that pretend policy exists.
- Boot resolve and/or settings pull **fail closed** (exact error surface Open to implement wave).
- Soft-boot / empty Volume behaviors that already exist for missing packs stay orthogonal; once a pack is present, shell capabilities are required for this REQ focus.

---

## 4) Packaging seam (mandatory note)

| Concern | Decision |
|---------|----------|
| Ownership | Pack files Git and/or Railway Volume under `SCHEMA_PACKS_ROOT` (SSR-34 warehouse model) |
| Git ownership ≠ image readability | Node packs may be Volume-only; demo packs may be in-tree — production entry must see the **active** pair |
| Verify | Resolve active pack + settings capabilities on the runtime that serves production, not only local unit fixtures |
| Deploy residual | After pack file change on Volume: upload/overwrite + restart as operator runbook (existing Volume ops manuals) |

---

## 5) Migration (pack data — mandatory, no backward compat)

Even if few node packs / versions exist:

1. **Inventory** every pack that can be selected as `NODE_SCHEMA_*` in any env you care about (local + Volume).
2. **Rewrite / add** verification policy + shell knobs capabilities into those pack documents (and any mirrored GPT instruction copies the operator maintains — lockstep note only; GPT files not edited by this arch package).
3. **Do not** support a “knobs optional legacy pack” mode on first launch.
4. Packs that cannot be migrated are **not** eligible as active until completed.

This is **data/content migration** of pack files, parallel to identity’s user-profile migration — different stores, same rule: new format only.

---

## 6) Identity intake (Open)

How validation type + integration name are delivered into identity remains **Open** (REQ `52` §6; identity TECH-ARCH §7). This package owns pack home and settings expose to threads; it does not invent identity’s config API.

---

## 7) Out of scope

- Comment rate limits / near-dup automation (D32 / AC-GW-THR-06).
- Sanction enforce / voice-source (REQ8 / AC-GW-THR-04).
- Invented key string tables.
