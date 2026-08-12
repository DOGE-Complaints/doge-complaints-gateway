# STORY-GW-DRAFT-03 — Пересмотр канона (supersede docs) + identity-задача

## Meta
- **Key:** `STORY-GW-DRAFT-03`
- **Parent Epic:** [`../../../EPIC-M2-21-story-draft-handoff.md`](../../../EPIC-M2-21-story-draft-handoff.md)
- **Type:** docs (пометки superseded + кросс-репо задача)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED (иначе два противоречащих описания флоу — anti-pattern «Legacy Accumulation»)
- **source:** [`../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Decision Ref:** backlog file above; [`interview-story-draft-handoff-2026-07-03`](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-5, D-DRAFT-6**); [`mvp-integration-plan-2026-07-02 §2`](../../../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000045-20260703-gw-draft-03-supersede-gpt-submit-authz-canon.yaml`](../../../../gateway-active-packages/pkg-000045-20260703-gw-draft-03-supersede-gpt-submit-authz-canon.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05
- **Зависит от:** [GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash/STORY-GW-DRAFT-01-story-draft-stash.md), [GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Разблокирует:** [GW-DRAFT-04](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Парная:** [GW-DRAFT-04](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) (эта — **docs**, та — **код**)

## Зачем простыми словами
Раньше канон был «GPT сам постит историю с двумя токенами» — [`04-security.md §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) + пакет [`gpt-submit-authz`](../../../../backlog-stories/gpt-submit-authz/INDEX.md). После разворота на «браузер сабмитит» эта часть **осиротела**. Нельзя оставлять два взаимоисключающих описания — надо явно пометить старое как superseded и синхронизировать канон. Эта стори — **только документация/пометки**; удаление кода — в [GW-DRAFT-04](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md).

## Что наблюдаю сейчас (verified по коду/докам)
- **Канон-SSOT «GPT сам сабмитит»:** [`04-security.md §A` шаги 6-8](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) (sequence-диаграмма) — **чужой репо** (identity).
- **Пакет [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md):** GAUTH-01 (два токена на submit), GAUTH-02 (introspection OAuth-токена GPT), GAUTH-03 (verify-gate 403), GAUTH-04 (авторитетный автор) — все 🔵 Done (pkg-000039..042).
- **Что переиспользуется (остаётся валидным):** GAUTH-04 (`submitter=sub`) + verify-канон (GAUTH-03: `verification_required`) — реюз в [GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate/STORY-GW-DRAFT-02-browser-submit-verification-gate.md). **Осиротело:** GAUTH-01 (два токена от GPT), OAuth-introspection именно токена GPT (GAUTH-02). Точный инвентарь — [interview §Инвентарь](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md).
- **Прочие ссылки на старую модель:** [`09-gateway-expectations.md`](../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md) (identity), ID-08 «Gateway (submit-story)» блок.

## Требование / целевое состояние (D-DRAFT-5)
- **A. Пометить superseded** в [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md): GAUTH-01 и «GPT сам сабмитит» — superseded by `story-draft-handoff/` (browser-submit). **Сохранить историю, не удалять** (аудиты/pkg остаются, D-DRAFT-6).
- **B. Развести переиспользуемое:** явно связать GAUTH-04 (автор) и verification_required-канон (GAUTH-03) с [GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate/STORY-GW-DRAFT-02-browser-submit-verification-gate.md).
- **C. As-built в gateway-доках:** зафиксировать browser-submit как актуальную модель в runtime-docs gateway (`architecture-and-layers-as-is.md` / api-reference), чтобы gateway-SSOT не противоречил.
- **D. Identity-задача (кросс-репо, D-DRAFT-5):** **не** править `04-security.md`/`09-gateway-expectations.md` сами — **завести явную identity-side задачу** (файл-указатель или backlog-стори в identity) на приведение канона к browser-submit; в gateway-доках оставить пометку «канон identity — рассинхронизирован, см. identity-задачу».

## Out of scope
- правка `doge-identity-service/docs/runtime-docs/04-security.md` / `09-gateway-expectations.md` в этой волне
- удаление кода GAUTH → [GW-DRAFT-04](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- удаление аудитов/pkg-000039..042 / run-summary (D-DRAFT-6)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-draft-03-t01-gpt-submit-authz-superseded-index`](./task-gw-draft-03-t01-gpt-submit-authz-superseded-index/README.md) | pkg-000045 |
| 2 | [`task-gw-draft-03-t02-gateway-runtime-docs-browser-submit-as-built`](./task-gw-draft-03-t02-gateway-runtime-docs-browser-submit-as-built/README.md) | pkg-000045 |
| 3 | [`task-gw-draft-03-t03-identity-side-canon-sync-backlog-pointer`](./task-gw-draft-03-t03-identity-side-canon-sync-backlog-pointer/README.md) | pkg-000045 |
| 4 | [`task-gw-draft-03-t04-grep-doc-consistency-no-dual-truth`](./task-gw-draft-03-t04-grep-doc-consistency-no-dual-truth/README.md) | pkg-000045 |
| 5 | [`task-gw-draft-03-t05-story-acceptance-gate`](./task-gw-draft-03-t05-story-acceptance-gate/README.md) | pkg-000045 |

## Audit follow-up (G2 — GAUTH reuse discoverability)

Post-audit P5 2026-07-03. **Не** в pkg-000045. Исполнение: `run_mode=gw_draft_03_audit_followup` ([`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)).

| Order | Task folder | Wave |
|-------|-------------|------|
| 6 | [`task-gw-draft-03-t06-gauth-reused-discoverability-banners`](./task-gw-draft-03-t06-gauth-reused-discoverability-banners/README.md) | audit override |

**Audit ref:** [`audit-gw-draft-03-supersede-gpt-submit-authz-canon-2026-07-03`](../../../../../../analysis/audit-gw-draft-03-supersede-gpt-submit-authz-canon-2026-07-03.md) §3 **G2** — **Done** 2026-07-03 (`run_mode=gw_draft_03_audit_followup`). **G1** (identity `04-security` sync) → [STORY-IDS-DOC-DRAFT-05](../../../../../../../doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md), `activation: none`.

## Acceptance Criteria
- [x] `gpt-submit-authz/INDEX.md` явно помечает superseded-часть; читатель не примет её за актуальный флоу.
- [x] Переиспользуемое (GAUTH-04, verification_required-канон) явно связано с `story-draft-handoff/`.
- [x] Gateway runtime-docs отражают browser-submit как as-built; нет gateway-док с «GPT сам сабмитит» без пометки.
- [x] Заведена identity-side задача на правку `04-security.md`/`09-gateway-expectations.md` (кросс-репо, D-DRAFT-5); gateway не редактирует чужой канон сам.
- [x] История (аудиты/pkg-000039..042) **не** удалена (D-DRAFT-6).

## Швы
[`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md), gateway [`runtime-docs/`](../../../../../runtime-docs/) (architecture-and-layers-as-is.md, api-reference); identity-side указатель — [`STORY-IDS-DOC-DRAFT-05`](../../../../../../../doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md). Ссылки: [`04-security.md`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md), [`09-gateway-expectations.md`](../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md), [`STORY-SPA-ID-08`](../../../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-08-gpt-verification-entry.md).
