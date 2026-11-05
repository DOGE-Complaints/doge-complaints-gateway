# Hard Audit — STORY-GW-REQ59-01 aibridge stash parity verify (2026-11-05)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ59-01-aibridge-stash-parity-verify`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md) (T01–T06, **pkg-000117**) · backlog [`…/STORY-GW-REQ59-01-…`](../tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md).  
**Pkg:** [`pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml`](../tasks/gateway-active-packages/pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ59-01.md`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/task-gw-req59-01-t06-story-gate/story-acceptance-gate-STORY-GW-REQ59-01.md) PASS **2026-11-05T12:10:10Z**.  
**Run-summary:** [`run-summary-20261105-1210-gw-req59-01-p3.md`](../tasks/run-reports/run-summary-20261105-1210-gw-req59-01-p3.md).  
**Evidence SSOT:** [`evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md`](./evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md).  
**Прогон этого аудита:** `utc_now: 2026-11-05T12:14:55Z`. Branch: **`dev`**. Live harness: draft_01 + draft_02 get/submit + openapi → **24 passed** (1.86s). `--verify` → **ok 6** (pkg-000117).

> **Природа аудита.** P4 hard audit verify-first vs AC. Реализацию не предлагаю — только findings.  
> **Default Pass = no GW product code** if parity holds — **honored** (no `src/` change claimed; re-verified Present paths only).  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1254 / L1260–1265. AC из Target verbatim — **не** invent.

---

## 1. Итог: AC PASS (harness); parity holds; no GW code; evidence Present; live Unknown; 4 soft gaps (docs + live residual)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | stash path inventory | `POST /story-drafts` + `_STORY_DRAFT_WRITE_DEPS` — [`asgi_app.py:375`](../../src/core/api/asgi_app.py) / [`:685`](../../src/core/api/asgi_app.py); `handle_story_draft_create` 201 + `draft_id` — [`handlers.py:790–829`](../../src/core/api/handlers.py); TTL `story_draft_ttl_seconds` L808 | ✅ PASS† |
| **T02** | aibridge client parity | Peer [`gateway.py`](../../../doge-ai-bridge/src/aibridge/gateway.py) `STASH_PATH="/story-drafts"` L13 · `parse_success_body` L123–143 · `map_http_outcome` 201→STASHED L154–158 · `authorization_header` Bearer L204–207 · `execute_stash` L209+ | ✅ PASS |
| **T03** | service vs citizen auth | POST write deps service; GET/submit citizen — [`asgi_app.py:378–434`](../../src/core/api/asgi_app.py) / [`:685`](../../src/core/api/asgi_app.py) / [`:701`](../../src/core/api/asgi_app.py) / [`:717`](../../src/core/api/asgi_app.py) / [`:734–736`](../../src/core/api/asgi_app.py); 401 tests Present | ✅ PASS |
| **T04** | stash ≠ published Story | `data={"draft_id"}` only on create; `test_post_story_drafts_returns_draft_id_without_creating_story`; peer `STASH_REPLY` L20–22 | ✅ PASS |
| **T05** | evidence or gap note | [`evidence-gw-req59-01-…`](./evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md) Present · empty OPEN gap · no GW code | ✅ PASS† |
| **T06** | gate AC-01…04 | Gate PASS 12:10:10Z | ✅ PASS |

† Task README Code Facts still scaffold phrasing (see **G4**).

**Verdict:** GW-REQ59-01 **исполнена по verify-first / gate framing** (POST stash SSOT · peer path+Bearer+draft_id · stash≠Story · auth boundaries · evidence · Default Pass no GW code).  
**Product Story Done (AC/DoD) = yes** (verify story; product = no code change required). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-GW-59-01 Documented verify: stash 201 + `draft_id` for aibridge client | **PASS**† | Peer `STASH_PATH` + `execute_stash` + `parse_success_body` · GW create 201 + `draft_id` · harness draft_01 / openapi · evidence §AC map |
| AC-GW-59-02 Stash success ≠ published Story | **PASS** | Create envelope only `draft_id`; story count unchanged in `test_post_story_drafts_returns_draft_id_without_creating_story`; Story via submit/`handle_story_intake` |
| AC-GW-59-03 If break: written gap + decision | **PASS** | No hard break · evidence gap list **Empty** · no silent invent |
| AC-GW-59-04 Service vs citizen boundaries unchanged | **PASS** | Write = service; GET/submit = citizen deps; missing/wrong service → 401 |
| Default Pass = no GW code if parity holds | **PASS** | P3/run-summary/evidence: **no** product `src/` change · this audit read-only re-verify |

† AC-01 live peer→hosted execute_stash = **Unknown** (soft G4) — residual **G1**; gate framed code+harness.

### Focus re-checks

| Focus | Result |
|-------|--------|
| Locked path `POST /story-drafts` | ✅ `asgi_app.py:685` |
| Service auth write | ✅ `_STORY_DRAFT_WRITE_DEPS` → `require_public_content_service_auth` |
| 201 + `draft_id` (+ `trace_id` envelope) | ✅ `handlers.py:825–829` |
| Peer path `/story-drafts` | ✅ `STASH_PATH` |
| Peer Bearer ≠ channel | ✅ `authorization_header` / `GATEWAY_SERVICE_API_TOKEN` required |
| Stash ≠ Story | ✅ create response + harness + peer `STASH_REPLY` |
| Citizen cannot POST stash | ✅ service-only dep + 401 tests |
| Evidence Present | ✅ `docs/analysis/evidence-gw-req59-01-…` |
| Live aibridge | ⚠ **Unknown** (not run) |
| Harness | ✅ **24 passed** this audit |
| Branch / pkg | ✅ `dev` · pkg-000117 · `--verify` ok 6 |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| POST stash route | `asgi_app.py:685–698` | ✅ |
| Write deps | `asgi_app.py:368–375` | ✅ |
| Create handler | `handlers.py:790–829` | ✅ |
| GET citizen | `asgi_app.py:701` / `:717` + `_STORY_DRAFT_READ_DEPS` | ✅ |
| Submit citizen + gate | `asgi_app.py:734–751` + `_STORY_DRAFT_SUBMIT_DEPS` | ✅ |
| Peer client | `doge-ai-bridge/src/aibridge/gateway.py` | ✅ |
| Offline harness | draft_01 / draft_02 get / draft_02 submit / openapi | ✅ 24 |
| No hard contract break | evidence empty gap · this audit | ✅ |

---

## 3. Регрессии / gaps

### G1 — Live aibridge `execute_stash` Unknown · severity: **LOW** · **WAIVED-likely reason=info-nonblocking** (soft)

Evidence + gate + run-summary: live peer stash against hosted gateway **not run** this P3 → **Unknown** (no invent PASS). Soft-depend G4 / story Meta. AC-01 PASS = code + harness. Not a hard contract break.

**Как закрыть:** WAIVE info-nonblocking (verify-first Default Pass + Unknown live explicit); **or** TASKED optional live smoke when G4 hosted available — not required to reopen AC.

### G2 — Bullrun §«Актуальная точка» без REQ59-01 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1254 + tasks L1260–1265 Done; epic banner + P3 note: §Актуальная точка **не** переписана.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — Pipeline §Verified still «scaffold / pre-P3» · severity: **LOW** · **TASKED-likely** (docs)

[`STORY-GW-REQ59-01-….md:49`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md): heading `Verified current state (scaffold / pre-P3 · …)` while Meta Status **Done**, gate PASS, nested T01–T06 Done. Soft SSOT heading drift; table facts still match Present code.

**Как закрыть:** TASKED docs — retitle As-of-Done P3 + cite evidence; **or** WAIVE if operator keeps probe heading intentional.

### G4 — Task README Code Facts still «Await P3» / T05 «Evidence Absent» · severity: **LOW** · **TASKED-likely** (docs)

T01–T04 Code Facts item 3 still **Await P3** ([`t01`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/task-gw-req59-01-t01-stash-path-inventory/README.md) / [`t02`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/task-gw-req59-01-t02-aibridge-client-contract-parity/README.md) / [`t03`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/task-gw-req59-01-t03-auth-boundary-service-vs-citizen/README.md) / [`t04`](../tasks/epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/task-gw-req59-01-t04-stash-neq-story-assert/README.md)). T05 Code Facts: «Evidence… **Absent**» while evidence file **Present**. Status/DoD checkboxes Done; Gap sections not marked Closed. Soft present-tense drift only.

**Как закрыть:** TASKED docs — align Code Facts/Gap with As-of-Done + evidence path; **or** WAIVE if acceptance + evidence treated as SSOT.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1254 GW-REQ59-01 | 🔵 Done · gate PASS · verify-first · no product · pkg-000117 | Story Done (verify) | PASS† |
| T01 | L1260 | Done · AC-01/02 · GW-DRAFT-01 | Done | PASS (+ G4 soft) |
| T02 | L1261 | Done · peer parity | Done | PASS (+ G4 soft) |
| T03 | L1262 | Done · AC-04 | Done | PASS (+ G4 soft) |
| T04 | L1263 | Done · AC-02 | Done | PASS (+ G4 soft) |
| T05 | L1264 | Done · evidence Present · empty gap · no GW code | Done | PASS (+ G4 soft) |
| T06 | L1265 | Done · AC-01…04 PASS | Gate PASS | PASS |
| P3 note | L1267 | gate PASS · live Unknown · no product | matches | PASS (+ G1) |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

† Pipeline §Verified heading still scaffold — **G3**.

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | live aibridge Unknown | **no** (WAIVED-likely info) | soft G4; harness Present |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | story §Verified heading | **yes** (docs) | As-of-Done retitle |
| G4 | Low | task README Await P3 / Absent | **yes** (docs) | align Code Facts to evidence |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 4.  
**TASKED-likely (docs):** G3, G4.  
**WAIVED-likely:** G1 (info), G2 (operator).

**Product Story Done ≠ empty OPEN gap-list** — зафиксировано явно.  
**Hard break / contract invent:** **none** · Default Pass (no GW code) **holds**.

---

## 6. Non-goals honored (story Out of scope)

- Interview / telegram / sense-brief redesign — Absent this story.  
- New stash fields without lock — Absent.  
- SPA-REQ15 UX / aibridge FSM rewrite — out of scope; peer client read-only.  
- Invent live PASS — Absent (Unknown explicit).  
- No push; immutable pkg-000117 unchanged this audit.
