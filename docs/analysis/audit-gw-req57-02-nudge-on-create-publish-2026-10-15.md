# Hard Audit — STORY-GW-REQ57-02 thin nudge on create/publish (2026-10-15)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ57-02-nudge-on-create-publish`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-02-nudge-on-create-publish/STORY-GW-REQ57-02-nudge-on-create-publish.md) (T01–T07, **pkg-000114**) · backlog [`…/STORY-GW-REQ57-02-…`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md).  
**Pkg:** [`pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml`](../tasks/gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ57-02.md`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-02-nudge-on-create-publish/task-gw-req57-02-t07-story-gate/story-acceptance-gate-STORY-GW-REQ57-02.md) PASS **2026-10-15T11:41:13Z**.  
**Run-summary:** [`run-summary-20261015-1141-gw-req57-02-p3.md`](../tasks/run-reports/run-summary-20261015-1141-gw-req57-02-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-15T11:44:22Z`. Branch: **`dev`**. Live: `pytest -q tests/test_gw_req57_02_nudge_on_create_publish.py` → **8 passed** (0.04s). `--verify` → **ok 7** (pkg-000114).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T07 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1108 / L1116–1122. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; nudge client + pending hook + fail-closed; 8 tests; 4 gaps (bullrun + soft evidence/docs); TASKED-likely soft = G1/G3/G4

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | locked AIBRIDGE_* env | [`schema.py`](../../src/core/config/schema.py) ENV_SCHEMA + load; [`example.env`](../../example.env) L121–127; unit `test_req57_02_config_env_names_locked` | ✅ PASS |
| **T02** | HTTP client accept + Bearer | [`sense_brief_nudge.py`](../../src/core/application/sense_brief_nudge.py) `ACCEPT_PATH` + `Authorization: Bearer`; transport double asserts URL/body/auth | ✅ PASS |
| **T03** | optional corpus from Stories | `build_corpus_from_stories` + create path corpus in body | ✅ PASS |
| **T04** | create/publish → pending + nudge | `_apply_pending_and_nudge` on `_create_issue` + `create_manual_issue`; factory wire [`service_factory.py`](../../src/core/infrastructure/service_factory.py) | ✅ PASS† |
| **T05** | fail-closed | disabled / missing_config / http 503 → pending kept, no ready pretend | ✅ PASS |
| **T06** | HTTP double suite | [`test_gw_req57_02_nudge_on_create_publish.py`](../../tests/test_gw_req57_02_nudge_on_create_publish.py) **8 passed** | ✅ PASS |
| **T07** | gate AC-01…04 | Gate PASS 11:41:13Z | ✅ PASS |

† Product hook Present. ASGI test only GETs seeded pending (see **G1**); `create_manual_issue` unwired in suite (see **G4**).

**Verdict product:** GW-REQ57-02 **исполнена по gate framing** (pending + thin nudge · locked env · fail-closed · HTTP double · no live aibridge/LLM).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-GW-REQ5702-01 create/publish → pending + nudge observable | **PASS**† | `test_req57_02_create_sets_pending_and_nudges` (service create); ASGI GET pending — see **G1** |
| AC-GW-REQ5702-02 URL/body/auth + locked env names | **PASS** | accept URL `…/v1/worker/sense-brief/accept`; Bearer S2S; body `issue_id`+`generation_version`(+`corpus`); ENV_SCHEMA names |
| AC-GW-REQ5702-03 HTTP test double, no live aibridge | **PASS** | `_RecordingTransport`; **8 passed** this audit |
| AC-GW-REQ5702-04 missing/disabled → fail-closed | **PASS** | disabled + missing_config + 503 tests; pending remains; no `ready` |

† AC-01 service create path Present; ASGI `POST /node/issues` + live nudge not exercised in suite — residual **G1**.

### Focus re-checks

| Focus | Result |
|-------|--------|
| `POST {AIBRIDGE_BASE_URL}/v1/worker/sense-brief/accept` | ✅ `ACCEPT_PATH` + `accept_url` |
| Bearer `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | ✅ header in `nudge()` |
| Gate `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED` | ✅ settings.enabled; default `false` in example.env |
| pending + `generation_version=v1` | ✅ `mark_generation_pending` / `INITIAL_GENERATION_VERSION` |
| Fail-closed (no pretend success) | ✅ skip HTTP when disabled/missing; keep pending on 503 |
| No LLM/image in gateway | ✅ outbound HTTP only |
| Hook on `_create_issue` | ✅ after first save |
| Hook on `create_manual_issue` | ✅ code Present; **no dedicated test** — **G4** |
| Hook on `_extend_issue` | ✅ Absent (not create/publish; brief-wins stays REQ57-01) |
| Tests | ✅ 8 passed |
| Branch | ✅ `dev` |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Nudge module | `src/core/application/sense_brief_nudge.py` | ✅ |
| Config | `src/core/config/schema.py` AIBRIDGE_* | ✅ |
| example.env | `example.env` L121–127 | ✅ |
| Hook | `issue_create.py` `_apply_pending_and_nudge` | ✅ |
| Factory DI | `service_factory.py` `build_nudge_service_from_config` | ✅ |
| Offline tests | `tests/test_gw_req57_02_nudge_on_create_publish.py` | ✅ 8 |
| Peer path match | handoff accept `/v1/worker/sense-brief/accept` | ✅ |
| No live aibridge | HTTP double only | ✅ |

---

## 3. Регрессии / gaps

### G1 — ASGI evidence = GET seeded pending, not POST create + nudge · severity: **LOW** · **TASKED-likely** (soft)

[`test_req57_02_asgi_create_pending_observable`](../../tests/test_gw_req57_02_nudge_on_create_publish.py) seeds projection via `mark_generation_pending` + `store.save_projection`, then `GET /node/issues/…`. Does **not** `POST /node/issues` or assert transport call on ASGI create. Service-level create+nudge Covered by `test_req57_02_create_sets_pending_and_nudges`. Gate already PASS for Product Done.

**Как закрыть:** TASKED test — ASGI/service-auth create path with recording transport → pending + 1 accept call; **or** P5 WAIVE if unit create+nudge accepted as AC-01 evidence (gate already did).

### G2 — Bullrun §«Актуальная точка» без REQ57-02 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1108 + tasks L1116–1122 Done; epic banner + P3 note: §Актуальная точка **не** переписана.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — Backlog §Code touchpoints still scaffold phrasing · severity: **LOW** · **TASKED-likely**

[`backlog …/STORY-GW-REQ57-02-….md:59–63`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md): «New outbound HTTP client module (implement choice)» while `sense_brief_nudge.py` Present and §Verified As-of-Done. Nested tasks already Done.

**Как закрыть:** TASKED docs — align Code touchpoints with As-of-Done paths (`sense_brief_nudge.py`, `issue_create.py`, `schema.py`).

### G4 — `create_manual_issue` hook unwired in suite · severity: **LOW** · **TASKED-likely** (soft)

T04 Code Facts claim hook on `create_manual_issue` — Present at [`issue_create.py:518–523`](../../src/core/application/issue_create.py). No test calls `create_manual_issue` under nudge. Primary `_create_issue` Covered.

**Как закрыть:** TASKED test — one `create_manual_issue` → pending + optional nudge call; **or** WAIVE if operator treats `_create_issue` as sufficient publish evidence.

### G5 — ENV-CHECKLIST «unset ENABLED» vs `_require_value` boot · severity: **LOW** · **TASKED-likely** (soft docs) / WAIVE-ok

[`ENV-CHECKLIST.md:17`](../tasks/backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md): «if unset/false → fail-closed». Product: `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED` is `_require_value` at config load ([`schema.py:672–675`](../../src/core/config/schema.py)) — **unset fails boot**, not nudge-time fail-closed. `false` / missing URL|token when enabled → nudge fail-closed (tests). example.env sets `=false`.

**Как закрыть:** TASKED docs — clarify unset = config load fail; false/missing peer env = runtime fail-closed; **or** WAIVE as checklist wording soft.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1108 GW-REQ57-02 | 🔵 Done · gate PASS · suite **8** · pkg-000114 | Product Done | PASS |
| T01 | L1116 | Done · locked AIBRIDGE_* | Done | PASS |
| T02 | L1117 | Done · accept + Bearer · AC-02 | Done | PASS |
| T03 | L1118 | Done · optional corpus | Done | PASS |
| T04 | L1119 | Done · pending + nudge · AC-01 | Done (+ G1/G4 residual) | PASS |
| T05 | L1120 | Done · AC-04 | Done | PASS |
| T06 | L1121 | Done · suite **8** | 8 passed this audit | PASS |
| T07 | L1122 | Done · AC-01…04 PASS | Gate PASS | PASS |
| P3 note | L1124 | gate PASS · no §Актуальная точка rewrite | matches | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | ASGI create+nudge evidence soft | **yes** (soft) | test add or WAIVE |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | backlog Code touchpoints scaffold | **yes** | docs align |
| G4 | Low | create_manual_issue untested | **yes** (soft) | test add or WAIVE |
| G5 | Low | ENV-CHECKLIST unset vs require | **yes** (soft docs) | wording or WAIVE |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 5.  
**TASKED-likely (docs):** G3, G5.  
**TASKED-likely (soft test):** G1, G4.  
**WAIVED-likely:** G2.

**Product Story Done ≠ empty OPEN gap-list** — зафиксировано явно.

---

## 6. Non-goals honored (story Out of scope)

- Bind receiver → REQ57-01 — not re-audited as this story.  
- Sweep / regenerate → 03/04.  
- Live aibridge/LLM — Absent; HTTP double only.  
- No push; immutable pkg-000114 unchanged this audit.
