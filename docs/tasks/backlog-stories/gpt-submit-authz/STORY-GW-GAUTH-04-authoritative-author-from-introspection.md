# STORY-GW-GAUTH-04 — Авторитетный автор = `sub` из introspection (сверка с submitter/req-19)

> **↔ Reused (browser submit):** authoritative author (`submitter=sub`) на `POST /story-drafts/{id}/submit` ([GW-DRAFT-02](../../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)). Разведение: [`gpt-submit-authz/INDEX.md`](./INDEX.md).

## Meta
- **Key:** `STORY-GW-GAUTH-04`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline [pkg-000042](../../gateway-active-packages/pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml) (T01–T06, gate PASS 2026-06-25): `authoritative_submitter_from_introspection` (автор = проверенный `sub`), подмена до персиста + `story_intake_submitter_mismatch`-лог, req-19 §5.3 согласован; 6 contract + 554 unit. Код-аудит [`audit-gw-gauth-04-...`](../../../analysis/audit-gw-gauth-04-authoritative-author-from-introspection-2026-06-25.md). **Пакет gpt-submit-authz (GAUTH-01→04) завершён end-to-end.** SSOT исполнения — pipeline-копия.
- **Приоритет:** P2
- **Тип:** implement (authorship-источник истины)
- **Закрывает:** доверие авторства непроверенному `submitter` из тела вместо проверенного `sub`
- **Источник процесса:** [`04-security §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 8 + [`req-19 §5`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md).
- **Основание:** [`interview-gpt-submit-authz-2026-06-24`](./interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-4)
- **Зависит от:** [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)

## Зачем простыми словами
Кто автор истории? Сейчас автор берётся **из тела запроса** (`submitter.external_user_id`, который **заявил GPT**). Но когда gateway уже проверил пользователя у identity и получил подтверждённый `sub`, **именно он** должен считаться автором — заявленному в payload доверять меньше, чем проверенному токеном. Иначе доверенный канал может записать историю на чужой id.

## Что наблюдаю сейчас (контекст до реализации)

> Gap до GAUTH-04. Актуальное — **Текущее состояние (post-Done)**.

## Текущее состояние (post-Done, verified)

- `authoritative_submitter_from_introspection` на submit ([`authoritative_submitter.py`](../../../../src/core/identity/authoritative_submitter.py)); `sub` из [`me_client.py`](../../../../src/core/identity/me_client.py) `/me` response.
- pkg-000042 gate PASS; автор = проверенный `sub`, не payload submitter.
- Legacy `POST /intake/stories` — к удалению [GW-DRAFT-06](../../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md).

## Контекст до реализации (исторический)

- **Автор сейчас = непроверенный payload:** intake читал `submitter.external_user_id` из тела ([`intake/contracts.py:223-227`](../../../../src/core/intake/contracts.py#L223)).
- **Проверенный `sub`** — из identity; gateway получает через `/me` (GW-DRAFT-02), не через удалённый GAUTH-02 OAuth introspect.

## Требование / целевое состояние
- При успешном introspection ([GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)) **авторство фиксируется по проверенному `sub`**, а не по непроверённому `submitter.external_user_id` из тела.
- Расхождение «payload-submitter ↔ introspected `sub`» разрешается **в пользу `sub`** (зафиксировать в контракте; опц. логировать расхождение как сигнал).
- Это **уточнение** к [`req-19 §5`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (lineage/authorship), не отдельная новая модель авторства — согласовать формулировки, без дублирования.
- **Fallback снят (D-GAUTH-4):** нет introspection → fail-closed (история не создаётся, см. [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)/[03](./STORY-GW-GAUTH-03-verification-gate-403.md)) → вопрос «доверять ли payload-submitter без introspection» **не возникает** (истории без проверки нет).

## Граница и контракт
- Хранение авторства/lineage/Story Store — это **req-19** и реализация; здесь только **источник истины об авторе**, не схема хранения.
- Получение `sub` — [`me_client.py`](../../../../src/core/identity/me_client.py) на browser submit (GW-DRAFT-02).
- Маппинг `sub`→существующая колонка (`submitter_external_user_id` vs новое поле «verified subject») — реализационный (T-уровень), но **истина = `sub`** фиксируется здесь.

## Подзадачи (черновик)
- **T01** — Определить точку подстановки: после успешного introspection авторство берётся из `sub` (а не из `submitter.external_user_id`), до записи в Story Store ([`application/services.py:238`](../../../../src/core/application/services.py#L238)).
- **T02** — Контракт расхождения: `payload.submitter.external_user_id != sub` → приоритет `sub`; решить, логировать ли расхождение (сигнал подмены).
- **T03** — Согласовать формулировку с [`req-19 §5`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (один источник, без параллельной модели авторства) — правка req-19 при необходимости.
- **T04** — Тесты: при introspection автор = `sub`; при расхождении побеждает `sub`; (fail-closed: без introspection истории нет — отдельного fallback-теста авторства не требуется).
- **T05** — story acceptance gate.

## Acceptance Criteria
- [x] Автор сохранённой истории соответствует `sub` из introspection.
- [x] При расхождении payload-submitter ↔ introspected `sub` — приоритет у `sub` (зафиксировано в контракте).
- [x] Формулировка авторства согласована с [`req-19 §5`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (единый источник, без параллельной модели).
- [x] Кейс «нет introspection» не порождает историю с payload-автором (следствие fail-closed D-GAUTH-4).

## Открытые вопросы
- ~~Fallback на payload-submitter при недоступном introspection?~~ → **снято D-GAUTH-4 (fail-closed):** без introspection истории нет.
- Хранить ли исходный заявленный `submitter` рядом с проверенным `sub` (для аудита расхождений) — реализационное.
