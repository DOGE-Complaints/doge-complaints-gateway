# 52. Issue thread context and node verification policy (shell)

Parent: docs/requirements backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md §0, §5.3–5.4, §7–§9, T-REQ7-02, T-REQ7-04, T-REQ7-08, D4, D19, D28–D32, AC-REQ7-15  
Parent-id: doge-threads-entity-social-governance  
Siblings: doge-threads/docs/requirements/01-entity-thread-core.md (contract: threads **pulls** Issue ThreadContext; route and fields unnamed); doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md (contract: pack states validation type and integration name; identity returns the user’s **verified boolean** and writes the audit log; this gateway **consumes** that boolean for civic verify — not phone hard-code); spa-app/docs/requirements/17-issue-thread-feed-ux-and-reactions.md (contract: TBD-question — spa shows the dashboard feed and the verification flow; no new gateway route named here)  
Status: Draft — awaiting PA.2 (shell scope 2026-09-21; Part A locks applied)  
Related algorithms parent: docs/requirements backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md (sanction enforce / voice-source — not this child’s shell AC)  
Architecture (target tech): [docs/architecture/threads-issue-context-and-pack/00-overview.md](../architecture/threads-issue-context-and-pack/00-overview.md)  
Interview report: [docs/analysis/zeya888.req-target-tech-arch-interview-52-issue-thread-context-and-node-verification-2026-09-21.md](../analysis/zeya888.req-target-tech-arch-interview-52-issue-thread-context-and-node-verification-2026-09-21.md)  

Дата: 2026-09-21  
Проект: doge-complaints-gateway  
Фокус: shell — Issue ThreadContext на pull + **materialize** pack verification policy **и** shell knobs (depth, reaction enables/max, Topic-guarded defaults, media-type allowlist). Story-create sanction enforce и voice-source API → **REQ8**. **Без** нового HTTP path; exact JSON key names Open (do not invent)

---

## 1) Goal

Gateway остаётся civic-рантаймом и не становится сервисом тредов. Для shell он — провайдер Issue-контекста (pull) и дом активного node pack: политика «что значит verified» (тип + имя интеграции) **и** shell knobs из parent §7 / T-REQ7-04 / T-REQ7-08. Verified boolean — свойство пользователя в identity; gateway не владеет булеаном.

## 2) Scope / Out of scope

### In scope (shell)

- Issue adapter capabilities named in parent §5.3 (title, discussion taxonomy, binding mode, opaque story ids, safety/escalation pointers). No Story narrative (D19).
- Existing Issue read remains the civic projection. This Draft does not rename it.
- **Active pack must carry (this wave):**
  - verification policy: validation type (`phone` or `eID`) and integration name (D4, D28);
  - `threads.tree.max_depth`;
  - per-reaction enable flags and `max_reactions_per_actor` with Topic-guarded presentation defaults from parent §8.2 (T-REQ7-08);
  - media-type allowlist within parent §9 legal floors.
- Exact JSON key **names** remain Open — capabilities are mandatory; inventing key strings in this Draft is forbidden.
- Uus Veerenni: type = phone. Landing is not this home.
- Comment create must not change clustering (D1).
- **Consumer seam (AC-REQ7-04):** civic write / verification checks that ask “is this user verified?” must use identity’s method-opaque **verified boolean**, not a hard-coded phone-only gate (`verification_gate.py:19-25` is the current gap).

### Out of scope (this child / shell)

- Story-create sanction **enforce** — **REQ8** ([REQ8](../../../docs/requirements%20backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md) T-REQ8-05).
- Designing or exposing a **voice-source API** for weighting — **REQ8** (opaque `value_source_refs` may remain in ThreadContext for lineage/privacy without implying weighting).
- Thread CRUD, reaction storage, votes, spa screens.
- Running the phone/eID provider (identity).
- Inventing a public ThreadContext route or concrete pack JSON key strings.
- Pack Builder authoring UX (elicit may come later; **live pack materialize is not blocked** on Pack Builder).
- Blob store for comment photos; comment rate limits / near-dup automation (parent D32).

## 3) Verified current state

| Fact | Path |
|------|------|
| Issue list/get | `src/core/api/asgi_app.py:503-556` |
| Verification gate hard-codes phone | `src/core/identity/verification_gate.py:19-25` |
| Active pack is env pair | `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` |
| Story↔issue links exist | `src/core/infrastructure/db_supabase.py:39`, `save_issue_story_links` at `:1251` |
| Cluster lenses (10) | `src/core/cluster/types.py:10-22` |
| Embeddings `vector(8)` | `supabase/migrations/20260423_1500_init_db_wave.sql:32,51` |

Unknown: pack block that already names validation type + integration name. Unknown: pack blocks for `threads.tree.max_depth` / reaction enables. Unknown: a read that already returns §5.3 as one ThreadContext object (route unnamed).

## 4) Target behavior

1. Threads pulls parent §5.3 context for a civic Issue. Gateway does not push. No Story text. Route unnamed.
2. Active pack states verification policy (type + integration name). Consumers read verified boolean from identity.
3. Active pack also carries shell knobs listed in §2 In scope (depth, reaction enables/max with Topic-guarded defaults, media-type allowlist). Pack Builder is optional polish, not a gate.
4. Uus Veerenni: type = phone + named phone integration. Outward flag stays verified boolean.
5. Civic paths that gate on verification consume identity’s verified boolean (method opaque). Hard-coded phone-only check is the gap to close this wave (D4 / AC-REQ7-04).
6. Shell does **not** require intake to refuse Stories on a threads sanction signal (that is REQ8).
7. Opaque story ids for lineage may appear in context without implying cabinet metrics or voice curve.

## 5) Acceptance criteria

1. AC-GW-THR-01: Draft does not mandate a new public route or invent concrete pack JSON key strings.
2. AC-GW-THR-02: Issue context lists parent §5.3 capabilities, forbids Story bodies, served on pull (D29). Route unnamed.
3. AC-GW-THR-03: Verification policy home is the gateway schema pack (validation type + integration name). Identity owns execution and the verified boolean. Landing excluded (D28).
4. AC-GW-THR-04: This Draft does **not** claim story-create sanction enforce or a voice-weighting source API as shell duties (parent §0 / D31).
5. AC-GW-THR-05: Active pack **materializes** shell knobs this wave: max depth, per-reaction enable flags, `max_reactions_per_actor`, Topic-guarded defaults from parent §8.2, media-type allowlist within §9 (parent T-REQ7-04, T-REQ7-08, AC-REQ7-15). Exact key names Open.
6. AC-GW-THR-06: This child does **not** require comment rate limits or near-duplicate warnings in pack/runtime (parent D32).
7. AC-GW-THR-07: Civic verification consumers use identity’s method-opaque verified boolean; phone-only hard-code (`verification_gate.py:19-25`) is not the target contract (parent D4, AC-REQ7-04).

## 6) Open questions

- Whether `issue_story_links` rows cover every Issue or only promoted links (`db_supabase.py:1251`).
- Exact JSON key names for verification policy and `threads.*` shell knobs (capabilities locked; names Open).
- REQ8 signal shape for story-create sanction (out of shell).

## 7) Dependencies

- Parent §0 / D31 / D32 / T-REQ7-04 / T-REQ7-08.
- threads 01 consumes context and node settings.
- identity 21 executes the named integration.
- spa 17 shows feed + verification flow and reads enabled reaction ids.
- **REQ8** [`docs/requirements backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md`](../../../docs/requirements%20backlog/REQ8-DOGEstonia-Threads-Metrics-Voice-Governance.md) for sanction enforce and voice-source delivery.
