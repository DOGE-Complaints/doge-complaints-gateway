# EPIC-req9-ops-parity-env-naming: REQ9 ops parity & env naming (gateway)

## Epic Meta
- Status: 🔵 Done (REQ9-01 Done pkg-000096; REQ9-02 Done pkg-000097)
- Priority: High (REQ9 / REQ53)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`req9-ops-parity-env-naming/`](../backlog-stories/req9-ops-parity-env-naming/INDEX.md)
- **Parent REQ:** [`53-req9-ops-parity-env-naming.md`](../requirements/53-req9-ops-parity-env-naming.md)
- **Parent product:** REQ9 §3, §5–§8.1, §10
- **Tech-arch:** [`docs/architecture/req9-ops-naming/00-overview.md`](../../../docs/architecture/req9-ops-naming/00-overview.md)
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — ops package (operator lock B)
- **Git:** `semantic-schema-runtime` (no separate package branch)
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Updated:** 2026-09-26T12:22:28Z (REQ9-02 P3 Done pkg-000097)

## Problem Statement

Gateway `example.env` peer/own URL keys; hard-cut `SPA_VERIFY_*` → `SPA_BASE_URL` (env + Python field/helpers); later story delivers `make test` offline + `make test-live`. Inbound `SERVICE_API_TOKEN` unchanged for aibridge pairing. No invent Railway service ids / waitlist / nginx.

## Soft (backlog)

- Soft (backlog): REQ9-01 example.env + SPA_BASE_URL hard cut — **Done** pkg-000096 T01–T05 (P3 2026-09-26T12:06:30Z)
- Soft (backlog): REQ9-02 make test + test-live — **Done** pkg-000097 T01–T03 (P3 2026-09-26T12:22:28Z)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ9-01 | [pipeline](./EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) → [backlog](../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md) · [pkg-000096](../gateway-active-packages/pkg-000096-20260926-gw-req9-01-example-env-and-spa-base-url.yaml) | 🔵 Done pkg-000096 T01–T05 |
| STORY-GW-REQ9-02 | [pipeline](./EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md) → [backlog](../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md) · [pkg-000097](../gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml) | 🔵 Done pkg-000097 T01–T03 |

## Decision Ref
- Backlog INDEX + `$storyFile` REQ9-01 / REQ9-02
- REQ 53 · REQ9 · tech-arch `02-env-auth-url-naming.md` · `01-runtime-and-probes.md` · `00-overview.md`
- Operator locks: SPA hard cut A; MVP dashboard B; make test C (REQ9-02)
