# STORY-GW-DRAFT-03 — Пересмотр канона (supersede docs) + identity-задача

## Meta
- **Key:** `STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — pipeline [pkg-000045](../../gateway-active-packages/pkg-000045-20260703-gw-draft-03-supersede-gpt-submit-authz-canon.yaml) (T01–T05, gate PASS 2026-07-03): superseded-блок в gpt-submit-authz/INDEX (GAUTH-01/02 superseded→GW-DRAFT-04, 03/04 reused), as-built browser-submit в architecture §4.1, identity-указатель [STORY-IDS-DOC-DRAFT-05](../../../../../doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md) без правки чужого канона (D-DRAFT-5), история цела (D-DRAFT-6). Код-аудит [`audit-gw-draft-03-...`](../../../analysis/audit-gw-draft-03-supersede-gpt-submit-authz-canon-2026-07-03.md). **G1:** финальная синхронизация 04-security — за identity-задачей. SSOT исполнения — pipeline-копия.
- **Приоритет:** 🟠 MED (иначе два противоречащих описания флоу — anti-pattern «Legacy Accumulation»)
- **Тип:** docs (пометки superseded + кросс-репо задача)
- **Основание:** [`interview-story-draft-handoff-2026-07-03`](./interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-5**); [`mvp-integration-plan-2026-07-02 §2`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Зависит от:** [GW-DRAFT-01](./STORY-GW-DRAFT-01-story-draft-stash.md), [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) (сначала утверждаем новую модель в доках/коде)
- **Парная:** [GW-DRAFT-04](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) (эта — **docs**, та — **код**)

## Зачем простыми словами
Раньше канон был «GPT сам постит историю с двумя токенами» — [`04-security.md §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) + пакет [`gpt-submit-authz`](../gpt-submit-authz/INDEX.md). После разворота на «браузер сабмитит» эта часть **осиротела**. Нельзя оставлять два взаимоисключающих описания — надо явно пометить старое как superseded и синхронизировать канон. Эта стори — **только документация/пометки**; удаление кода — в [GW-DRAFT-04](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md).

## Что наблюдаю сейчас (verified по коду/докам)
- **Канон-SSOT «GPT сам сабмитит»:** [`04-security.md §A` шаги 6-8](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) (sequence-диаграмма) — **чужой репо** (identity).
- **Пакет [`gpt-submit-authz/INDEX.md`](../gpt-submit-authz/INDEX.md):** GAUTH-01 (два токена на submit), GAUTH-02 (introspection OAuth-токена GPT), GAUTH-03 (verify-gate 403), GAUTH-04 (авторитетный автор) — все 🔵 Done (pkg-000039..042).
- **Что переиспользуется (остаётся валидным):** GAUTH-04 (`submitter=sub`) + verify-канон (GAUTH-03: `verification_required`) — реюз в [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md). **Осиротело:** GAUTH-01 (два токена от GPT), OAuth-introspection именно токена GPT (GAUTH-02). Точный инвентарь — [interview §Инвентарь](./interview-story-draft-handoff-2026-07-03.md).
- **Прочие ссылки на старую модель:** [`09-gateway-expectations.md`](../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md) (identity), ID-08 «Gateway (submit-story)» блок.

## Требование / целевое состояние (D-DRAFT-5)
- **A. Пометить superseded** в [`gpt-submit-authz/INDEX.md`](../gpt-submit-authz/INDEX.md): GAUTH-01 и «GPT сам сабмитит» — superseded by `story-draft-handoff/` (browser-submit). **Сохранить историю, не удалять** (аудиты/pkg остаются, D-DRAFT-6).
- **B. Развести переиспользуемое:** явно связать GAUTH-04 (автор) и verification_required-канон (GAUTH-03) с [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md).
- **C. As-built в gateway-доках:** зафиксировать browser-submit как актуальную модель в runtime-docs gateway (`architecture-and-layers-as-is.md` / api-reference), чтобы gateway-SSOT не противоречил.
- **D. Identity-задача (кросс-репо, D-DRAFT-5):** **не** править `04-security.md`/`09-gateway-expectations.md` сами — **завести явную identity-side задачу** (файл-указатель или backlog-стори в identity) на приведение канона к browser-submit; в gateway-доках оставить пометку «канон identity — рассинхронизирован, см. identity-задачу».

## Подзадачи (черновик)
- **T01** — Superseded-блок в [`gpt-submit-authz/INDEX.md`](../gpt-submit-authz/INDEX.md): что осиротело (GAUTH-01, GPT-two-token), что живёт (GAUTH-03/04), ссылка на `story-draft-handoff/`.
- **T02** — As-built browser-submit в gateway runtime-docs (`architecture-and-layers-as-is.md` + api-reference кросс-ссылки).
- **T03** — Завести identity-side задачу на правку `04-security.md §A` + `09-gateway-expectations.md` (D-DRAFT-5); в gateway оставить указатель.
- **T04** — Grep-верификация «нет двух истин»: пройти ссылки на «GPT сам сабмитит»/`X-User-Token` в gateway-доках, привести к browser-submit или пометить.
- **T05** — story acceptance gate (doc-consistency).

## Acceptance Criteria
- [ ] `gpt-submit-authz/INDEX.md` явно помечает superseded-часть; читатель не примет её за актуальный флоу.
- [ ] Переиспользуемое (GAUTH-04, verification_required-канон) явно связано с `story-draft-handoff/`.
- [ ] Gateway runtime-docs отражают browser-submit как as-built; нет gateway-док с «GPT сам сабмитит» без пометки.
- [ ] Заведена identity-side задача на правку `04-security.md`/`09-gateway-expectations.md` (кросс-репо, D-DRAFT-5); gateway не редактирует чужой канон сам.
- [ ] История (аудиты/pkg-000039..042) **не** удалена (D-DRAFT-6).

## Швы
[`gpt-submit-authz/INDEX.md`](../gpt-submit-authz/INDEX.md), gateway [`runtime-docs/`](../../../runtime-docs/) (architecture-and-layers-as-is.md, api-reference); identity-side указатель — новый файл/стори в identity. Ссылки: [`04-security.md`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md), [`09-gateway-expectations.md`](../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md), [`STORY-SPA-ID-08`](../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-08-gpt-verification-entry.md).
