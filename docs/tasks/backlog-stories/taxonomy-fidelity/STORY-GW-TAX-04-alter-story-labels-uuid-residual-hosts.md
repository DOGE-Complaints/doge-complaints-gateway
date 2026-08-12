# STORY-GW-TAX-04 — ALTER `story_labels` on residual UUID hosts

## Meta
- **Key:** `STORY-GW-TAX-04-alter-story-labels-uuid-residual-hosts`
- **Пакет:** [`taxonomy-fidelity/`](./INDEX.md)
- **Status:** ⏸ Deferred — ops residual; не MVP value-loop
- **Приоритет:** ⚪ LOW — только при реальном broken host с UUID `story_labels`
- **Тип:** ops / migration successor
- **Основание:** [TAX-03 audit G2](../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) — `CREATE TABLE IF NOT EXISTS` не меняет тип уже созданной UUID-таблицы
- **Зависит от:** [GW-TAX-03](./STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) Done (repo migration text SSOT); [GW-DRAFT-07](../story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) Done (Public Node path)
- **Не reopen:** GW-TAX-03 product AC; GW-DRAFT-07

## Зачем простыми словами

TAX-03 выровнял **repo** migration на `story_id text` для **fresh** apply. Host, где старый UUID DDL уже успешно лёг (если `stories.story_id` когда-то был UUID), не получит type change от `IF NOT EXISTS`. Public Node уже text через DRAFT-07. Нужен отдельный ops successor (`ALTER` / rebuild) **только** при подтверждённом residual UUID host — вне DoD TAX-03.

## Что наблюдаю сейчас (verified)

| Источник | Claim | Ref |
|----------|-------|-----|
| TAX-03 migration | `CREATE TABLE IF NOT EXISTS` + text FK | [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) |
| Audit G2 | IF NOT EXISTS не ALTER’ит существующую UUID-таблицу | [`audit-gw-tax-03-…§G2`](../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) |
| Public Node | text FK post DRAFT-07 | DRAFT-07 evidence / readiness |

## Требование / целевое состояние (при активации)

1. Inventory: есть ли hosted/CI host с `story_labels.story_id` UUID при text `stories.story_id` (или иной broken combo).
2. Successor migration или ops runbook: `ALTER COLUMN` / drop-recreate с data safety — **не** silent edit TAX-03 file again without decision.
3. Verify `/ready` + submit path после apply.
4. Не трогать fresh-host path, уже закрытый TAX-03.

## Acceptance Criteria (при активации)

- [ ] Подтверждённый residual host (или явный «no residual — close as N/A»).
- [ ] Successor DDL/runbook + evidence apply.
- [ ] Readiness / submit regression green на целевом host.
- [ ] TAX-03 / DRAFT-07 не reopen без нужды.

## Границы

- **In scope:** ops ALTER / residual UUID hosts only.
- **Вне scope:** MVP board/submit value-loop; SPA; GPT; rewriting TAX-03 AC; analysis-only doc polish.

## Условие реактивации

- Обнаружен broken host с UUID `story_labels` **или** явный ops-запрос на ALTER successor.
- Иначе остаётся Deferred; fresh-host = TAX-03 migrations as-is.
