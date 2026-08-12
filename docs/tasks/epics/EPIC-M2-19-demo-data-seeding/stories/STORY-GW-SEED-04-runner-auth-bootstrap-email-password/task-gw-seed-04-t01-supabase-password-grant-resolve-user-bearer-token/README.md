# task-gw-seed-04-t01

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro
- **Depends on:** SEED-03 runner stash+submit (Done)

## Purpose
Backlog §B + T01: переписать `resolve_user_bearer_token()` — Supabase password grant (`POST {SUPABASE_URL}/auth/v1/token?grant_type=password`, header `apikey`, body `{email,password}`) → `access_token`; in-memory once per run; удалить чтение `GATEWAY_USER_TOKEN` / `SMOKE_USER_BEARER_TOKEN`.

## Code Facts
- Current token resolver — [`simulation_intake_http.py:17-28`](../../../../../../../tests/simulation_intake_http.py#L17)
- Runner entry — [`simulation_runner.py:149`](../../../../../../../tests/simulation_runner.py#L149) `resolve_user_bearer_token()`
- Env load order — [`simulation_runner.py:39-41`](../../../../../../../tests/simulation_runner.py#L39) `.env.test` then `.env`
- Identity accepts Supabase JWT — [`doge-identity-service/src/core/api/security.py:36-42`](../../../../../../../../../../doge-identity-service/src/core/api/security.py#L36)
- SPA parity — [`spa-app/src/pages/LoginPage.jsx:188`](../../../../../../../../../../spa-app/src/pages/LoginPage.jsx#L188) `signInWithPassword`
- Required env (backlog §A): `GATEWAY_USER_EMAIL`, `GATEWAY_USER_PASSWORD`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`

## Acceptance / DoD
- Traces parent AC#2: runner exchanges email+password → Supabase `access_token` on start
- Traces parent AC#4: token held in-memory only (no disk write, no log of token value)
- `GATEWAY_USER_TOKEN` / `SMOKE_USER_BEARER_TOKEN` no longer read in `resolve_user_bearer_token`
- Missing any of 4 env vars → `RuntimeError` naming the variable
- Supabase login failure → `RuntimeError` with rejected-login message (no silent fallback)

## Where to change
- [`tests/simulation_intake_http.py`](../../../../../../../tests/simulation_intake_http.py) — add `fetch_supabase_access_token(...)`; rewrite `resolve_user_bearer_token()`
- [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — optional module-level cache for token for duration of `main()`

## Out of scope
- Fail-closed submit HTTP messages (T02)
- Docs / `.env.test.example` (T03–T04)
- `src/core/` gateway API changes

## Verification commands
```bash
cd doge-complaints-gateway
python3 -c "from simulation_intake_http import resolve_user_bearer_token; print('import ok')"
# Unit tests added in T05
```
