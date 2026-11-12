# STORY-GW-SSR-11 — Pack-declared fields on Issue projection (gateway)

## Meta
- **Key:** `STORY-GW-SSR-11-pack-declared-issue-projection`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave product (sequence **11**; overnight **после** SSR-13)
- **Тип:** implement (projection + pack data; первый слой)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Parent REQ:** 51 SPA-003/004 (gateway **называет** derived fields; payload не auto на карточке)
- **Decision:** INDEX **D-SSR-7** / **D-SSR-3** / **D-SSR-6**
- **decision_ref:** backlog SSR-11 + INDEX **D-SSR-7** / **D-SSR-3** / **D-SSR-6**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml`](../../../../gateway-active-packages/pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml)
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-05 (pack Issue существует); **SSR-13** (канон `GET /node/issues`, D-SSR-7)
- **Scaffolded:** 2026-08-29T19:08:43Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 SPA-003/004 | named derived fields; no auto-dump |
| Decision | INDEX **D-SSR-7** `GET /node/issues`; **D-SSR-3** identity; **D-SSR-6** SSR-06/07 Draft not this pkg |

- **Разблокирует:** G11 → SSR-14. **Not** SSR-06/07/12/14/15 this pkg
- **Не reopen:** SSR-01…05 / 08 / 09 / 10 / 13 product; T-wave G3 «`GET /tallinn/issues` stays» = historical
- **Не трогаем:** identity-service / claim keys (**D-SSR-3**); overlay UI spa-app; `SchemaRuntime.project` stub

## Nested tasks (pkg-000070)

| ID | Folder |
|----|--------|
| T00 / R1 | [`task-gw-ssr-11-t00-pack-card-fields-contract`](./task-gw-ssr-11-t00-pack-card-fields-contract/README.md) |
| T01 | [`task-gw-ssr-11-t01-loader-card-allowlist`](./task-gw-ssr-11-t01-loader-card-allowlist/README.md) |
| T02 | [`task-gw-ssr-11-t02-project-pack-issue-fields`](./task-gw-ssr-11-t02-project-pack-issue-fields/README.md) |
| T03 | [`task-gw-ssr-11-t03-tests-public-dict-no-dump`](./task-gw-ssr-11-t03-tests-public-dict-no-dump/README.md) |
| T04 | [`task-gw-ssr-11-t04-story-acceptance-gate`](./task-gw-ssr-11-t04-story-acceptance-gate/README.md) |
| T05 | [`task-gw-ssr-11-t05-audit-g1-epic-dod-ssot`](./task-gw-ssr-11-t05-audit-g1-epic-dod-ssot/README.md) |

## Зачем простыми словами

Карточка Issue сейчас одна на всех: title/type/labels/geo… Кастомный payload на `GET /node/issues` **не** попадает. Нужно: в паке указать, **какие** поля показать, gateway положить их в проекцию **именованно**. Не вывалить весь JSON. SPA рисует overlay по уже названным полям (sibling spa-16 overlay later; пути — SSR-13).

## Scope / Out of scope

**In:** pack объявляет allowlist dotted paths (имя ключа loader — **refine**); gateway projection для pack-promoted Issue включает только эти поля (или безопасный named sidecar, не сырой `structured_payload`); тесты: `to_public_dict` / public read **без** полного payload; civic Issues без binding — форма карточки как сейчас.

**Out:** overlay UI spa-app; form builder; invent filter HTTP; `build_index` как замена этому; класть `node_private` / `forbidden` field_policy на карточку (SEC-004). URL-репозитории SPA — **SSR-13**, не эта стори.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-11 pkg-000070)** Public card | [`dto.py`](../../../../../../src/core/projection/dto.py) `to_public_dict` — **нет** `structured_payload` token; optional named sidecar `schema_card` |
| **As-of-Done** Loader key | [`schema-packs/README.md`](../../../../../../schema-packs/README.md) `card_fields`; [`resolver.py`](../../../../../../src/core/schema/resolver.py) `_parse_card_fields`; `legal_process` / `tallinn_civic` without key stay civic-form |
| **As-of-Done** Extract | [`card_fields.py`](../../../../../../src/core/projection/card_fields.py); wired [`issue_create.py`](../../../../../../src/core/application/issue_create.py) `_to_public_payload` |
| Projection input | [`input.py:8–31`](../../../../../../src/core/projection/input.py) — civic narrative/geo; no new required keys on `DOGEIssue` |
| `SchemaRuntime.project` | [`runtime.py:68–72`](../../../../../../src/core/schema/runtime.py) `NotImplementedError` — stub stays |
| Public read | [`asgi_app.py:462`](../../../../../../src/core/api/asgi_app.py) `GET /node/issues` |
| **Historical (pre-P3)** | no `card_fields` on `SchemaContext`; `to_public_dict()` civic-only |
| SPA overlay UI | sibling 16: **not this story** |

SPA-003: payload MUST NOT automatically become Issue. Эта стори как раз **именованная** проекция, не auto-dump.

## Стыковка

Не invent имена полей карточки в SPA. Gateway SSOT: pack allowlist → фиксированная форма на проводе (refine: вложенный объект vs плоские ключи). Пока имена не зафиксированы parent — не ломать контракт REQ-09 enums (`type`/`status`).

`field_policy` `forbidden` / `node_private` не проецировать даже если попали в allowlist по ошибке.

Civic `DOGEIssue` без новых required keys.

## Подзадачи (первый слой)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **R1** | Contract | Ключ pack.json + JSON shape на `GET /node/issues` (named, не dump) | Invent SPA routes; dump payload |
| **T01** | Loader | Читать allowlist; default = ничего сверх civic card | Проецировать весь payload |
| **T02** | Projection | Pack Issue: только allowlist leaf’ы; civic Issues unchanged | Менять civic extraction_policy as-is для всех |
| **T03** | Tests | Public dict без полного `structured_payload`; private paths отсутствуют | spa-app UI |

## Target / AC

- [x] Pack MAY объявить card fields; absent = текущая civic-форма карточки.
- [x] Public Issue **не** содержит целиком `structured_payload`.
- [x] `forbidden` / `node_private` не утекают.
- [x] Public read path = `GET /node/issues` (D-SSR-7 / SSR-13), не `/tallinn/issues`.
- [x] Overlay UI spa-app в этой стори не менять.

## Dependencies

- SSR-05; **SSR-13** (пути). Overlay UI — spa-16 later, не path-rename.
- SSR-07 `project()` stub — не подменять эту стори «вызовом NotImplementedError».
