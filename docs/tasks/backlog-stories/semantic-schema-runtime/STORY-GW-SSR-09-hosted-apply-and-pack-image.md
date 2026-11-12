# STORY-GW-SSR-09 — Hosted apply binding migration + packs in deploy image

## Meta
- **Key:** `STORY-GW-SSR-09-hosted-apply-and-pack-image`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave ops (sequence **9**)
- **Тип:** ops / deploy (не invent HTTP)
- **Parent REQ:** 51 DATA persist; runtime-docs мануал
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](./orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-02 (DDL уже в репо)

## Зачем простыми словами

На sqlite pack-поля появляются сами. На hosted Supabase, пока миграция не применена, omit-probe **вырезает** binding — civic живёт, pack **не** пишется. Плюс процесс должен видеть файлы `schema-packs/` (или `SCHEMA_PACKS_ROOT`). Иначе intake с `schema_binding` на проде ломается или молча теряет payload.

## Scope / Out of scope

**In:** применить [`20260828_1400_gw_ssr_02_stories_schema_binding.sql`](../../../../supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql) на hosted; рестарт процесса (probe кэшируется); убедиться, что каталог `schema-packs/` попадает в runtime working tree образа (или volume + env); smoke: после apply omit-probe **не** режет binding; civic `/ready` не 503.

**Out:** класть binding-колонки в `required_columns_ready` ([`db_supabase.py:388`](../../../../src/core/infrastructure/db_supabase.py)); invent HTTP; GPT emit; смена `AppConfig` обязательна (поле `SCHEMA_PACKS_ROOT` там **нет** — факт, не таск «добавить, иначе нельзя»).

## Verified current state

| Fact | Ref |
|------|-----|
| Hosted DDL | [`20260828_1400_gw_ssr_02_stories_schema_binding.sql`](../../../../supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql) |
| Omit-probe binding | [`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py) `_STORIES_BINDING_COLUMNS` `:333–341`; `required_stories_binding_columns_ready` `:366`; omit из SELECT/save |
| `/ready` required set | `required_columns_ready` **без** binding имён [`:388`](../../../../src/core/infrastructure/db_supabase.py) |
| Packs root | [`resolver.py:19–30`](../../../../src/core/schema/resolver.py) `SCHEMA_PACKS_ROOT` или `<gateway-root>/schema-packs/` |
| Dockerfile в gateway | **Not found** (Glob) — деплой не invent из этой стори; проверить фактический build (Nixpacks/Railway root), что `schema-packs/` копируется с исходниками |
| Мануал | [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) |

## Стыковка

Не менять `/ready` required columns. После apply — **рестарт**, иначе кэш probe остаётся «колонок нет».

Если CWD процесса ≠ корень gateway, default path resolver не найдёт паки → `SCHEMA_PACKS_ROOT` на volume/образе.

## Подзадачи (первый слой)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Hosted SQL | Apply `20260828_1400_*`; проверить шесть колонок на `stories` | DROP таблиц; класть имена в `required_columns_ready` |
| **T02** | Process | Рестарт gateway; smoke omit-probe: binding round-trip | Менять civic path |
| **T03** | Image | Pack files видны resolver’у (cwd или `SCHEMA_PACKS_ROOT`); intake example pack не `unknown schema` | Invent Dockerfile без факта текущего build |

## Target / AC

- [x] Hosted `stories` имеет шесть nullable binding-колонок.
- [x] После рестарта persist `schema_binding` на supabase не вырезается omit-probe.
- [x] `/ready` не требует binding-колонки.
- [x] Resolver находит example pack в деплое.
- [x] Нет нового HTTP.

## Dependencies

- SSR-02 Done. Sibling GPT REQ-45 не блокирует apply (ручной JSON достаточен для smoke).
