# 15. Phased Implementation Plan (Demo -> Pilot)

## Phase 1 — Core foundation
- API layer + DI + orchestration skeleton.
- Story intake/store.
- Validation system baseline.
- Geo module rewrite (service + cache + provider adapter).

**Exit criteria:** story intake stable, tests green, security baseline enforced.

## Phase 2 — Intelligence and clustering
- Signal profile extraction.
- Dynamic cluster engine (micro/local/systemic).
- Explainability outputs.

**Exit criteria:** cluster views reproducible, reviewable, multi-membership works.

## Phase 3 — Distinct issue + SPA projection
- issue-candidate gates.
- projection engine with i18n/fallback.
- contract tests vs current SPA.

**Exit criteria:** zero-change SPA compatibility validated.

## Phase 4 — Evidence and pilot adapters
- evidence pack layer + lineage.
- wallet/sign/tx adapters as stubs in demo.
- feature flags for pilot switch-on.

**Exit criteria:** tokenization-ready architecture without enabling chain runtime.

## Phase 5 — Pilot activation
- enable prepare/sign/callback flow;
- подключить broadcaster adapter;
- end-to-end pilot qualification.

**Exit criteria:** controlled pilot with observable and reversible flow.
