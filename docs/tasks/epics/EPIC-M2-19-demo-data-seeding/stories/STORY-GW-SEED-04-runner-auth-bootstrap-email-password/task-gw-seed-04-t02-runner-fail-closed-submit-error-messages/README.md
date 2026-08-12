# task-gw-seed-04-t02

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog §B fail-closed + T02: явные сообщения об ошибках — missing env / bad Supabase creds (T01); submit `403` (`VERIFICATION_REQUIRED`); submit `401`. Не silent, без авто-провижна (D-SEED04-1).

## Code Facts
- Stash+submit HTTP — [`simulation_intake_http.py:96-127`](../../../../../../../tests/simulation_intake_http.py#L96)
- Runner failure loop — [`simulation_runner.py:186-208`](../../../../../../../tests/simulation_runner.py#L186)
- Submit gate — identity `/me` → `phone_verified` (403 if not verified) — backlog verified fact
- Backlog messages (verbatim intent):
  - 403 → «демо-пользователь не phone_verified — верифицируй телефон один раз в SPA, затем повтори»
  - 401 → «Supabase-токен невалиден/просрочен»

## Acceptance / DoD
- Traces parent AC#3: unverified user / bad creds / missing env → explicit error, fail-closed
- Submit 403 surfaces verification message (not generic HTTP dump only)
- Submit 401 surfaces token-invalid message
- Runner exit code 1 on failure; no partial success count for failed submit

## Where to change
- [`tests/simulation_intake_http.py`](../../../../../../../tests/simulation_intake_http.py) — map status codes to `RuntimeError` or structured error text
- [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — print/raise user-facing error in main loop

## Out of scope
- Auto phone verification / mock SMS
- Identity OAuth server changes
- Gateway handler changes

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest tests/test_gw_seed_04_runner_auth_bootstrap.py -q -k fail_closed
```
