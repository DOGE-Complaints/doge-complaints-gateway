# STORY-GW-GAUTH-04 — Авторитетный автор = `sub` из introspection (сверка с submitter/req-19)

## Meta
- **Key:** `STORY-GW-GAUTH-04`
- **Parent Epic:** [`../../../EPIC-M2-20-gpt-submit-authz.md`](../../../EPIC-M2-20-gpt-submit-authz.md)
- **Type:** implement (authorship-источник истины)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P2
- **source:** [`../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md`](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Закрывает:** доверие авторства непроверенному `submitter` из тела вместо проверенного `sub`
- **Источник процесса:** [`04-security §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 8 + [`req-19 §5`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md).
- **Decision Ref:** backlog file above; [`interview-gpt-submit-authz-2026-06-24`](../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-4); [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml`](../../../../gateway-active-packages/pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **Зависит от:** [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md) (Done), [GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403/STORY-GW-GAUTH-03-verification-gate-403.md) (Done)

## Зачем простыми словами
Кто автор истории? Сейчас автор берётся **из тела запроса** (`submitter.external_user_id`, который **заявил GPT**). Но когда gateway уже проверил пользователя у identity и получил подтверждённый `sub`, **именно он** должен считаться автором — заявленному в payload доверять меньше, чем проверенному токеном. Иначе доверенный канал может записать историю на чужой id.

## Что наблюдаю сейчас (verified по коду)
- **GW-GAUTH-02/03 Done:** `require_user_token` вызывает identity introspection, сохраняет `request.state.user_introspection` (`IntrospectionResult` с `sub`, `phone_verified`) — [`asgi_app.py:329`](../../../../../../src/core/api/asgi_app.py#L329); verify-гейт блокирует unverified до handler — [`verification_gate.py`](../../../../../../src/core/identity/verification_gate.py).
- **Introspection не plumbed в persist:** `POST /intake/stories` вызывает `handle_story_intake` **без** передачи `user_introspection` — [`asgi_app.py:482-488`](../../../../../../src/core/api/asgi_app.py#L482).
- **Автор сейчас = непроверенный payload:** intake читает `submitter.external_user_id` + `identity_issuer` из тела как есть ([`intake/contracts.py:223-227`](../../../../../../src/core/intake/contracts.py#L223), [`:355-357`](../../../../../../src/core/intake/contracts.py#L355)) и пишет в Story Store ([`application/services.py:237-238`](../../../../../../src/core/application/services.py#L237) → колонка `submitter_identity_issuer`, [`domain/contracts.py:48-49`](../../../../../../src/core/domain/contracts.py#L48)). Семантического парсинга/проверки нет (по req-19 формат `external_user_id` намеренно opaque).
- **Проверенный `sub` в introspection identity** — [`oauth/introspection.py:30`](../../../../../../../doge-identity-service/src/core/oauth/introspection.py#L30); gateway получает через GAUTH-02, но **не использует** для авторства при persist.
- **req-19 §5.3** уже требует «нет подделки с клиента»: `submitter` доверять только в связке с проверенным сервисным вызовом ([`req-19 §5.3`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md)). Эта стори уточняет: при наличии introspection авторитетен `sub`.
- Лог intake использует payload submitter — [`handlers.py:170`](../../../../../../src/core/api/handlers.py#L170).

## Требование / целевое состояние
- При успешном introspection ([GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md)) **авторство фиксируется по проверенному `sub`**, а не по непроверённому `submitter.external_user_id` из тела.
- Расхождение «payload-submitter ↔ introspected `sub`» разрешается **в пользу `sub`** (зафиксировать в контракте; опц. логировать расхождение как сигнал).
- Это **уточнение** к [`req-19 §5`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (lineage/authorship), не отдельная новая модель авторства — согласовать формулировки, без дублирования.
- **Fallback снят (D-GAUTH-4):** нет introspection → fail-closed (история не создаётся, см. [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md)/[03](../STORY-GW-GAUTH-03-verification-gate-403/STORY-GW-GAUTH-03-verification-gate-403.md)) → вопрос «доверять ли payload-submitter без introspection» **не возникает** (истории без проверки нет).

## Граница и контракт
- Хранение авторства/lineage/Story Store — это **req-19** и реализация; здесь только **источник истины об авторе**, не схема хранения.
- Получение `sub` — [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md).
- Маппинг `sub`→существующая колонка (`submitter_external_user_id` vs новое поле «verified subject») — реализационный (T-уровень), но **истина = `sub`** фиксируется здесь.

## Out of scope
- Схема Story Store / новые колонки «verified subject»
- Повторная реализация GW-GAUTH-02 introspection или GW-GAUTH-03 verify-гейта
- Identity OAuth-сервер, выдача токенов, verify-флоу телефона

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-gauth-04-t01-authoritative-sub-mapping`](./task-gw-gauth-04-t01-authoritative-sub-mapping/README.md) | pkg-000042 |
| 2 | [`task-gw-gauth-04-t02-plumb-introspection-to-intake`](./task-gw-gauth-04-t02-plumb-introspection-to-intake/README.md) | pkg-000042 |
| 3 | [`task-gw-gauth-04-t03-mismatch-priority-and-log`](./task-gw-gauth-04-t03-mismatch-priority-and-log/README.md) | pkg-000042 |
| 4 | [`task-gw-gauth-04-t04-req-19-section-5-alignment`](./task-gw-gauth-04-t04-req-19-section-5-alignment/README.md) | pkg-000042 |
| 5 | [`task-gw-gauth-04-t05-authoritative-author-contract-tests`](./task-gw-gauth-04-t05-authoritative-author-contract-tests/README.md) | pkg-000042 |
| 6 | [`task-gw-gauth-04-t06-story-acceptance-gate`](./task-gw-gauth-04-t06-story-acceptance-gate/README.md) | pkg-000042 |

## Подзадачи (черновик)
- **T01** — Определить точку подстановки: после успешного introspection авторство берётся из `sub` (а не из `submitter.external_user_id`), до записи в Story Store ([`application/services.py:238`](../../../../../../src/core/application/services.py#L238)).
- **T02** — Контракт расхождения: `payload.submitter.external_user_id != sub` → приоритет `sub`; решить, логировать ли расхождение (сигнал подмены).
- **T03** — Согласовать формулировку с [`req-19 §5`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (один источник, без параллельной модели авторства) — правка req-19 при необходимости.
- **T04** — Тесты: при introspection автор = `sub`; при расхождении побеждает `sub`; (fail-closed: без introspection истории нет — отдельного fallback-теста авторства не требуется).
- **T05** — story acceptance gate.

## Acceptance Criteria
- [x] Автор сохранённой истории соответствует `sub` из introspection.
- [x] При расхождении payload-submitter ↔ introspected `sub` — приоритет у `sub` (зафиксировано в контракте).
- [x] Формулировка авторства согласована с [`req-19 §5`](../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (единый источник, без параллельной модели).
- [x] Кейс «нет introspection» не порождает историю с payload-автором (следствие fail-closed D-GAUTH-4).

## Открытые вопросы
- ~~Fallback на payload-submitter при недоступном introspection?~~ → **снято D-GAUTH-4 (fail-closed):** без introspection истории нет.
- Хранить ли исходный заявленный `submitter` рядом с проверенным `sub` (для аудита расхождений) — реализационное.
