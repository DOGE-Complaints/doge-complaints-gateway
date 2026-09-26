# STORY-GW-REQ9-01 — example.env peer URLs + SPA_BASE_URL hard cut

## Meta
- **Key:** `STORY-GW-REQ9-01-example-env-and-spa-base-url`
- **Parent Epic:** [`../../../EPIC-req9-ops-parity-env-naming.md`](../../../EPIC-req9-ops-parity-env-naming.md)
- **Пакет:** [`req9-ops-parity-env-naming/`](../../../../backlog-stories/req9-ops-parity-env-naming/INDEX.md)
- **Status:** 🔵 Done
- **Тип:** env template / config rename (hard cut) / docs+tests align
- **source:** [`../../../../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`](../../../../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Parent REQ:** 53 · REQ9 §3, §5–§8.1, §10 (G4, R5, R10–R11)
- **Tech-arch:** [`../../../../../docs/architecture/req9-ops-naming/02-env-auth-url-naming.md`](../../../../../docs/architecture/req9-ops-naming/02-env-auth-url-naming.md) R5, R10–R11; hard cut [`00-overview.md`](../../../../../docs/architecture/req9-ops-naming/00-overview.md)
- **decision_ref:** backlog REQ9-01 · REQ53 · tech-arch `02-env-auth-url-naming.md` / `00-overview.md`
- **Skill declared:** python-pro · soft code-documenter
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml`](../../../../gateway-active-packages/pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml)
- **Git:** `semantic-schema-runtime`
- **Operator lock:** full hard cut — env `SPA_BASE_URL` **and** Python `spa_base_url` / helpers; **no** dual-read of `SPA_VERIFY_*`
- **Siblings:** aibridge REQ-08; spa 18; identity 22 — not this wave DoD
- **Parallel:** STORY-GW-REQ9-02 (make test) — out of this pkg
- **Scaffolded:** 2026-09-26T12:02:43Z

## Nested tasks (pkg-000096)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req9-01-t01-example-env-keys`](./task-gw-req9-01-t01-example-env-keys/README.md) | Done |
| T02 | [`task-gw-req9-01-t02-schema-spa-base-hard-cut`](./task-gw-req9-01-t02-schema-spa-base-hard-cut/README.md) | Done |
| T03 | [`task-gw-req9-01-t03-verify-url-helpers`](./task-gw-req9-01-t03-verify-url-helpers/README.md) | Done |
| T04 | [`task-gw-req9-01-t04-tests-docs-align`](./task-gw-req9-01-t04-tests-docs-align/README.md) | Done |
| T05 | [`task-gw-req9-01-t05-story-gate`](./task-gw-req9-01-t05-story-gate/README.md) | Done |
| T06 | [`task-gw-req9-01-t06-audit-g1-as-of-done-ssot`](./task-gw-req9-01-t06-audit-g1-as-of-done-ssot/README.md) | Done (audit follow-up) |

## Scope

1. Document in `example.env`: `API_BASE_URL`, `IDENTITY_BASE_URL` (comment: local identity `:8100`), `SPA_BASE_URL`; keep inbound `SERVICE_API_TOKEN`.
2. Hard-cut runtime/config: env name and AppConfig field/`verify_url` helpers from `SPA_VERIFY_*` / `spa_verify_*` → `SPA_BASE_URL` / `spa_base_url` (and rename helper symbols accordingly). **No** alias dual-read.
3. Update gateway tests/docs that still use `SPA_VERIFY_BASE_URL` / `spa_verify_base_url` as primary.
4. Same implement wave: rename local/Railway env var for SPA base (service id still Open — operator/ops); do not invent waitlist/nginx.

## Out of scope

- `make test` / `make test-live` (→ STORY-GW-REQ9-02).
- Product APIs, clustering, invent backends.
- aibridge Makefile / spa `VITE_*` renames.
- Dual-read `SPA_VERIFY_*`.

