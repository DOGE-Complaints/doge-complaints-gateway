# STORY-GW-SSR-35 — SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH (federation remote registry)

## Meta
- **Key:** `STORY-GW-SSR-35-schema-root-url-pack-refresh`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — operator-forced federation consume (sequence **35**)
- **Тип:** implement (config + boot fetch + refresh + tests + docs)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md)
- **Architecture:** D-SSR-12 · D-SSR-8 · D-SSR-4 · REQ4 §5.3
- **Parent REQ:** 51 · REQ4
- **decision_ref:** backlog SSR-35
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000092-20260907-gw-ssr-35-schema-root-url-pack-refresh.yaml`](../../../../gateway-active-packages/pkg-000092-20260907-gw-ssr-35-schema-root-url-pack-refresh.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** soft SSR-34 Done (`f51dcf8`); hard SSR-16; soft federation readiness (не invent registry)
- **Scaffolded:** 2026-09-07T08:45:20Z
- **G35:** PASS 2026-09-07T08:54:22Z · [`gate`](./task-gw-ssr-35-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-SSR-35.md) · [`run-summary`](../../../../run-reports/run-summary-20260907-0854-gw-ssr-35-p3.md)
- **P6 G1:** CLOSED 2026-09-07T08:58:54Z · `run_mode=gw_ssr_35_audit_followup` · [`run-summary-audit`](../../../../run-reports/run-summary-20260907-0858-gw-ssr-35-audit-p6.md)

## Nested tasks (pkg-000092)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-35-t01-config-schema-root-url-refresh`](./task-gw-ssr-35-t01-config-schema-root-url-refresh/README.md) | Done (Awaiting Commits) |
| T02 | [`task-gw-ssr-35-t02-fetch-manifest-into-cache`](./task-gw-ssr-35-t02-fetch-manifest-into-cache/README.md) | Done (Awaiting Commits) |
| T03 | [`task-gw-ssr-35-t03-boot-wire-before-resolve`](./task-gw-ssr-35-t03-boot-wire-before-resolve/README.md) | Done (Awaiting Commits) |
| T04 | [`task-gw-ssr-35-t04-refresh-overwrite-fail-fast`](./task-gw-ssr-35-t04-refresh-overwrite-fail-fast/README.md) | Done (Awaiting Commits) |
| T05 | [`task-gw-ssr-35-t05-tests-tmp-path-http-mock`](./task-gw-ssr-35-t05-tests-tmp-path-http-mock/README.md) | Done (Awaiting Commits) |
| T06 | [`task-gw-ssr-35-t06-docs-federation-vs-volume`](./task-gw-ssr-35-t06-docs-federation-vs-volume/README.md) | Done (Awaiting Commits) |
| T07 | [`task-gw-ssr-35-t07-story-acceptance-gate`](./task-gw-ssr-35-t07-story-acceptance-gate/README.md) | Done (Awaiting Commits) · G35 PASS |
| T08 | [`task-gw-ssr-35-t08-audit-g1-as-of-done-ssot`](./task-gw-ssr-35-t08-audit-g1-as-of-done-ssot/README.md) | Done (Awaiting Commits) · G1 CLOSED |

## Scope / Out of scope

**In:** Config `SCHEMA_ROOT_URL` + `SCHEMA_PACK_REFRESH`; boot fetch into packs root; refresh overwrite; fail-fast; tmp_path+HTTP mock tests; manuals federation vs SSR-34; G35.

**Out:** Volume UI / gitignore / uus activate (SSR-34); URL as mount path; pack repair; invent registry product; change `NODE_SCHEMA_*` semantics; §Актуальная точка rewrite.

## Target / AC

- [x] **AC-GW-SSR35-01:** URL + empty cache + `NODE_SCHEMA_*` → files under cache root → `resolve_pack` SUCCESS (fixture).
- [x] **AC-GW-SSR35-02:** Fresh cache → no unnecessary re-fetch (or documented policy).
- [x] **AC-GW-SSR35-03:** Refresh overwrite; corrupt remote → ConfigError-class; not tallinn default.
- [x] **AC-GW-SSR35-04:** pytest mocked HTTP; no network in CI.
- [x] **AC-GW-SSR35-05:** Manuals: URL = federation registry; Volume path = `SCHEMA_PACKS_ROOT` only.
