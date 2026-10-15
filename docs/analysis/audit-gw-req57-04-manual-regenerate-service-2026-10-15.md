# Hard Audit — STORY-GW-REQ57-04 manual regenerate service-auth (2026-10-15)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ57-04-manual-regenerate-service`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/STORY-GW-REQ57-04-manual-regenerate-service.md) (T01–T06, **pkg-000116**) · backlog [`…/STORY-GW-REQ57-04-…`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md).  
**Pkg:** [`pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml`](../tasks/gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ57-04.md`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/task-gw-req57-04-t06-story-gate/story-acceptance-gate-STORY-GW-REQ57-04.md) PASS **2026-10-15T12:23:00Z**.  
**Run-summary:** [`run-summary-20261015-1223-gw-req57-04-p3.md`](../tasks/run-reports/run-summary-20261015-1223-gw-req57-04-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-15T12:26:16Z`. Branch: **`dev`**. Live: `pytest -q tests/test_gw_req57_04_manual_regenerate_service.py` → **6 passed** (0.04s). `--verify` → **ok 6** (pkg-000116).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1110 / L1116–1121. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; regenerate apply + route service-auth + nudge + citizen reject; 6 tests; 4 gaps (bullrun + soft docs/evidence); TASKED-likely soft = G1/G3/G4

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | bump → pending; keep brief; omit public poster | [`sense_brief_regenerate.py`](../../src/core/application/sense_brief_regenerate.py) `bump_generation_version` / `mark_regenerate_pending` / `SenseBriefRegenerateService.regenerate` + [`apply_public_generation_keys`](../../src/core/projection/columnar_storage.py) | ✅ PASS† |
| **T02** | `POST /v1/issue-sense-brief/regenerate` + service-auth | [`asgi_app.py:665–682`](../../src/core/api/asgi_app.py) `Depends(require_public_content_service_auth)` · [`handlers.py:653–709`](../../src/core/api/handlers.py) | ✅ PASS |
| **T03** | nudge with new `generation_version` (02 client) | `regenerate` → `nudge_service.nudge(..., generation_version=new_version)` · reuse [`sense_brief_nudge.py`](../../src/core/application/sense_brief_nudge.py) | ✅ PASS |
| **T04** | missing / citizen Bearer → 401 | same service-auth dep; tests 401 | ✅ PASS |
| **T05** | stub suite | [`test_gw_req57_04_manual_regenerate_service.py`](../../tests/test_gw_req57_04_manual_regenerate_service.py) **6 passed** | ✅ PASS |
| **T06** | gate AC-01…04 | Gate PASS 12:23:00Z | ✅ PASS |

† Product apply Present. T01 Purpose wording soft vs omit-poster (see **G3**).

**Verdict product:** GW-REQ57-04 **исполнена по gate framing** (service-token regenerate · bump+pending+nudge · no citizen · distinct version key · HTTP double · no live aibridge).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-GW-REQ5704-01 service token → version bump + pending + nudge | **PASS** | `test_req57_04_asgi_service_token_bumps_pending_and_nudges` + `test_req57_04_unit_regenerate_bumps_pending_and_nudges` — v1→v2, pending, accept body |
| AC-GW-REQ5704-02 without service auth → rejected | **PASS** | `test_req57_04_asgi_missing_auth_rejected` → **401** |
| AC-GW-REQ5704-03 citizen Bearer cannot regenerate | **PASS** | `test_req57_04_asgi_citizen_bearer_rejected` → **401** |
| AC-GW-REQ5704-04 new version distinct peer idempotency key | **PASS** | `test_req57_04_bump_generation_version_distinct` + ASGI/unit assert `generation_version` ≠ prior |

### Focus re-checks

| Focus | Result |
|-------|--------|
| Locked path `POST /v1/issue-sense-brief/regenerate` | ✅ `asgi_app.py:665–668` |
| Auth = `SERVICE_API_TOKEN` family (`require_public_content_service_auth` → `ServiceTokenAuth.require` mandatory) | ✅ `asgi_app.py:368–372` · `security.py:107–118` · `build_service_auth_from_env` |
| Bump then pending then nudge order | ✅ save_projection pending **before** `nudge_service.nudge` (`sense_brief_regenerate.py:100–115`) |
| Brief title/summary kept | ✅ `mark_regenerate_pending` keeps title/summary; test asserts |
| Public `poster_url` omitted while not ready | ✅ `apply_public_generation_keys` pops unless `generation_status==ready` |
| Reuse 02 nudge client / accept path | ✅ `ACCEPT_PATH` `/v1/worker/sense-brief/accept` · Bearer S2S |
| No citizen regenerate endpoint | ✅ single route; service-auth only |
| No LLM/image in gateway | ✅ outbound nudge only |
| Tests | ✅ **6 passed** this audit |
| Branch | ✅ `dev` |
| Immutable pkg | ✅ pkg-000116 · `--verify` ok 6 |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Regenerate service | `src/core/application/sense_brief_regenerate.py` | ✅ |
| Route | `asgi_app.py` L665–682 | ✅ |
| Handler | `handlers.py` `handle_issue_sense_brief_regenerate` L653–709 | ✅ |
| Nudge reuse | `sense_brief_nudge.py` | ✅ |
| Public key normalize | `columnar_storage.py` `apply_public_generation_keys` | ✅ |
| Offline tests | `tests/test_gw_req57_04_manual_regenerate_service.py` | ✅ 6 |
| Gate / run-summary | T06 gate + `run-summary-20261015-1223-…` | ✅ PASS |
| Arch DP6 §2.5 | bump → pending → nudge; service token only | ✅ product matches |

---

## 3. Регрессии / gaps

### G1 — Pipeline story Meta Status still «Waiting Acceptance» · severity: **LOW** · **TASKED-likely** (docs)

[`STORY-GW-REQ57-04-….md:7`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/STORY-GW-REQ57-04-manual-regenerate-service.md): `Implemented (Waiting Acceptance)` while Nested T01–T06 Done, gate PASS, bullrun L1110 **Done**, backlog Meta **Done (Awaiting Commits)**. Soft status drift only; product AC unaffected.

**Как закрыть:** TASKED docs — align pipeline story Status with gate/bullrun/backlog (Done / Awaiting Commits); **or** WAIVE if operator treats Waiting Acceptance as intentional pre-P8 label.

### G2 — Bullrun §«Актуальная точка» без REQ57-04 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1110 + tasks L1116–1121 Done; P3 note L1123: §Актуальная точка **не** переписана.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — T01 Purpose «Keep poster until new bind» vs omit `poster_url` · severity: **LOW** · **TASKED-likely** (docs soft)

T01 Purpose ([`task-gw-req57-04-t01-…/README.md:18`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/task-gw-req57-04-t01-regenerate-apply/README.md)): «Keep poster until new bind». Product: `mark_regenerate_pending` → `apply_public_generation_keys` **omits** `poster_url` while not ready ([`sense_brief_regenerate.py:58–70`](../../src/core/application/sense_brief_regenerate.py); test `test_req57_04_mark_regenerate_keeps_brief_title`). T01 Code Facts / Acceptance correctly say omit public poster. Soft Purpose wording only.

**Как закрыть:** TASKED docs — Purpose = keep brief title/summary; omit public `poster_url` until ready bind; **or** WAIVE if Purpose «poster» meant brief content loosely.

### G4 — Unknown / empty `issue_id` → 400 untested · severity: **LOW** · **TASKED-likely** (soft) / WAIVE-ok

Handler maps `SenseBriefRegenerateError` → **400** ([`handlers.py:704–705`](../../src/core/api/handlers.py)); service raises on empty / unknown issue ([`sense_brief_regenerate.py:87–92`](../../src/core/application/sense_brief_regenerate.py)). Suite covers AC auth + happy path only — **no** ASGI/unit assert for missing Issue / empty `issue_id`. Not AC-GW-REQ5704-01…04; soft negative-path evidence.

**Как закрыть:** TASKED test — empty + unknown `issue_id` → 400 with service token; **or** WAIVE info-nonblocking (out of AC; error path Present in code).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1110 GW-REQ57-04 | 🔵 Done · gate PASS · suite **6** · pkg-000116 | Product Done | PASS† |
| T01 | L1116 | Done · bump → pending · AC-01 | Done | PASS (+ G3 Purpose soft) |
| T02 | L1117 | Done · `POST …/regenerate` · DP6 | Done | PASS |
| T03 | L1118 | Done · reuse 02 · AC-04 | Done | PASS |
| T04 | L1119 | Done · AC-02/03 · no citizen | Done | PASS |
| T05 | L1120 | Done · suite **6** | 6 passed this audit | PASS (+ G4 residual) |
| T06 | L1121 | Done · AC-01…04 PASS | Gate PASS | PASS |
| P3 note | L1123 | gate PASS · no §Актуальная точка rewrite | matches | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

† Pipeline story Meta Status still Waiting Acceptance — **G1** (bullrun Done claim still matches gate/product).

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | pipeline story Status drift | **yes** (docs) | Waiting Acceptance vs Done |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | T01 Purpose poster wording | **yes** (docs) | Purpose vs omit-poster Code Facts |
| G4 | Low | unknown/empty issue_id untested | **yes** (soft) / WAIVE info | 400 path Present; not AC |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 4.  
**TASKED-likely (docs):** G1, G3.  
**TASKED-likely (soft test/evidence):** G4.  
**WAIVED-likely:** G2.

**Product Story Done ≠ empty OPEN gap-list** — зафиксировано явно.

---

## 6. Non-goals honored (story Out of scope)

- Citizen regenerate / SPA UI — Absent; rejected by service-auth.  
- Auto-regen on Story merge (REQ13 L9) — Absent.  
- Bind/nudge first implement → 01/02 — reused, not reinvented.  
- Live aibridge/LLM — Absent; HTTP double only.  
- No push; immutable pkg-000116 unchanged this audit.
