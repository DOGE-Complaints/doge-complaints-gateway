# task-gw-ssr-35-t05-tests-tmp-path-http-mock

## Task: tests — Tests tmp_path + HTTP mock (T05)

## Meta
- **Story:** [STORY-GW-SSR-35](../STORY-GW-SSR-35-schema-root-url-pack-refresh.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000092
- **Skill declared:** python-pro
- **Depends on:** soft SSR-34 Done; prior T* in pkg order
- **Scaffolded:** 2026-09-07T08:45:20Z
- **Completed:** 2026-09-07T08:54:22Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-35-schema-root-url-pack-refresh.md`

## Purpose
`tests/test_gw_ssr_35_*.py`: tmp_path cache + HTTP mock (httpx/respx/unittest); no live registry / network in CI. Cover miss→fetch, refresh overwrite, fail-fast, URL-unset path.

## Code Facts
1. Preferred `tests/test_gw_ssr_35_*.py`.
2. No depend on uus content bugs.
3. CI must not require network.

## Gap
**Closed (P3 2026-09-07T08:54:22Z):** implemented.

## Acceptance / DoD
- [x] pytest green with mocked HTTP only
- [x] tmp_path nested layout + resolve_pack SUCCESS fixture
- [x] fail-fast / refresh cases covered
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_35_*.py`

## Out of scope
Volume/gitignore/uus (SSR-34); invent registry; URL as mount; pack repair; §Актуальная точка rewrite.
- Overlay bans (every task):
  - `SCHEMA_ROOT_URL` = remote federation registry URL only — never Volume mount / disk path.
  - Persist target = `SCHEMA_PACKS_ROOT` or default local root — not URL.
  - **No** Volume/gitignore/uus-activate reopen (SSR-34 Done).
  - **No** invent registry product / live CI registry.
  - Fresh cache: no unnecessary re-fetch (or document policy in T03/T04).
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000061…091; pointer is pkg-000092.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_35_*.py
```
