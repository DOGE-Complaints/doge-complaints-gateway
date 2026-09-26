# Hard Audit — STORY-GW-REQ9-01 example.env + SPA_BASE_URL hard cut (2026-09-26)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ9-01-example-env-and-spa-base-url`](../tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) (T01–T05, **pkg-000096**).  
**Pipeline:** [`…/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/STORY-GW-REQ9-01-example-env-and-spa-base-url.md).  
**Pkg:** [`pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml`](../tasks/gateway-active-packages/pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ9-01.md`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/task-gw-req9-01-t05-story-gate/story-acceptance-gate-STORY-GW-REQ9-01.md) PASS **2026-09-26T12:06:30Z**.  
**Run-summary:** [`run-summary-20260926-1206-gw-req9-01-p3.md`](../tasks/run-reports/run-summary-20260926-1206-gw-req9-01-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-09-26T12:09:15Z`. Live: pytest gauth_03 + draft_02 → **10 passed**; `rg SPA_VERIFY|spa_verify` under `src/` / `tests/` / `docs/runtime-docs/` → **0**; `example.env` has `API_BASE_URL` / `IDENTITY_BASE_URL` (+ `:8100`) / `SPA_BASE_URL` / `SERVICE_API_TOKEN`.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints T01–T05 / story rows актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L669 / L676–680. AC из pipeline Target verbatim — **не** invent.

---

## 1. Итог: product AC-01…05 / T01–T05 закрыты; 2 OPEN gaps (0 Critical/High/Medium); TASKED-likely = G1

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | `example.env` peer/own URL keys + keep token | [`example.env:104–124`](../../example.env) `API_BASE_URL` / `IDENTITY_BASE_URL` + `:8100` / `SPA_BASE_URL` / `SERVICE_API_TOKEN` | ✅ PASS |
| **T02** | Schema hard cut `SPA_BASE_URL` / `spa_base_url` | [`schema.py:53`](../../src/core/config/schema.py), load [`:583–589`](../../src/core/config/schema.py), ctor [`:649`](../../src/core/config/schema.py); no `SPA_VERIFY` in `schema.py` | ✅ PASS |
| **T03** | Helpers rename | [`verify_url.py`](../../src/core/identity/verify_url.py) `resolve_spa_base_url` / `DEFAULT_SPA_BASE_URL`; [`identity/__init__.py`](../../src/core/identity/__init__.py) exports | ✅ PASS |
| **T04** | Tests/docs primary `SPA_BASE_URL` | Contracts set `SPA_BASE_URL`; [`server-env-quickstart.md:158`](../../docs/runtime-docs/manuals/server-env-quickstart.md); live **10 passed** | ✅ PASS |
| **T05** | Gate AC-01…05 | Gate PASS 12:06:30Z | ✅ PASS |

**Verdict product:** GW-REQ9-01 **исполнена по AC** (hard cut; no dual-read).  
**Product Story Done (AC/DoD) = yes. Empty OPEN gap-list = no** (G1 TASKED-likely; G2 WAIVED-likely).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts (findings, not fix)

| AC (pipeline Target) | Result | Evidence |
|----------------------|--------|----------|
| AC-01 `IDENTITY_BASE_URL` + `:8100` comment | **PASS** | `example.env:106–108` |
| AC-02 `API_BASE_URL` in `example.env` | **PASS** | `example.env:104` |
| AC-03 `SPA_BASE_URL` / `spa_base_url`; no primary `SPA_VERIFY_*` | **PASS** | schema + verify_url; `rg` src/tests/runtime-docs = 0 |
| AC-04 `SPA_BASE_URL` documented; `SERVICE_API_TOKEN` retained | **PASS** | `example.env:112` / `:124` |
| AC-05 tests/docs not primary `SPA_VERIFY_BASE_URL` | **PASS** | monkeypatch `SPA_BASE_URL`; manual table `SPA_BASE_URL` |
| Out: make test (REQ9-02); dual-read; invent Railway service ids | **PASS** | run-summary; fence |

---

## 3. Регрессии / gaps

### G1 — Persistent SSOT present-tense vs live post-P3 · severity: **LOW** · **TASKED-likely**

Product shipped; backlog/pipeline §Verified + T01–T03 Code Facts/Gap всё ещё утверждают pre-P3 «lacks keys / SPA_VERIFY / spa_verify_*».

| Artifact | Stale claim | Live fact |
|----------|-------------|-----------|
| Backlog §Verified [`:38–44`](../tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) | `SPA_VERIFY_BASE_URL` / `spa_verify_base_url`; «lacks IDENTITY/SPA/API keys»; tests set `SPA_VERIFY_*` | Hard cut + keys present; tests set `SPA_BASE_URL` |
| Pipeline §Verified [`:49–56`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) | same present-tense pre-P3 table | Same live facts |
| T01 Code Facts / Gap [`:19–25`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/task-gw-req9-01-t01-example-env-keys/README.md) | «No IDENTITY/SPA keys»; Gap «Template missing» | Keys landed; DoD `[x]` |
| T02 Code Facts / Gap | field/load still `SPA_VERIFY_*` | `spa_base_url` / `SPA_BASE_URL` only |
| T03 Gap | «Helper names still `spa_verify_*`» | `resolve_spa_base_url` shipped |

**Как закрыть (P5 hint):** TASKED — As-of-Done vs Historical на backlog + pipeline §Verified и T01–T03 Code Facts/Gap. Docs-only; **не** reopen product unless drift.

### G2 — Bullrun §«Актуальная точка» без REQ9-01 · severity: **LOW** · **WAIVED-likely reason=operator**

Fence / overlay: не rewrite §«Актуальная точка». Файл всё ещё стартует с EPIC-M2-24 / ES-03 — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). REQ9-01 story row L669 + T01–T05 L676–680 уже 🔵 Done + gate PASS.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L669 GW-REQ9-01 | 🔵 Done pkg-000096 T01–T05 P3 12:06:30Z · hard cut | Product Done | PASS |
| T01 | L676 | 🔵 API/IDENTITY/SPA_BASE_URL; keep token | Done | PASS |
| T02 | L677 | 🔵 spa_base_url; no SPA_VERIFY dual-read | Done | PASS |
| T03 | L678 | 🔵 resolve_spa_base_url | Done | PASS |
| T04 | L679 | 🔵 no primary SPA_VERIFY_* | Done | PASS |
| T05 | L680 | 🔵 AC-01…05 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1877 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | persistent SSOT present-tense (backlog/pipeline §Verified + T01–T03 Code Facts/Gap) | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** 1 (G1).  
**WAVE:** n/a (P4).

Handoff: P5 disposition (G1 TASKED-likely; G2 WAIVED-likely). Не закрывать gaps здесь.
