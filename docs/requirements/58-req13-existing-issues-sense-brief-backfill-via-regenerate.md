# 58. REQ13 — Backfill existing Issues via sense-brief regenerate

Parent: [docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) (L9 manual regenerate; AC-07; board authenticity for **already created** Issues)  
Parent-id: REQ13-issue-sense-brief-civic-poster  
Prior sibling (same pipe): [`57-req13-issue-sense-brief-poster-projection.md`](./57-req13-issue-sense-brief-poster-projection.md) — create/publish nudge + bind + single-issue regenerate Present  
Peer sibling: [doge-ai-bridge REQ-10](../../../doge-ai-bridge/docs/requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) (provider + mock mode for dry backfill without vendor spend)  
Status: Draft — **interview locks closed** 2026-10-16 · awaiting PA.2  
Дата: 2026-10-15 · Locks: 2026-10-16

---

## 1) Goal

Дать оператору **безопасный способ** прогнать sense brief + civic poster для **уже существующих** Issues (созданных до pipe или без `generation_status=ready`), опираясь на Present **`POST /v1/issue-sense-brief/regenerate`**, а не на silent rewrite alpha-текста.

Итог: на доске у выбранных Issues появляются новые `generation_version`, brief-sourced title/summary и `poster_url` (когда peer worker + bind успешны).

## 2) Scope / Out of scope

**In scope**

- Ops **CLI/script** (not HTTP batch API in v1) to **select** Issues and regenerate them (one or many).
- Parity with create path: regenerate must supply **corpus** `{ "stories": [ … ] }` from Issue Story membership when Stories Present (verified gap today — see §3).
- Observable outcomes: pending → ready|failed; nudge success/fail; no citizen regenerate.
- Batch: **dry-run required**, hard cap, **sequential**, stop-on-fail; default **skip** Issues already `ready` (force only explicit).
- First target environment: **local-five**; hosted later.
- Docs/runbook: aibridge mock provider (REQ-10) → live text spot-check → wider batch.

**Out of scope**

- Replacing REQ57 create/publish pipe.
- Running LLM/image inside gateway (L2 extract stays on aibridge — lock §6 Q3).
- HTTP `regenerate-batch` endpoint in v1 (CLI/script only).
- SPA UI for regenerate; citizen “refresh poster”.
- Auto-regen on every Story merge (REQ13 L9).
- Gateway pre-shaping L2 brief fields from Stories.

## 3) Verified current state

| Fact | Path / note |
|------|-------------|
| Single-issue regenerate Present | `POST /v1/issue-sense-brief/regenerate` · [`sense_brief_regenerate.py`](../../src/core/application/sense_brief_regenerate.py) · service token only (REQ57-04) |
| Effect | bump `generation_version` → `generation_status=pending` → thin nudge |
| Create path builds corpus | [`issue_create.py`](../../src/core/application/issue_create.py) `_apply_pending_and_nudge` → `build_corpus_from_stories` |
| Regenerate / sweep nudge **without** corpus | [`sense_brief_regenerate.py`](../../src/core/application/sense_brief_regenerate.py) `nudge(...)` no corpus arg; [`sense_brief_sweep.py`](../../src/core/application/sense_brief_sweep.py) `corpus=None` |
| Corpus builder Present | [`sense_brief_nudge.py`](../../src/core/application/sense_brief_nudge.py) `build_corpus_from_stories` → `{ "stories": [ … ] }` |
| Sweep eligibility | only `generation_status` in `pending`\|`failed` — Issues **never** nudged (no status) are **not** picked by sweep alone |
| Batch backfill API / CLI | **Absent** (not found as dedicated backfill endpoint/tool) |

**Implication:** regenerate without corpus → peer `corpus_insufficient` risk. This REQ closes corpus parity; peer live/mock extract of `{stories}` is sibling REQ-10.

## 4) Target behavior

1. Single regenerate (HTTP Present) **and** CLI/script batch attach corpus via `build_corpus_from_stories` (parity with create).
2. Batch selection: start with **explicit Issue ids** and/or **demo fixture set**; later optional “all PUBLISHED without `ready`” with hard cap.
3. Each regenerated Issue gets a **new** `generation_version`; batch **skips** `generation_status=ready` unless `--force` (or equivalent).
4. Batch is **sequential**, has max N, **stop-on-fail**, and **dry-run** lists targets without peer nudge.
5. First prove on **local-five** with aibridge **mock** providers; then one live-text spot-check; then wider batch.
6. Public wire after bind unchanged from REQ57 (`generation_status`, `generation_version`, `poster_url`, brief title/summary).

## 5) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **AC-58-01** | Regenerate for an Issue with Stories membership includes `{stories:[…]}` corpus on nudge (parity with create) |
| **AC-58-02** | Issues with no prior `generation_status` can enter pending via regenerate (not only sweep) |
| **AC-58-03** | Ops CLI/script can process more than one Issue (service-auth / local credentials as designed in PA.2) |
| **AC-58-04** | Batch: hard cap + sequential + stop-on-fail (documented + testable) |
| **AC-58-05** | Dry-run lists Issues that would be regenerated **without** calling peer |
| **AC-58-06** | Citizen Bearer cannot trigger backfill/regenerate |
| **AC-58-07** | Operator runbook: mock-first (REQ-10) → live text spot-check → batch; local-five first |
| **AC-58-08** | Batch skips `ready` by default; force regenerate is explicit opt-in |

## 6) Interview locks (closed 2026-10-16)

Operator accepted architect recommendations.

| ID | Lock |
|----|------|
| **L58-1** | Batch surface = **ops CLI/script** (not HTTP batch endpoint in v1) |
| **L58-2** | Selection = start **explicit ids** and/or **demo set**; later all PUBLISHED without `ready` with cap |
| **L58-3** | Corpus = gateway sends `{stories:[…]}`; **aibridge** extracts L2 (mock or live text provider) — no gateway L2 map |
| **L58-4** | Dry-run = **required** for batch v1 |
| **L58-5** | Concurrency = **sequential only** |
| **L58-6** | First environment = **local-five** |
| **L58-7** | Already `ready` = batch **skip** by default; force only explicit |

**Residual Open (PA.2 / ops naming only — not product forks):** exact CLI command name, env for service token, max-N default number.

## 7) Dependencies

- REQ57 pipe Present (bind, nudge env, regenerate single).
- Sibling aibridge REQ-10 (mock/live text+image; `{stories}` → L2 on worker).
- Peer worker accept/bind (REQ-09 / handoff 2026-10-15).
- Orthogonal: spa 23 (display only).
