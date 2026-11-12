# 59. REQ15 — Story draft stash parity verify (channel handoff)

Parent: [docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md](<../../../docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>) §1, §3 L4, AC-08; child sketch §8 gateway  
Parent-id: REQ15-interview-deepseek-telegram  
Siblings:
- [doge-ai-bridge REQ-11](../../../doge-ai-bridge/docs/requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) (client of stash; server owns submit)
- [spa 25](../../../spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md) (browser submit after `draft_id`)
- [GPT UI REQ-48](<../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md>) (instructions no longer model-call gateway)
Status: Draft — awaiting PA.2  
Дата: 2026-10-31

---

## Целевое состояние (простыми словами)

Gateway **уже** умеет принимать черновик (`POST /story-drafts`) и отдавать `draft_id` для продолжения в SPA.  
Под REQ15 мы **не изобретаем** новый stash API. Нужно **проверить**, что путь от aibridge (вместо Custom GPT Actions) по-прежнему совместим: тот же смысл stash ≠ публикация, Bearer service, успешный ответ достаточен для handoff. Ломающие изменения — только если T1 найдёт жёсткий разрыв (отдельное решение).

---

## 1) Goal

Verify Present story-draft stash contract remains the handoff SSOT for aibridge-owned submit; document parity vs historical Custom GPT Actions client; change gateway only if T1 proves a hard break.

## 2) Scope / Out of scope

**In scope**

- Re-verify `POST /story-drafts` (and related draft submit) against aibridge client expectations.  
- Confirm stash ≠ Story created; SPA still completes citizen submit.  
- Auth boundary: service Bearer for stash remains distinct from citizen session submit.  
- Evidence note / AC for REQ15 live path.  
- If T1 finds incompatibility: explicit gap list → optional follow-on REQ (do not silently invent fields here).

**Out of scope**

- Interview roles, providers, telegram transport.  
- Sense-brief / poster (57/58).  
- Redesigning intake wire “for fun”.  
- Hosting instruction files.

## 3) Verified current state

| Fact | Path / note |
|------|-------------|
| Stash create | handlers / draft flow — GW-DRAFT lineage; OpenAPI peer in GPT UI Actions YAML historically |
| aibridge client | `doge-ai-bridge` `gateway.py` `execute_stash` |
| Historical GPT Actions client | GPT UI `api-orchestrator.md` + Actions Bearer |

**T1:** confirm current handler paths/line numbers in implement wave — do not treat this Draft as code audit Done.

## 4) Target behavior

1. aibridge stash succeeds under same product rules as Actions-era citizen path.  
2. `draft_id` usable by SPA `#/story/submit`.  
3. No requirement that GPT/model call gateway.

## 5) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **AC-GW-59-01** | Documented verify: stash 201 + `draft_id` works for aibridge client |
| **AC-GW-59-02** | Stash success still ≠ published Story |
| **AC-GW-59-03** | If break found: written gap + decision — no silent contract drift |
| **AC-GW-59-04** | Service vs citizen auth boundaries unchanged unless explicit REQ |

## 6) Open

- Any additive headers/fields only after T1 + operator lock.