## Verified current state

### As-of-Done (post-P3 · pkg-000096 · gate 2026-09-26T12:06:30Z)

| Fact | Path |
|------|------|
| `IDENTITY_BASE_URL` EnvSpec + load | `src/core/config/schema.py:129`, load `:574-580` |
| `SPA_BASE_URL` load + field `spa_base_url` | `schema.py:53`, `:583-589`, ctor `:649` |
| Helpers `resolve_spa_base_url` / `DEFAULT_SPA_BASE_URL` | `src/core/identity/verify_url.py:7-19`; export `identity/__init__.py` |
| `example.env` peer/own URL keys + token | `API_BASE_URL=` `:104`; `IDENTITY_BASE_URL` + `:8100` comment `:107-108`; `SPA_BASE_URL=` `:112`; `SERVICE_API_TOKEN=` `:124` |
| Tests set `SPA_BASE_URL` | e.g. `tests/test_gw_gauth_03_verification_gate_contract.py:21`; `tests/test_gw_draft_02_story_draft_submit_contract.py` |
| Manual primary name `SPA_BASE_URL` | `docs/runtime-docs/manuals/server-env-quickstart.md:158` |

### Historical (pre-P3)

| Fact | Path (was) |
|------|------------|
| Primary env/field `SPA_VERIFY_BASE_URL` / `spa_verify_base_url` | schema load + field (pre hard cut) |
| `example.env` lacked `IDENTITY_BASE_URL` / `SPA_BASE_URL` / `API_BASE_URL=` keys | smoke comment only for API |
| Tests/manuals treated `SPA_VERIFY_BASE_URL` as primary | draft_02 / gauth_03 / server-env-quickstart |

## Target / AC

- [x] **AC-GW-REQ901-01:** `example.env` contains `IDENTITY_BASE_URL` + local `:8100` comment (G4/R11).
- [x] **AC-GW-REQ901-02:** `example.env` contains `API_BASE_URL` (R10).
- [x] **AC-GW-REQ901-03:** Configured name is `SPA_BASE_URL`; schema/load/field/helpers use `spa_base_url` — no primary `SPA_VERIFY_*` / `spa_verify_*` (R5 hard cut).
- [x] **AC-GW-REQ901-04:** `example.env` documents `SPA_BASE_URL`; inbound `SERVICE_API_TOKEN` retained for sibling aibridge value pairing.
- [x] **AC-GW-REQ901-05:** Gateway tests/docs in this repo do not treat `SPA_VERIFY_BASE_URL` as the primary config name.

## Техническое решение (projected)

- Rename env + `AppConfig.spa_base_url` + `resolve_spa_base_url` / `build_verify_url` call sites; grep-clean `SPA_VERIFY` / `spa_verify` in gateway tree (except historical run-reports if left untouched).
- Fail-closed behavior for missing optional SPA base unchanged in spirit (default localhost verify URL in `verify_url.py` — confirm at P3 whether default stays).

## Code touchpoints

- `example.env`
- `src/core/config/schema.py`
- `src/core/identity/verify_url.py`, `identity/__init__.py`
- Tests/docs (primary name now `SPA_BASE_URL` / `spa_base_url`)
- Optional: `.env.test.example`, `server-env-quickstart.md`, MVP §Deploy env list

## Dependencies

- Sibling child REQs may rename their own vars in parallel; this story owns gateway only.
- Railway SPA base var rename at implement (service id Open).

## Overlay bans

- Hard cut `SPA_BASE_URL` / `spa_base_url` — **NO** dual-read `SPA_VERIFY_*` / `spa_verify_*`.
- Do not invent Railway service ids / waitlist / nginx.
- Stay `semantic-schema-runtime`.
- Do not rewrite bullrun §«Актуальная точка».
- Do not mutate pkg-000095; pointer is pkg-000096.
- REQ9-02 make test not in this story/pkg.
