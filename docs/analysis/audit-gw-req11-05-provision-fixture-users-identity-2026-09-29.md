# Hard Audit — STORY-GW-REQ11-05 provision fixture users Identity + secrets (2026-09-29)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-05-provision-fixture-users-identity`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md) (T01–T07, **pkg-000104**).  
**Pipeline:** [`…/STORY-GW-REQ11-05-provision-fixture-users-identity.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md).  
**Pkg:** [`pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml`](../tasks/gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-05.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/task-gw-req11-05-t07-story-gate/story-acceptance-gate-STORY-GW-REQ11-05.md) PASS* **2026-09-29T18:15:05Z**.  
**Run-summary:** [`run-summary-20260929-1815-gw-req11-05-p3.md`](../tasks/run-reports/run-summary-20260929-1815-gw-req11-05-p3.md).  
**Operator note:** [`note-gw-req11-05-provision-fixture-users-identity-2026-09-29.md`](./note-gw-req11-05-provision-fixture-users-identity-2026-09-29.md).  
**Прогон этого аудита:** `utc_now: 2026-09-29T18:16:58Z`. Branch: **`dev`**. Live: pytest → **10 passed**; provision `--dry-run --limit 3` → ok; `--life-sim` dry-run → **3/3 secrets-1:1**; `git ls-files` secrets → **0**; invent `GET /dev/last-otp` → **absent** in provision code (disk outbox only).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T07 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L770 / L857–867. AC из backlog Target verbatim — **не** invent.

---

## 1. Итог: tooling/docs AC PASS; live signup PASS-via-blocker; Product Done = yes (with residual); 3 gaps; TASKED-likely = G2 (+ G1 ops/WAIVE)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Provision script signup | [`life_sim_provision_users.py`](../../tests/sandbox/life_sim_provision_users.py) + [`life_sim_provision_lib.py`](../../tests/sandbox/life_sim_provision_lib.py); `make life-sim-provision-users`; dry-run 3/3 | ✅ PASS *(live signup 429)* |
| **T02** | CSPRNG ≥24 + gitignored secrets | `generate_password` / `PASSWORD_MIN_LEN=24`; `.gitignore:17` `tests/sandbox/.secrets/`; tracked secrets **0** | ✅ PASS |
| **T03** | File OTP verify + pacing | `read_latest_otp_from_outbox` disk-only; `POST …/phone/request|confirm`; `--pace-s` default 65; **no** last-otp HTTP | ✅ PASS *(live OTP blocked upstream by signup)* |
| **T04** | Wire replay 1:1 Bearer | [`resolve_fixture_user_bearer_token`](../../tests/simulation_intake_http.py:145); runner secrets-1:1; pool deprecated + `LIFE_SIM_USE_POOL_M20=1` emergency | ✅ PASS *(dry-run)* |
| **T05** | Operator docs preconditions | note AC-05 (file SMS, outbox, Supabase, pacing, never commit) | ✅ PASS |
| **T06** | Offline unit tests | [`test_gw_req11_05_provision_fixture_users.py`](../../tests/test_gw_req11_05_provision_fixture_users.py) **10 passed** | ✅ PASS |
| **T07** | Gate AC-01…06 | Gate PASS* 18:15:05Z | ✅ PASS |

**Verdict product:** GW-REQ11-05 **исполнена по gate framing** (provision tooling + secrets hygiene + file-OTP path + 1:1 wire + docs + units). Live Supabase signup (even `--limit 1`) **not** proven — **operator blocker** `HTTP 429 over_email_send_rate_limit`. Identity file-OTP precondition documented OK at gate time.  
**Product Story Done (AC/DoD) = yes** — holds **with** documented blocker + tooling (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

**Confirm (operator ask):** invent OTP HTTP → **not present**; secrets committed → **no**.

---

## 2. AC overlay — Product Done vs live signup blocker

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Script creates/updates verified accounts (200 / `--limit`) | **PASS*** | Script+Make+`--limit`; dry-run ok. *Live `--limit 1` → 429 (run-summary-1815 / gate). Full N=200 live unproven. |
| AC-02 CSPRNG ≥24; gitignored secrets + generation_id | **PASS** | lib + gitignore + units; `git ls-files` `.secrets/**` = 0 |
| AC-03 password grant → Bearer → `/me` phone_verified | **PASS*** | Code path (signup→file OTP→grant→me) Present; *live blocked upstream by signup 429 |
| AC-04 replay own Bearer from secrets (not pool %20) | **PASS** | Runner Auth `secrets-1:1`; dry-run 3/3 this turn; pool schema_note DEPRECATED |
| AC-05 docs preconditions | **PASS** | note |
| AC-06 offline tests; live `--limit` smoke when env available | **PASS*** | 10 pytest; live smoke attempted → 429 documented |

### Does Product Done hold with documented blocker?

**Yes — under gate/story DoD as shipped:** AC closed via tooling + offline proof + documented Supabase email rate-limit blocker (gate PASS*). Unit **10**; dry-run provision + dry-run replay prove orchestration without inventing OTP HTTP or committing secrets.

**Caveat:** residual live Pass (signup + file OTP confirm + `/me` verified + live stash→submit with 1:1 Bearer, then scale to 200) still needs ops clear of email rate limit → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Users JSON 200 | `dogestonia_life_sim_users_v0_1.json` | ✅ |
| Provision + lib | `life_sim_provision_users.py`, `life_sim_provision_lib.py` | ✅ |
| Make target | `Makefile` `life-sim-provision-users` | ✅ |
| Secrets gitignore | `.gitignore:17` + nested `.secrets/.gitignore` | ✅ |
| Secrets tracked | `git ls-files` count **0** | ✅ |
| OTP = file outbox only | `read_latest_otp_from_outbox`; no `/dev/last-otp` invent | ✅ |
| 1:1 Bearer resolve | `resolve_fixture_user_bearer_token` | ✅ |
| Pool deprecated | `life_sim_pool_m20.json` schema_note; `LIFE_SIM_USE_POOL_M20` | ✅ |
| Branch | `dev` | ✅ |

---

## 3. Регрессии / gaps

### G1 — Live Supabase signup 429; verified provision + AC-03 live unproven · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Gate/run-summary: Identity health + `SMS_PROVIDER=file` + outbox Present; live signup `--limit 1` → **`over_email_send_rate_limit`**. Fail-closed / no invent secrets or OTP HTTP — correct. Until rate limit clears (or demo confirm-email off), AC-01/03 literal live verified accounts remain tooling-only.

**Как закрыть (P5 hint):** TASKED ops — wait/retry Supabase email quota or demo project settings; `make life-sim-provision-users LIMIT=2` then paced N=200; evidence `/me` phone_verified + optional live `--life-sim --max N`. Or WAIVE operator if tooling+blocker accepted as Done for this wave.

### G2 — Backlog §Verified current state still present-tense pre-P3 «Absent» · severity: **LOW** · **TASKED-likely**

[`STORY-GW-REQ11-05-…md` backlog](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md) §Verified still claims «No life-sim signup/provision script» and «Replay uses pool M=20» while Meta Status = Done and artifacts Present. Pipeline has As-of-Done **and** labeled Historical scaffold table (L70–79) — backlog SSOT not split.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog Verified (mirror pipeline / REQ11-0x pattern). Optional: label pipeline «Code touchpoints (implement wave)» as Historical (still says «named only»).

### G3 — Bullrun §«Актуальная точка» без REQ11-05 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L770 + tasks L861–867 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L770 GW-REQ11-05 | 🔵 Done · PASS* · file OTP + 1:1 · live 429 · pkg-000104 | Product Done (blocker) | PASS* + **G1** |
| T01 | L861 | ✅ provision signup | Done | PASS (dry-run) |
| T02 | L862 | ✅ CSPRNG + `.secrets/` | Done | PASS |
| T03 | L863 | ✅ file OTP; no invent last-otp | Done | PASS (code) |
| T04 | L864 | ✅ 1:1 Bearer; pool deprecated | Done | PASS (dry-run) |
| T05 | L865 | ✅ note preconditions | Done | PASS |
| T06 | L866 | ✅ offline tests | Done | PASS 10 |
| T07 | L867 | ✅ AC-01…06 PASS* | Gate PASS* | PASS |
| Journal | L2063 | P3 execute 1815 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live signup 429; verified provision/AC-03 unproven | **yes** (ops) or WAIVE operator | Identity/file OTP OK; no invent OTP HTTP |
| G2 | Low | backlog Verified «Absent» vs Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
