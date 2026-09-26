# 53. REQ9 — gateway ops parity & env naming

Parent: docs/requirements backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md §3, §5–§8.1, §10 (G4, G7, R5, R10–R11)  
Parent-id: dogestonia-microservices-ops-parity-target  
Siblings:  
- doge-ai-bridge/docs/requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md (contract: inbound `SERVICE_API_TOKEN` value = aibridge `GATEWAY_SERVICE_API_TOKEN`; `SPA_BASE_URL` public base)  
- doge-threads/docs/requirements/02-req9-ops-peer-token-docs.md (contract: threads outbound `SERVICE_API_TOKEN` = this process `SERVICE_API_TOKEN`)  
- doge-identity-service/docs/requirements/22-req9-make-env-load-parity.md (contract: `IDENTITY_BASE_URL` peer for `/me` forward — no new `/me` fields)  
- spa-app/docs/requirements/18-req9-vite-identity-base-url.md (contract: `SPA_BASE_URL` value aligns with public spa origin)  
Status: Draft — awaiting PA.2  
Tech-arch: docs/architecture/req9-ops-naming/  
Дата: 2026-09-25  

---

## 1) Goal

Bring gateway env template and Make parity in line with REQ9: document peer/own URL keys; rename SPA verify base to `SPA_BASE_URL` (hard cut); add `make test`.

## 2) Scope / Out of scope

**In:** `example.env` keys `API_BASE_URL`, `IDENTITY_BASE_URL`, `SPA_BASE_URL`; schema/load rename `SPA_VERIFY_BASE_URL`→`SPA_BASE_URL`; Makefile `test` target; keep `SERVICE_API_TOKEN` inbound; probes already `/health` `/ready`.

**Out:** product APIs; clustering; invent waitlist; aibridge Makefile; spa `VITE_*` renames; alias dual-read of old SPA verify name (hard cut per tech-arch).

## 3) Verified current state

- `IDENTITY_BASE_URL` in schema, absent from `example.env` — REQ9 G4  
- `SERVICE_API_TOKEN` in `example.env` — majority  
- Makefile `.PHONY: serve dev simulate check-env` — no `test` (G7)  
- `SPA_VERIFY_BASE_URL` loaded in schema (R5 as-is name)

## 4) Target behavior

- `example.env` documents `API_BASE_URL`, `IDENTITY_BASE_URL` (local identity `:8100` comment), `SPA_BASE_URL`  
- Runtime/config uses `SPA_BASE_URL` (hard cut from `SPA_VERIFY_*`)  
- `make test` runs project pytest like identity/threads  
- Inbound S2S unchanged: Bearer / `X-Service-Token` vs `SERVICE_API_TOKEN`

## 5) Acceptance criteria

- [ ] G4/R11: `example.env` contains `IDENTITY_BASE_URL` + comment  
- [ ] R10: `example.env` contains `API_BASE_URL`  
- [ ] R5: `SPA_BASE_URL` is the configured name (no primary `SPA_VERIFY_BASE_URL`)  
- [ ] G7: `make test` exists and runs  
- [ ] Sibling aibridge can pair `GATEWAY_SERVICE_API_TOKEN` to this `SERVICE_API_TOKEN`

## 6) Open questions

- Railway gateway service id for var sync — Unknown until implement

## 7) Dependencies

Parent §3, §8.1, §10; tech-arch 01–03; siblings REQ-08, threads `02-…`.
