# REQ9 ops parity & env naming (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`53-req9-ops-parity-env-naming.md`](../../../requirements/53-req9-ops-parity-env-naming.md)  
**Parent product:** [`REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md`](../../../../../docs/requirements%20backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md)  
**Tech-arch:** [`docs/architecture/req9-ops-naming/`](../../../../../docs/architecture/req9-ops-naming/00-overview.md)  
**Dashboard:** [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (operator lock: sync MVP board — ops package, not product feature)  
**Naming:** `STORY-GW-REQ9-*`  
**Updated:** 2026-09-26T12:31:20Z · REQ9-01/02 Done pkg-000096/097 (+ T04 audit G1 CLOSED)  
**Epic:** [`EPIC-req9-ops-parity-env-naming.md`](../../epics/EPIC-req9-ops-parity-env-naming.md)  
**Active pkg:** [`pkg-000097`](../../gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml)

---

## Контекст одной фразой

Gateway: `example.env` peer/own URL keys; hard-cut `SPA_VERIFY_*` → `SPA_BASE_URL` (env + Python field); `make test` offline + `make test-live`. Inbound `SERVICE_API_TOKEN` unchanged for aibridge pairing.

---

## Operator locks (clarifying 2026-09-25)

| Theme | Decision |
|-------|----------|
| SPA rename depth | **A** — env `SPA_BASE_URL` + Python `spa_base_url` / helpers; no dual-read |
| Dashboard | **B** — sync `gateway-mvp-dashboard.md` (no separate REQ9 scope dashboard) |
| Make test | **C** — `make test` = `-m "not live_integration"`; separate `make test-live` |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-REQ9-01 | [backlog](./STORY-GW-REQ9-01-example-env-and-spa-base-url.md) → [pipeline](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) · [pkg-000096](../../gateway-active-packages/pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml) | **Done** pkg-000096 T01–T06 · P3+P6 2026-09-26T12:12:27Z | — |
| STORY-GW-REQ9-02 | [backlog](./STORY-GW-REQ9-02-make-test.md) → [pipeline](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md) · [pkg-000097](../../gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml) | **Done** pkg-000097 T01–T04 · P3+P6 2026-09-26T12:31:20Z | — |

---

## Out of package

- Product APIs / clustering / waitlist invent  
- aibridge Makefile / spa `VITE_*`  
- Alias dual-read `SPA_VERIFY_*`  
- Railway service id (Open REQ §6)  
