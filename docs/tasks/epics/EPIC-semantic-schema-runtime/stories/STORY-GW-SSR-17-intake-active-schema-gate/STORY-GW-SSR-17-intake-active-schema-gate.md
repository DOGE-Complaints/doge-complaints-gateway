# STORY-GW-SSR-17 — Intake только активная схема ноды

## Meta
- **Key:** `STORY-GW-SSR-17-intake-active-schema-gate`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — node-schema wave (sequence **17**)
- **Тип:** implement (intake + stash + HTTP tests)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Parent REQ:** 51 FLOW; INDEX **D-SSR-8**
- **Decision:** INDEX **D-SSR-8**
- **decision_ref:** backlog SSR-17 + INDEX **D-SSR-8**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config/STORY-GW-SSR-16-node-active-schema-config.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000074-20260830-gw-ssr-17-intake-active-schema-gate.yaml`](../../../../gateway-active-packages/pkg-000074-20260830-gw-ssr-17-intake-active-schema-gate.yaml)
- **Git:** только `semantic-schema-runtime` — [node-schema Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md)
- **Зависит от:** SSR-16 ([pipeline](../STORY-GW-SSR-16-node-active-schema-config/STORY-GW-SSR-16-node-active-schema-config.md))
- **Scaffolded:** 2026-08-30T14:37:24Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 FLOW | INDEX **D-SSR-8** |
| Decision | INDEX **D-SSR-8** | нет/mismatch binding → 4xx; match → validate активного pack |

- **Разблокирует:** G17 → SSR-18 (cluster). **Not** SSR-06/07/12 this pkg.
- **Не reopen:** SSR-01…05 / 08–16 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; `POST /node/issues`; bullrun §«Актуальная точка»

## Nested tasks (pkg-000074)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-17-t01-parse-require-binding`](./task-gw-ssr-17-t01-parse-require-binding/README.md) |
| T02 | [`task-gw-ssr-17-t02-match-active-pair`](./task-gw-ssr-17-t02-match-active-pair/README.md) |
| T03 | [`task-gw-ssr-17-t03-validate-active-pack`](./task-gw-ssr-17-t03-validate-active-pack/README.md) |
| T04 | [`task-gw-ssr-17-t04-tests`](./task-gw-ssr-17-t04-tests/README.md) |
| T05 | [`task-gw-ssr-17-t05-story-acceptance-gate`](./task-gw-ssr-17-t05-story-acceptance-gate/README.md) |
| T06 | [`task-gw-ssr-17-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-17-t06-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Клиент больше не выбирает pack. Новый intake проходит, только если `schema_binding.schema_id` и `schema_binding.schema_version` **ровно** равны `NODE_SCHEMA_*` из конфига. Нет ключа, `{}`, другой pack — **4xx**, не civic.

## Scope / Out of scope

**In:** stash + submit: [`contracts.py`](../../../../../../src/core/intake/contracts.py) `_parse_schema_binding_block` (`:227–263`; сейчас empty/`null` = civic None) и [`services.py`](../../../../../../src/core/application/services.py) `create_story` (`:239–260`). Нет binding / mismatch → `IntakeValidationError`. Совпадение → `validate` payload **активного** pack (`resolve_pack` той же пары). HTTP 4xx envelope. Адаптировать gateway pytest, которые шлют civic envelope **без** binding через TestClient / smoke canvas (req24, e2e sandbox, `tests/smoke` intake ls02/ls03, `test_gw_ssr_03` civic-absent, и grep `schema_binding` отсутствующих POST). Env в фикстурах = SSR-16 helper. Не `live_integration` как proof.

**Out:** GPT UI / instruction pack (REQ-45). Pulse/Emerging семантика. `POST /node/issues` (это Issue create, не story envelope). Удаление civic engine.

**Сеам GPT:** без emit `schema_binding` с id **этой** ноды прод-intake из GPT сломается. В AC стори — факт; правка GPT UI **не** эта реализация.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-17 pkg-000074):** absent / `{}` / null → `IntakeValidationError` 4xx | [`contracts.py:227–241`](../../../../../../src/core/intake/contracts.py), `:480–482` |
| **As-of-Done:** match `NODE_SCHEMA_*` → `resolve`/`validate` **active** pack; mismatch → 4xx | [`services.py:249–271`](../../../../../../src/core/application/services.py) |
| Stash копирует binding на submit (same parse) | [`contracts.py:585`](../../../../../../src/core/intake/contracts.py) |
| Civic HTTP без binding → 4xx; fixtures adapted (binding + env) | G17 `test_gw_ssr_17_*` + `test_gw_ssr_03_*` 22 passed |
| **Historical (pre-SSR-17):** Binding optional; `{}` / null → None civic; validate only if binding present; civic HTTP без binding зелёный | same paths pre-P3 |

## Стыковка

Не silent coerce чужого pack на активный. Не подставлять активный id, если клиент его не прислал.

Stash без binding тоже 4xx (тот же parse).

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Parse | Absent / `{}` / null → IntakeValidationError | Civic None |
| **T02** | Match | id+version == AppConfig; иначе 4xx | Rewrite payload schema_id |
| **T03** | Validate | payload против **активного** pack | Validate чужого pack.json |
| **T04** | Tests | reject absent/mismatch; accept match; адаптировать civic HTTP fixtures | live_integration proof |
| **T05** | Gate | civic HTTP без binding 4xx; match 202; mismatch 4xx | |

## Target / AC

- [x] Нет `schema_binding` / empty object → 4xx, Story не сохраняется civic.
- [x] Другой `schema_id` или `schema_version` → 4xx.
- [x] Совпадение с `NODE_SCHEMA_*` → validate + persist binding.
- [x] Существующие HTTP-тесты intake без binding зелёные **после** адаптации (binding + env), не «skip всех».
- [x] GPT UI files не в diff.

## Dependencies

- SSR-16. Clustering skip — SSR-18.
