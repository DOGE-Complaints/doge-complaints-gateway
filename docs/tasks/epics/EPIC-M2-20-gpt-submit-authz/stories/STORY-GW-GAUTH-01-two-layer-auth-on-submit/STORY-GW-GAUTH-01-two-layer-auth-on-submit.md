# STORY-GW-GAUTH-01 — Двухслойная аутентификация на мутациях публичного контента

## Meta
- **Key:** `STORY-GW-GAUTH-01`
- **Parent Epic:** [`../../../EPIC-M2-20-gpt-submit-authz.md`](../../../EPIC-M2-20-gpt-submit-authz.md)
- **Type:** implement (gateway auth-слой)
- **Status:** ⚪ Todo
- **Приоритет:** P1
- **source:** [`../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md`](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Закрывает:** разрыв «intake открыт без auth» на пути подачи истории из GPT
- **Источник процесса:** [`04-security §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) — принцип «два независимых вопроса», шаг 7.
- **Decision Ref:** backlog file above; [`interview-gpt-submit-authz-2026-06-24`](../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-2); [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml`](../../../../gateway-active-packages/pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05
- **Зависит от:** —
- **Разблокирует:** [GW-GAUTH-02](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)

## Зачем простыми словами
Когда GPT шлёт историю в gateway, на запросе **два токена**: сервисный (доказывает, что зовёт доверенный канал GPT-Action) и пользовательский (говорит, кто человек). Это **два разных вопроса** — отвечать надо на оба. Сервисный токен сам по себе не доказывает, какой пользователь стоит за запросом: если поверить только ему, любой сможет подать историю за кого угодно («confused deputy» — подмена субъекта на доверенном канале).

## Что наблюдаю сейчас (verified по коду)
- **`POST /intake/stories` открыт** — нет auth-зависимости ([`asgi_app.py:396`](../../../../../../src/core/api/asgi_app.py#L396)). Для сравнения, `POST /tallinn/issues` уже под сервисным гейтом: `dependencies=[Depends(require_service_auth)]` ([`asgi_app.py:380`](../../../../../../src/core/api/asgi_app.py#L380)).
- **Сервисный слой существует, но опционален:** `ServiceTokenAuth.require()` — no-op без `SERVICE_API_TOKEN` ([`security.py:54-62`](../../../../../../src/core/api/security.py#L54)); `require_service_auth` бросает `UnauthorizedError` при включённом токене ([`asgi_app.py:252`](../../../../../../src/core/api/asgi_app.py#L252)). Токен читается из `Authorization: Bearer` / `X-Service-Token` ([`security.py:16-27`](../../../../../../src/core/api/security.py#L16)).
- **Пользовательского слоя нет** — gateway не извлекает и не проверяет пользовательский токен на intake.
- **Контракт уровней доверия уже зафиксирован** в [`req-19 §5.1`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md): `Authorization` = доверие к каналу; `submitter` = автор. Эта стори добавляет: **на verify-гейтед мутациях применяются оба слоя**.

## Требование / целевое состояние
- На **всех мутациях публичного контента** (intake-подача + любые будущие write-пути, влияющие на публичную доску — **D-GAUTH-2**) **обязателен сервисный слой доверия** (сервисный токен или mTLS) — отсекает не-доверенные вызовы.
- На том же пути для verify-гейтед действия **обязателен пользовательский токен** (его проверка — [GW-GAUTH-02](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)).
- **Сервисного токена недостаточно** для решения «за какого пользователя создаём историю»: нужен пользовательский слой.
- Сервисный слой на этих путях — **обязателен** (не опционально-disabled, как сейчас в demo-конфиге).

## Out of scope
- Проверка пользователя и статус верификации (introspection, `phone_verified`) — [GW-GAUTH-02](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)/[03](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md)
- Авторитетный `sub` из introspection — [GW-GAUTH-04](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- Дублирование identity OAuth / изменение `req-19` submitter-контракта

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-gauth-01-t01-inventory-public-content-write-paths`](./task-gw-gauth-01-t01-inventory-public-content-write-paths/README.md) | pkg-000039 |
| 2 | [`task-gw-gauth-01-t02-attach-service-gate-to-uncovered-writes`](./task-gw-gauth-01-t02-attach-service-gate-to-uncovered-writes/README.md) | pkg-000039 |
| 3 | [`task-gw-gauth-01-t03-mandatory-service-auth-policy-config`](./task-gw-gauth-01-t03-mandatory-service-auth-policy-config/README.md) | pkg-000039 |
| 4 | [`task-gw-gauth-01-t04-two-layer-auth-contract-tests`](./task-gw-gauth-01-t04-two-layer-auth-contract-tests/README.md) | pkg-000039 |
| 5 | [`task-gw-gauth-01-t05-story-acceptance-gate`](./task-gw-gauth-01-t05-story-acceptance-gate/README.md) | pkg-000039 |

## Acceptance Criteria
- [ ] Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op).
- [ ] На verify-гейтед действии пользовательский токен обязателен (его отсутствие — отказ).
- [ ] Наличие только сервисного токена **не** открывает создание истории за произвольного пользователя.
- [ ] Политика «оба слоя» применена ко **всем** write-путям публичного контента (D-GAUTH-2), не только к intake.
- [ ] Поведение зафиксировано как контракт (что отвергается и почему), согласовано с [`04-security §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md).

## Открытые вопросы
- ~~Только `/intake/stories` или все мутации?~~ → **решено D-GAUTH-2: все мутации публичного контента.**
- Сервисное доверие к demo-профилю: где «обязательность» включается жёстко, а где допустим demo-bypass (согласовать с deployment-профилями `config/schema.py`) — закрывается в T03.
