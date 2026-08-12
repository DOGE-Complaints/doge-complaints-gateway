# Story acceptance gate — STORY-GW-GAUTH-01

- **Story:** Двухслойная аутентификация на мутациях публичного контента
- **Package:** `pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml`
- **Result:** PASS
- **Date:** 2026-06-25

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op). | PASS | T03 `build_service_auth_from_env` mandatory channel; T04 `test_intake_without_service_token_rejected_not_noop`, `test_intake_rejects_when_service_token_env_unset` |
| На verify-гейтед действии пользовательский токен обязателен (его отсутствие — отказ). | PASS | `require_user_token` + T04 `test_intake_service_only_without_user_token_rejected` |
| Наличие только сервисного токена **не** открывает создание истории за произвольного пользователя. | PASS | T04 `test_service_only_does_not_create_story_for_arbitrary_submitter` (401, no story) |
| Политика «оба слоя» применена ко **всем** write-путям публичного контента (D-GAUTH-2), не только к intake. | PASS | T01 inventory; T02 `_PUBLIC_CONTENT_WRITE_DEPS` on `/intake/stories` + `/tallinn/issues`; T04 tallinn test |
| Поведение зафиксировано как контракт (что отвергается и почему), согласовано с [`04-security §A`](../../../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md). | PASS | T04 `tests/test_gw_gauth_01_two_layer_auth_contract.py`; 401 `UNAUTHORIZED` envelope |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q -m 'not live_integration'
```

**Live run (2026-06-25):** gauth contract 6 passed; unit suite 534 passed, 12 skipped.

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
