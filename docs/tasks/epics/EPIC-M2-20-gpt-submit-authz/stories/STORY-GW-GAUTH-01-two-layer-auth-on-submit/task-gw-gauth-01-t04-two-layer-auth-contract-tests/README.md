# task-gw-gauth-01-t04

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000039
- **Skill declared:** python-pro
- **Depends on:** T02, T03

## Purpose
Тесты контракта двухслойной auth: вызов без сервисного токена → отказ; с валидным сервисным, но без пользовательского → отказ на verify-гейтед действии (**stub/hook под GAUTH-02**); только сервисный токен не создаёт историю за произвольного пользователя.

## Code Facts
- Intake endpoint — [`asgi_app.py:396`](../../../../../../../src/core/api/asgi_app.py#L396)
- Unauthorized handler — [`asgi_app.py:240-242`](../../../../../../../src/core/api/asgi_app.py#L240-L242)
- Existing security tests — [`tests/test_api_security_and_ops.py`](../../../../../../../tests/test_api_security_and_ops.py)
- Intake contract tests — [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py)
- req-19 trust levels — [`requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`](../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) §5

## Acceptance / DoD
- Traces parent AC: Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op)
- Traces parent AC: На verify-гейтед действии пользовательский токен обязателен (его отсутствие — отказ) — via stub `require_user_auth`
- Traces parent AC: Наличие только сервисного токена **не** открывает создание истории за произвольного пользователя
- Traces parent AC: Поведение зафиксировано как контракт (что отвергается и почему)
- New tests: `tests/test_gw_gauth_01_*.py` green
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_gauth_01_two_layer_auth_contract.py` (or split modules)
- Optional stub: `require_user_auth` FastAPI dependency in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) (fail-closed until GAUTH-02)
- Document rejection contract in test docstrings or task acceptance file

## Out of scope
- Real identity HTTP introspection (GW-GAUTH-02)
- `verification_required` 403 body (GW-GAUTH-03)
- Overwriting submitter from introspected `sub` (GW-GAUTH-04)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py
```
