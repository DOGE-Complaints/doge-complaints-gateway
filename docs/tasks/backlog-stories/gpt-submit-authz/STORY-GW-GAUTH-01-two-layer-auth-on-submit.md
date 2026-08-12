# STORY-GW-GAUTH-01 — Двухслойная аутентификация на мутациях публичного контента

> **⚠️ Superseded (user submit):** для подачи истории пользователем актуален browser-submit — [`story-draft-handoff/`](../story-draft-handoff/INDEX.md). Эта стори остаётся для legacy `POST /intake/stories` (удаление кода → GW-DRAFT-04). См. [`gpt-submit-authz/INDEX.md`](./INDEX.md).

## Meta
- **Key:** `STORY-GW-GAUTH-01`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000039](../../gateway-active-packages/pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml), T01–T05, gate PASS 2026-06-25): `_PUBLIC_CONTENT_WRITE_DEPS` (mandatory сервисный + `require_user_token`) на `/intake/stories`+`/tallinn/issues`; 6 contract + full 533 passed. Код-аудит [`audit-gw-gauth-01-...`](../../../analysis/audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md). **G1:** user-слой = заглушка присутствия `X-User-Token`; реальный introspection/`phone_verified` → GAUTH-02/03. SSOT исполнения — pipeline-копия.
- **Приоритет:** P1
- **Тип:** implement (gateway auth-слой)
- **Закрывает:** разрыв «intake открыт без auth» на пути подачи истории из GPT
- **Источник процесса:** [`04-security §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) — принцип «два независимых вопроса», шаг 7.
- **Основание:** [`interview-gpt-submit-authz-2026-06-24`](./interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-2)
- **Зависит от:** —
- **Разблокирует:** [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)

## Зачем простыми словами
Когда GPT шлёт историю в gateway, на запросе **два токена**: сервисный (доказывает, что зовёт доверенный канал GPT-Action) и пользовательский (говорит, кто человек). Это **два разных вопроса** — отвечать надо на оба. Сервисный токен сам по себе не доказывает, какой пользователь стоит за запросом: если поверить только ему, любой сможет подать историю за кого угодно («confused deputy» — подмена субъекта на доверенном канале).

## Что наблюдаю сейчас (verified по коду)
- **`POST /intake/stories` открыт** — нет auth-зависимости ([`asgi_app.py:396`](../../../../src/core/api/asgi_app.py#L396)). Для сравнения, `POST /tallinn/issues` уже под сервисным гейтом: `dependencies=[Depends(require_service_auth)]` ([`asgi_app.py:380`](../../../../src/core/api/asgi_app.py#L380)).
- **Сервисный слой существует, но опционален:** `ServiceTokenAuth.require()` — no-op без `SERVICE_API_TOKEN` ([`security.py:54-62`](../../../../src/core/api/security.py#L54)); `require_service_auth` бросает `UnauthorizedError` при включённом токене ([`asgi_app.py:252`](../../../../src/core/api/asgi_app.py#L252)). Токен читается из `Authorization: Bearer` / `X-Service-Token` ([`security.py:16-27`](../../../../src/core/api/security.py#L16)).
- **Пользовательского слоя нет** — gateway не извлекает и не проверяет пользовательский токен на intake.
- **Контракт уровней доверия уже зафиксирован** в [`req-19 §5.1`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md): `Authorization` = доверие к каналу; `submitter` = автор. Эта стори добавляет: **на verify-гейтед мутациях применяются оба слоя**.

## Требование / целевое состояние
- На **всех мутациях публичного контента** (intake-подача + любые будущие write-пути, влияющие на публичную доску — **D-GAUTH-2**) **обязателен сервисный слой доверия** (сервисный токен или mTLS) — отсекает не-доверенные вызовы.
- На том же пути для verify-гейтед действия **обязателен пользовательский токен** (его проверка — [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)).
- **Сервисного токена недостаточно** для решения «за какого пользователя создаём историю»: нужен пользовательский слой.
- Сервисный слой на этих путях — **обязателен** (не опционально-disabled, как сейчас в demo-конфиге).

## Граница и контракт
- Конкретный механизм сервисного доверия (ключ/HMAC/mTLS) и его enforcement — реализация (T-уровень), но требование «оба слоя обязательны» фиксируется здесь.
- Проверка пользователя и статус верификации — [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)/[03](./STORY-GW-GAUTH-03-verification-gate-403.md).
- Разделение «сервисная vs пользовательская идентичность» уже в [`req-19 §5`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) — здесь лишь добавляется обязательность **обоих** слоёв на verify-гейтед путях.

## Подзадачи (черновик)
- **T01** — Инвентаризация write-путей: перечислить все мутации публичного контента (как минимум `POST /intake/stories`; сверить `/tallinn/issues` и иные `@app.post`), зафиксировать, какие уже под `require_service_auth`, какие нет.
- **T02** — Привязать сервисный гейт к `POST /intake/stories` (по образцу `/tallinn/issues:380`): `dependencies=[Depends(require_service_auth)]`.
- **T03** — Сделать сервисный слой **обязательным** на этих путях (политика «enabled required», не demo no-op) — чтобы отсутствие `SERVICE_API_TOKEN` не открывало intake молча; согласовать с конфиг-профилями.
- **T04** — Тесты: вызов без сервисного токена → отказ; с валидным сервисным, но без пользовательского → отказ на verify-гейтед действии (заглушка под GAUTH-02); только сервисный токен не создаёт историю за произвольного пользователя.
- **T05** — story acceptance gate.

## Acceptance Criteria
- [ ] Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op).
- [ ] На verify-гейтед действии пользовательский токен обязателен (его отсутствие — отказ).
- [ ] Наличие только сервисного токена **не** открывает создание истории за произвольного пользователя.
- [ ] Политика «оба слоя» применена ко **всем** write-путям публичного контента (D-GAUTH-2), не только к intake.
- [ ] Поведение зафиксировано как контракт (что отвергается и почему), согласовано с [`04-security §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md).

## Открытые вопросы
- ~~Только `/intake/stories` или все мутации?~~ → **решено D-GAUTH-2: все мутации публичного контента.**
- Сервисное доверие к demo-профилю: где «обязательность» включается жёстко, а где допустим demo-bypass (согласовать с deployment-профилями `config/schema.py`).
