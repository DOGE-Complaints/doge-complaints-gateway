# Hard Audit — STORY-GW-REQ57-01 bind-in + projection apply (2026-10-15)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ57-01-bind-in-projection-apply`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/STORY-GW-REQ57-01-bind-in-projection-apply.md) (T01–T08, **pkg-000113**) · backlog [`…/STORY-GW-REQ57-01-…`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md).  
**Pkg:** [`pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml`](../tasks/gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ57-01.md`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/task-gw-req57-01-t08-story-gate/story-acceptance-gate-STORY-GW-REQ57-01.md) PASS **2026-10-15T11:13:59Z**.  
**Run-summary:** [`run-summary-20261015-1113-gw-req57-01-p3.md`](../tasks/run-reports/run-summary-20261015-1113-gw-req57-01-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-15T11:18:07Z`. Branch: **`dev`** (gateway git root). Live: `pytest -q tests/test_gw_req57_01_bind_in_projection_apply.py` → **8 passed** (0.06s). `--verify` → **ok 8** (pkg-000113).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T08 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1107 / L1116–1123. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; bind route + apply + brief-wins wire; 8 tests; 4 gaps (SSOT + test evidence + bullrun + T06 Where); TASKED-likely = G1 (+ soft G3/G4)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | generation fields persist (DP5) | [`columnar_storage.py`](../../src/core/projection/columnar_storage.py) `_OPTIONAL_SCALARS` + SQLite migrate [`db_sqlite.py`](../../src/core/infrastructure/db_sqlite.py) + InMemory [`repositories.py`](../../src/core/infrastructure/repositories.py) + Supabase via `payload_to_storage_fields` [`db_supabase.py:947–974`](../../src/core/infrastructure/db_supabase.py) + [`20261015_1104_gw_req57_01_generation_fields.sql`](../../supabase/migrations/20261015_1104_gw_req57_01_generation_fields.sql); no job table | ✅ PASS |
| **T02** | public locked keys | `apply_public_generation_keys` + [`dto.py`](../../src/core/projection/dto.py) `to_public_dict`; list/get tests | ✅ PASS |
| **T03** | success bind apply | [`sense_brief_bind.py`](../../src/core/application/sense_brief_bind.py) success branch → ready + https poster + title≤80 | ✅ PASS |
| **T04** | fail bind apply | fail branch → failed + `[Brief unavailable]` + reason_class log; reject apply on fail | ✅ PASS |
| **T05** | route + service-auth | [`asgi_app.py:618–635`](../../src/core/api/asgi_app.py) `POST /v1/issue-sense-brief/bind` + `require_public_content_service_auth` → [`ServiceTokenAuth.require`](../../src/core/api/security.py) vs `SERVICE_API_TOKEN` | ✅ PASS |
| **T06** | brief-wins guard | `preserve_brief_wins_fields` + wire in [`issue_create.py`](../../src/core/application/issue_create.py) `_extend_issue` (~375–387); **not** in `extraction_policy.py` | ✅ PASS† |
| **T07** | stub suite | [`test_gw_req57_01_bind_in_projection_apply.py`](../../tests/test_gw_req57_01_bind_in_projection_apply.py) **8 passed** this audit | ✅ PASS |
| **T08** | gate AC-01…07 | Gate PASS 11:13:59Z | ✅ PASS |

† Product wire Present on `_extend_issue` save path. ASGI evidence for AC-06 is helper + manual save (see **G3**).

**Verdict product:** GW-REQ57-01 **исполнена по gate framing** (bind path · success/fail apply · public keys · brief-wins on extend · stub 8 · no live LLM · DP5).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-GW-REQ5701-01 success bind → title/summary ≠ dominant baseline | **PASS** | `test_req57_01_success_bind_applies_title_summary_ready`; `IssueSenseBriefBindService` success branch |
| AC-GW-REQ5701-02 title ≤80 / plain | **PASS** | `_plain_title` (collapse whitespace, len≤80); `test_req57_01_title_max_80` → 400 |
| AC-GW-REQ5701-03 public `poster_url` when ready | **PASS** | GET `/node/issues/{id}` + list test; `apply_public_generation_keys` requires https + ready |
| AC-GW-REQ5701-04 `generation_status` pending/ready/failed distinguishable | **PASS** | seed pending / success ready / fail failed in suite |
| AC-GW-REQ5701-05 fail → failed + no pretend AI sense | **PASS** | `test_req57_01_fail_bind_sets_failed_no_pretend` + reject apply body |
| AC-GW-REQ5701-06 ready brief not overwritten without regenerate | **PASS**† | unit `test_req57_01_brief_wins_guard_unit` + `test_req57_01_brief_wins_on_extend_save`; code wire `_extend_issue` — see **G3** |
| AC-GW-REQ5701-07 stub unit/ASGI, no live LLM | **PASS** | **8 passed** live this audit |

† AC-06 product path on `_extend_issue` Present; dedicated test does **not** call `IssueCreateService._extend_issue` — residual **G3**.

### Focus re-checks

| Focus | Result |
|-------|--------|
| `POST /v1/issue-sense-brief/bind` | ✅ ASGI + handler |
| `SERVICE_API_TOKEN` service-auth | ✅ `require_public_content_service_auth` → compare_digest; missing Bearer → 401 |
| Channel / wrong Bearer | ✅ reject by token inequality (code); dedicated wrong-token test Absent — **G5** soft |
| DP5 no job table | ✅ fields on `doge_issues` only; migration ALTER columns |
| Brief wins until regenerate | ✅ `preserve_brief_wins_fields` when `generation_status==ready` |
| Pending on create/publish | Out of scope this story (→ REQ57-02); not scored as product fail |
| Tests | ✅ 8 passed |
| Branch | ✅ `dev` |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Bind route | `src/core/api/asgi_app.py` `@app.post("/v1/issue-sense-brief/bind")` | ✅ |
| Handler | `src/core/api/handlers.py` `handle_issue_sense_brief_bind` | ✅ |
| Apply service | `src/core/application/sense_brief_bind.py` | ✅ |
| Brief-wins helper + `_extend_issue` | `sense_brief_bind.preserve_brief_wins_fields` + `issue_create.py` | ✅ |
| Brief-wins in `extraction_policy.py` | rg — no matches | ✅ Absent (guard at save, not extraction) |
| Columnar + public keys | `columnar_storage.py` | ✅ |
| DTO | `dto.py` generation_* fields | ✅ |
| SQLite + migrate | `db_sqlite.py` + supabase migration SQL | ✅ |
| Offline tests | `tests/test_gw_req57_01_bind_in_projection_apply.py` | ✅ 8 |
| No live LLM in suite | stub JSON only | ✅ |

---

## 3. Регрессии / gaps

### G1 — Backlog story SSOT still scaffold Absent / Planned vs product Done · severity: **LOW** · **TASKED-likely**

[`backlog-stories/…/STORY-GW-REQ57-01-….md`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md): §Verified still «Bind receiver … **Absent**»; Nested tasks table still **Planned**; §Code touchpoints still «`extraction_policy.py` — brief-wins guard». Meta Status claims Done / gate PASS — contradictory. Pipeline story already As-of-Done.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog Verified + nested task statuses + Code touchpoints paths; mirror pipeline.

### G2 — Bullrun §«Актуальная точка» без REQ57-01 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1107 + tasks L1116–1123 Done; epic banner + P3 note: §Актуальная точка **не** переписана.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — AC-06 test evidence = helper + manual save, not live `_extend_issue` · severity: **LOW** · **TASKED-likely** (soft)

`test_req57_01_brief_wins_on_extend_save` calls `preserve_brief_wins_fields` then `store.save_projection` directly — does not invoke `IssueCreateService._extend_issue`. Product wire at [`issue_create.py:375–387`](../../src/core/application/issue_create.py) Present (read-verified). Gate already PASS for Product Done.

**Как закрыть:** TASKED test — one path through `_extend_issue` / create-extend with ready brief; **or** P5 WAIVE if operator accepts helper+code-wire as sufficient S6 evidence.

### G4 — T06 «Where to change» still cites `extraction_policy.py` · severity: **LOW** · **TASKED-likely**

[`task-gw-req57-01-t06-…/README.md`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/task-gw-req57-01-t06-brief-wins-guard/README.md) §Where to change: `extraction_policy.py`; §Code Facts correctly cite `sense_brief_bind.py` + `issue_create.py`. Product: no brief-wins in extraction_policy (rg empty).

**Как закрыть:** TASKED docs — align Where to change with As-of-Done paths.

### G5 — Scope #5 wrong Bearer / worker S2S: no dedicated ASGI case · severity: **LOW** · **TASKED-likely** (soft) / WAIVE-ok

Only `test_req57_01_bind_requires_service_auth` (no Authorization → 401). Reject of non-`SERVICE_API_TOKEN` Bearer is Present via [`security.py:114–118`](../../src/core/api/security.py) `compare_digest` under `require_public_content_service_auth`. No test with wrong/channel token.

**Как закрыть:** TASKED test — Bearer ≠ service token → 401; **or** WAIVE if missing-auth + compare_digest accepted as Scope #5 evidence.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1107 GW-REQ57-01 | 🔵 Done · gate PASS · bind · stub 8 · pkg-000113 | Product Done | PASS |
| T01 | L1116 | Done · columnar + SQLite migrate · DP5 | Done | PASS |
| T02 | L1117 | Done · AC-03/04 | Done | PASS |
| T03 | L1118 | Done · AC-01/02 | Done | PASS |
| T04 | L1119 | Done · AC-05 | Done | PASS |
| T05 | L1120 | Done · `POST /v1/issue-sense-brief/bind` | Done | PASS |
| T06 | L1121 | Done · AC-06 | Done (+ G3/G4 residual) | PASS |
| T07 | L1122 | Done · stub suite **8** | 8 passed this audit | PASS |
| T08 | L1123 | Done · AC-01…07 PASS | Gate PASS | PASS |
| P3 note | L1125 | gate PASS · no §Актуальная точка rewrite | matches | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | backlog SSOT scaffold vs Done | **yes** | Verified / nested / touchpoints |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | AC-06 evidence ≠ live `_extend_issue` | **yes** (soft) | test add or WAIVE |
| G4 | Low | T06 Where to change path drift | **yes** | docs align |
| G5 | Low | Scope #5 wrong-token test absent | **yes** (soft) | test add or WAIVE |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 5.  
**TASKED-likely (strict docs):** G1, G4.  
**TASKED-likely (soft test):** G3, G5.  
**WAIVED-likely:** G2.

**Product Story Done ≠ empty OPEN gap-list** — зафиксировано явно.

---

## 6. Non-goals honored (story Out of scope)

- Thin nudge / pending-on-create → REQ57-02 — not implemented; not scored fail.  
- Sweep / regenerate → 03/04.  
- Live LLM / SPA / Arweave MVP poster — Absent in suite and bind path.  
- No push; immutable pkg-000113 unchanged this audit.
