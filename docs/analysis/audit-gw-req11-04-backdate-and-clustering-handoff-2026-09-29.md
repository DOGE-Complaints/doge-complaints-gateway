# Hard Audit — STORY-GW-REQ11-04 backdate + clustering handoff (2026-09-29)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-04-backdate-and-clustering-handoff`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md) (T01–T06, **pkg-000103**).  
**Pipeline:** [`…/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md).  
**Pkg:** [`pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml`](../tasks/gateway-active-packages/pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-04.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-04-backdate-and-clustering-handoff/task-gw-req11-04-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-04.md) PASS **2026-09-29T14:39:37Z** (lock-B + docs; live backdate blocked by pool).  
**Run-summary:** [`run-summary-20260929-1439-gw-req11-04-p3.md`](../tasks/run-reports/run-summary-20260929-1439-gw-req11-04-p3.md).  
**Operator note:** [`note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`](./note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md).  
**Прогон этого аудита:** `utc_now: 2026-09-29T14:42:45Z`. Branch: **`dev`**. Live: pytest → **6 passed**; dry-run `--life-sim --max 3` → **3/3** (+ fixture `created_at` lines + banner lock-B PATCH); pool ready_env_slots / `.env` nonempty **0/20**; wait script on disk.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L769 / L832–841. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: AC tooling/docs PASS; live submit→backdate PASS-via-blocker; Product Done = yes (with residual); 4 gaps; TASKED-likely = G2 (+ G1 ops/WAIVE)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Stamp evidence + service-auth candidates | note T01; `services.py:313` / `:579`; fixtures on disk | ✅ PASS |
| **T02** | Lock-B service-auth backdate | `PATCH /ops/stories/{id}/created-at` [`asgi_app.py:453–473`](../../src/core/api/asgi_app.py); [`handle_story_created_at_backdate`](../../src/core/api/handlers.py:228); `update_created_at` InMemory/SQLite/Supabase; API_REFERENCE § | ✅ PASS |
| **T03** | Replay apply fixture timestamps | [`patch_story_created_at_http`](../../tests/simulation_intake_http.py:267); [`main_life_sim`](../../tests/simulation_runner.py:291–309) after submit; dry-run prints `created_at` | ✅ PASS *(live HTTP blocked)* |
| **T04** | Clustering wait runbook/script | note T04 + [`life_sim_wait_clustering.sh`](../../tests/sandbox/life_sim_wait_clustering.sh); `CLUSTER_MIN_SIZE=8` [`example.env:69`](../../example.env); cron L99–100 | ✅ PASS |
| **T05** | K3 card count follows clustering | note T05; no invent cluster APIs; test asserts K3 / no invent | ✅ PASS |
| **T06** | Gate AC-01…03 | Gate PASS 14:39:37Z | ✅ PASS |

**Verdict product:** GW-REQ11-04 **исполнена по gate framing** (ops route + repo + runner wire + clustering/K3 docs). Live stash→submit→PATCH backdate **not** proven — **operator blocker** `LIFE_SIM_POOL_*` **0/20** (carried from REQ11-03).  
**Product Story Done (AC/DoD) = yes** — holds **with** documented blocker + unit/contract path (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay — Product Done vs live pool blocker

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Fixture times via lock-B after stash→submit | **PASS*** | Route + `update_created_at` + helper + runner; `test_ac01_*` (auth 401, happy 200, not in `PUBLIC_ROUTES`, InMemory/SQLite). Dry-run 3/3 shows fixture `created_at`. *Live HTTP submit→backdate blocked by pool 0/20. |
| AC-02 Clustering wait before threads seed | **PASS** | note T04 + `tests/sandbox/life_sim_wait_clustering.sh` (echo knobs + 2× `CLUSTER_CRON_INTERVAL_S` sleep); no new cluster HTTP |
| AC-03 K3 card count; no invent cluster APIs | **PASS** | note T05; `test_ac02_ac03_clustering_handoff_docs_present` |

### Does Product Done hold with documented blocker?

**Yes — under gate/story DoD as shipped:** AC-01 closed via product path + unit tests + dry-run orchestration; live E2E called out as PASS* / Operator blocker (gate + run-summary-1439). AC-02/03 are docs/runbook Deliverables — present on disk.

**Caveat:** residual live Pass (real multi-Bearer submit then lock-B PATCH with fixture times) still needs pool creds → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Submit stamps `created_at=now` | `services.py:313` (+ `:579` signal) | ✅ |
| Ops route + Depends service-auth | `asgi_app.py:453–455` `require_public_content_service_auth` | ✅ |
| Handler parse + `update_created_at` | `handlers.py:211–265` | ✅ |
| Repos implement `update_created_at` | `repositories.py:106`; `db_sqlite.py:801`; `db_supabase.py:741` | ✅ |
| Runner lock-B after submit | `simulation_runner.py:244`, `:291–309` | ✅ |
| Wait script | `life_sim_wait_clustering.sh` | ✅ |
| `CLUSTER_MIN_SIZE` / cron | `example.env:69`, `:99–100` | ✅ |
| Pool filled | ready **0/20** | ✅ matches gate |
| Branch | `dev` | ✅ |
| pytest | **6 passed** | ✅ |

---

## 3. Регрессии / gaps

### G1 — Live pool creds 0/20; live submit→backdate unproven · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Fail-closed without inventing secrets (REQ11-03 carry-forward). Until `LIFE_SIM_POOL_00..19_*` filled, AC-01 literal end-to-end «fixture times survive intake» remains contract/unit + dry-run only.

**Как закрыть (P5 hint):** TASKED ops — bootstrap 20 verified users + env; non-dry `--life-sim` sample proving PATCH 200 after submit; append evidence. Or WAIVE operator if tooling+blocker accepted (same class as REQ11-03 G1).

### G2 — T01–T05 Code Facts still present-tense «Absent» · severity: **LOW** · **TASKED-likely**

Status/DoD checkboxes = Done, но Code Facts / Gap still claim Absent (T01 intake backdate Absent; T02 lock-B path Absent; T03 replay via B Absent; T04 wait Absent; T05 K3 note Absent) — e.g. T02 `:23`, T03 `:22`, T04 `:22`.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on T01–T05 Code Facts/Gap (mirror REQ11-01…03 T0x SSOT pattern).

### G3 — Bullrun §«Актуальная точка» без REQ11-04 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) MVP lead still EPIC-M2-24 / ES-03. Story L769 + tasks L836–841 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G4 — Note omits path to committed wait script · severity: **LOW** · **TASKED-likely** (docs) / WAIVE-able

Gate/story Verified cite `tests/sandbox/life_sim_wait_clustering.sh`; note T04 embeds equivalent bash but **does not** name the `.sh` path (`rg` → no hit). Script exists and matches intent; SSOT pointer incomplete.

**Как закрыть:** TASKED docs — one line in note pointing at `life_sim_wait_clustering.sh`. Or WAIVE if embedded runbook alone accepted for AC-02.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L769 GW-REQ11-04 | ✅ Done · lock B PATCH · pool 0/20 · pkg-000103 | Product Done (blocker) | PASS* + **G1** |
| T01 | L836 | ✅ stamp evidence note | Done | PASS |
| T02 | L837 | ✅ `PATCH /ops/stories/{id}/created-at` | Done | PASS |
| T03 | L838 | ✅ `--life-sim` lock-B after submit | Done | PASS (dry-run) |
| T04 | L839 | ✅ CLUSTER_* + wait script | Done | PASS (+ **G4** note pointer) |
| T05 | L840 | ✅ K3; no invent cluster APIs | Done | PASS |
| T06 | L841 | ✅ AC-01…03 PASS | Gate PASS | PASS |
| Journal | L2037 | P3 execute 1439 | present | PASS |
| §Актуальная точка | (MVP lead) | EPIC-M2-24 | n/a | **G3** WAIVED-likely |

**Emoji note (non-blocking):** siblings REQ11-01…03 use 🔵 Done; REQ11-04 rows use ✅ — same semantic Done; not a product gap.

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live pool 0/20; submit→backdate unproven | **yes** (ops) or WAIVE operator | fail-closed correct; carry REQ11-03 |
| G2 | Low | T01–T05 Code Facts «Absent» vs Status Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G4 | Low | note missing `.sh` path pointer | **yes** (docs) or WAIVE | script on disk; AC-02 still PASS |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 3.  
**Actionable TASKED-likely:** up to 3 (G1, G2, G4).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
