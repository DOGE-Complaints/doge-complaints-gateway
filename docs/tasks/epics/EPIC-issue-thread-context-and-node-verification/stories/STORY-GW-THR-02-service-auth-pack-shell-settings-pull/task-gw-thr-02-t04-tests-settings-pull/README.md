# task-gw-thr-02-t04-tests-settings-pull

## Task: tests — Settings pull pytest coverage (T04)

## Meta
- **Story:** [STORY-GW-THR-02](../STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000094
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-09-21T20:43:05Z
- **Completed:** 2026-09-21T20:48:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`

## Purpose
Pytest coverage for service-auth settings pull: allow/deny auth; incomplete pack → fail-closed; happy path returns capabilities; Issue get civic isolation + no Story bodies in settings.

## Code Facts
1. THR-01 pack shell tests exist (precedent for fail-closed caps) under `tests/` (pack shell required).
2. Service-auth write precedent at `asgi_app.py:559` — mirror allow/deny patterns from existing service-auth tests if present.
3. Issue get civic shape — `handlers.py:482-486`.

4. **As-of-Done (P3):** [`test_gw_thr_02_settings_pull.py`](../../../../../../tests/test_gw_thr_02_settings_pull.py).

## Gap
**Closed (P3 2026-09-21T20:48:13Z):** `tests/test_gw_thr_02_settings_pull.py` — 9 passed.


## Acceptance / DoD
- [x] Service-auth allow → capabilities returned (AC-GW-THR02-01)
- [x] Service-auth deny → rejected (AC-GW-THR02-02 class)
- [x] Incomplete pack → fail-closed (AC-GW-THR02-04)
- [x] Settings payload has no Story narrative bodies (AC-GW-THR02-03)
- [x] Public Issue get unchanged civic class (AC-GW-THR02-05)
- [x] Suite green for touched tests
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/` — new or extended pytest module(s) for settings pull
- Fixtures: complete vs incomplete shell_capabilities packs (THR-01 patterns)

## Out of scope
THR-03; REQ8; invent public ThreadContext route; invent path/JSON into REQ; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** public ThreadContext route.
  - Path/JSON field names **Open** — choose at P3; do not write into REQ.
  - No Story narrative bodies in settings (D19).
  - Fail-closed — no silent empty policy.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093; pointer is pkg-000094.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/ -k 'settings_pull or shell_settings or thr_02' --tb=short
```
