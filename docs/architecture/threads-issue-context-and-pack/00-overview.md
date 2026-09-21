# Gateway Issue ThreadContext materials + pack shell — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Active pack materialize (verification policy + shell knobs); service-auth pack settings pull; civic gate on method-opaque verified boolean; Issue materials for threads composition |
| **Parent REQ** | [`../../requirements/52-issue-thread-context-and-node-verification.md`](../../requirements/52-issue-thread-context-and-node-verification.md) |
| **Parent product** | `docs/requirements backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md` (§5.3–5.4, T-REQ7-02/04/08, D4, D19, D28–D32) |
| **Interview** | [`../../analysis/zeya888.req-target-tech-arch-interview-52-issue-thread-context-and-node-verification-2026-09-21.md`](../../analysis/zeya888.req-target-tech-arch-interview-52-issue-thread-context-and-node-verification-2026-09-21.md) |
| **Recorded** | 2026-09-21T19:10:35Z |
| **Mode** | Target technical architecture of the REQ focus — **not** implementation tasks / STORY / pkg |
| **Slug** | `threads-issue-context-and-pack` |

**Levels:** functional = REQ `52` · this folder = how the focus is realized in `doge-complaints-gateway` · work items = backlog / P1.3 elsewhere.

---

## 1) Context & functional vs tech split

Gateway stays the **civic runtime** and the **home of the active node pack**. It does **not** become the threads discussion service.

For shell (REQ7 Part A / REQ `52`):

1. **Materialize** into the active pack: verification policy (validation type + integration name) and shell knobs (depth, reaction enables/max, Topic-guarded defaults, media-type allowlist).
2. Expose those pack-derived settings to threads via a **service-auth** pull (path unnamed).
3. Keep existing civic Issue read for projection; threads **composes** logical ThreadContext itself (operator override vs “gateway returns one ThreadContext object”).
4. Civic verification consumers use identity’s method-opaque boolean wire `identity_verified` only — **no** `phone_verified` allow path; **no** backward-compatible dual-read on first launch.
5. Sanction enforce / voice-source API → **REQ8** (out of this package).

| Layer | Lives in | Content |
|-------|----------|---------|
| Functional / product | REQ `52` | Why, scope/OOS, DoD in product terms |
| Target tech (this package) | `docs/architecture/threads-issue-context-and-pack/` | Components, flows, ownership, migration, verify |
| Work items | backlog STORY (other prompts) | Not here |

**Sibling prior arch:**

- Identity: [`../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md) — wire `identity_verified`; profile persist + one-shot backfill on identity.
- Threads: [`../../../doge-threads/docs/architecture/threads-entity-shell/00-overview.md`](../../../doge-threads/docs/architecture/threads-entity-shell/00-overview.md) — see **cross-project seam** below (composition vs single pull).

---

## 2) Operator locks (Gateway O interview 2026-09-21)

| # | Topic | Decision | Rec. vs op |
|---|--------|----------|------------|
| DP1 | Who composes Issue ThreadContext (§5.3) | **B** — threads maps from civic Issue get + pack settings; gateway does **not** ship a unified ThreadContext object | Agent preferred C → **overridden** |
| DP2 | How pack knobs / verification policy reach threads | **A** — dedicated **service-auth** “active pack shell settings” pull from gateway | **accepted** |
| DP3 | Civic gate consumer | **A** — allow only on method-opaque verified boolean; **no** dual-read / no phone fallback on first launch | **accepted** (after pre-prod “no tails” position) |
| Migration | Data + contracts to new format | **Mandatory** even if few rows/users/packs; **no** backward compatibility requirement for gateway gate or pack shell contract | Operator mandate |

---

## 3) Target components (logical)

| Component | Responsibility | Must not |
|-----------|----------------|----------|
| Active pack warehouse | Hold nested `<id>/<ver>/` including verification policy + shell knobs capabilities | Invent concrete JSON key **strings** in this arch (names remain Open in REQ) |
| Pack settings read (service-auth) | Return pack-derived verification policy + shell knobs for the **active** `NODE_SCHEMA_*` pair | Serve Story bodies; become threads CRUD |
| Civic Issue projection read | Existing list/get Issue as civic projection | Be required to embed ThreadContext or knobs (not locked into public get) |
| Civic verification gate | Read `identity_verified` from Identity `/me` parse path; fail-closed | Use `phone_verified` for allow; decide phone vs eID |
| Pack → identity intake | Still **Open** (how type+integration name reach identity) | Invent a new public gateway route for this |

Siblings:

- [`01-threadcontext-materials-and-settings-pull.md`](./01-threadcontext-materials-and-settings-pull.md)
- [`02-pack-verification-and-shell-knobs.md`](./02-pack-verification-and-shell-knobs.md)
- [`03-civic-verified-boolean-consumer-and-migration.md`](./03-civic-verified-boolean-consumer-and-migration.md)

---

## 4) Primary flows (logical)

```text
Threads (service credentials)
  → GET civic Issue projection (existing public Issue get class)
  → GET active pack shell settings (service-auth; path unnamed)
  → compose logical ThreadContext (§5.3) locally
  → enforce knobs in threads (not gateway)

Civic write on gateway (e.g. draft submit)
  → Identity GET /me
  → allow iff identity_verified === true
  → never allow on phone_verified alone
```

No Story narrative in any threads-facing material (D19).

---

## 5) Ownership

| Artifact class | Owner |
|----------------|--------|
| Active pack files (policy + knobs materialize) | **Gateway** |
| Civic Issue projection | **Gateway** |
| Logical ThreadContext object composition | **Threads** (this wave, operator DP1=B) |
| Verified boolean persist + `/me` expose | **Identity** (`identity_verified`) |
| Feed UX | Spa — not this package |
| Sanction / voice-source | REQ8 |

---

## 6) Runtime / packaging / env

- **Runtime:** existing gateway ASGI (`src/core/api/asgi_app.py`).
- **Packaging seam:** Git-owned / Volume warehouse packs (`SCHEMA_PACKS_ROOT`, SSR-34). Materialize knobs = files on that warehouse for the active pair; production verify = resolve active pack **and** settings surface against that pair — not “unit test only in src”.
- **Env:** `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` required; `SCHEMA_PACKS_ROOT` as today for Volume.
- **Fail-closed:** active pack missing mandatory shell capabilities (REQ AC-05) → do not invent silent product defaults; boot/settings fail closed (exact HTTP/boot code Open to implement wave).

---

## 7) Cross-project seam (threads arch tension)

Threads package (`threads-entity-shell`) records knobs arriving **inside** a single ThreadContext pull from gateway.

**This gateway package** records operator locks: threads **composes** ThreadContext; knobs arrive via a **separate** service-auth settings pull; Issue get stays civic projection.

Both remain documented. Aligning threads docs / clients to the two-pull model (or revisiting DP1) is a **consistency follow-up** — not silently rewritten here, not a STORY list.

---

## 8) Open questions

1. Exact service-auth path string and JSON key names for settings (Open by REQ).
2. Which Issue projection fields are **sufficient** for threads §5.3 mapping (contract without inventing keys beyond REQ capabilities).
3. How pack validation type + integration name **reach** identity (also Open on identity TECH-ARCH §7).
4. Whether `issue_story_links` cover every Issue for opaque `value_source_refs` (REQ `52` §6).

---

## 9) Not in this doc

- STORY keys, epic waves, task README, pkg YAML, P3 code.
- Invented public ThreadContext route or concrete pack JSON key strings.
- REQ8 sanction enforce / voice-source API design.
- Pack Builder UX.
