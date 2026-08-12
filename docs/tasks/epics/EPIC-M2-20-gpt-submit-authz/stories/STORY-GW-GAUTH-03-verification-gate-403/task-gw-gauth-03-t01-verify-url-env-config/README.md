# task-gw-gauth-03-t01

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** GW-GAUTH-02 (Done)

## Purpose
Добавить конфигурацию gateway для `verify_url` в ответе `verification_required` (источник — env; backlog T02 «источник verify_url — конфиг/identity»). Helper строит URL по образцу identity [`build_spa_verify_url`](../../../../../../../../../doge-identity-service/src/core/oauth/spa_login.py).

## Code Facts
- Нет `VERIFY` env в [`schema.py`](../../../../../../../src/core/config/schema.py) (grep — 0 matches)
- Канон OAUTH-04 полей — [`verification_required.py:18-23`](../../../../../../../../../doge-identity-service/src/core/oauth/verification_required.py)
- Identity pattern — [`spa_login.py:25-30`](../../../../../../../../../doge-identity-service/src/core/oauth/spa_login.py)

## Acceptance / DoD
- Traces parent AC #2: `verify_url` loadable from gateway config
- EnvSpec + `AppConfig` field for SPA/verify base URL (e.g. `SPA_VERIFY_BASE_URL` or equivalent)
- Helper `build_verify_url(return_context?)` returns OAUTH-04-shaped URL
- Wired into `ApiDependencies` / config for T03
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- New module e.g. [`src/core/identity/verify_url.py`](../../../../../../../src/core/identity/verify_url.py) or [`src/core/api/verification_required.py`](../../../../../../../src/core/api/verification_required.py)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — expose if needed

## Out of scope
- OAuth relay / authorize complete path (identity OAUTH-04)
- SPA verify UI

## Verification commands
```bash
cd doge-complaints-gateway && rg 'VERIFY|verify_url' src/core/config/schema.py src/core/
```
