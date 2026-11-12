# STORY-GW-SSR-10 — Taxonomy + exact lenses on one bound story (pack-declared)

## Meta
- **Key:** `STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave product (sequence **10**)
- **Тип:** implement (orchestrator + loader contract; первый слой)
- **Parent REQ:** 51 CL; INDEX invariant «не расширять `ClusterLens`»
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](./orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-04, SSR-05

## Зачем простыми словами

Сейчас история с `schema_binding` идёт **только** в pack exact-lens. Ярлыки / civic `ClusterLens` её не видят. Оператор хочет в `pack.json` задать: *и* таксономия (как сейчас у civic), *и* exact по кастомным полям. Это не «добавить член enum».

## Scope / Out of scope

**In:** явный контракт в pack (ключ loader — **refine**, не invent frozen YAML): bound story MAY также получить civic memberships из `story_labels` / `infer_signals_from_canonical`, **и** pack exact-lenses с payload. Civic stories **без** binding не менять. `ClusterLens` enum не расширять. Тесты: dual membership на одном `story_id` (разные `lens` строки; PK `(story_id, lens)` уже TEXT).

**Out:** SSR-08 (это *копия* civic-осей в payload, без civic engine); смена factory `PromotionGatePolicy`; HTTP filter; процессоры; matching lost/found (→ SSR-12).

## Честная развилка (выбрать в refine, не оба как «уже решено»)

| Путь | Что менять | Когда достаточно |
|------|-----------|-------------------|
| **A. Payload-only** | SSR-08: оси в `structured_payload`, только exact | Нода не нужна в civic vocab |
| **B. Dual engine** | Orchestrator: bound ≠ skip civic; pack.json включает civic+exact | Жалоба Tallinn **и** кастомные поля на одной story |

Эта стори = **путь B** (запрос оператора). Путь A уже постановлен в SSR-08; не дублировать execute.

**As-of-Done (pkg-000068 G10):** код пути B **есть** — bound → `_process_bound_story` ([`cluster_orchestrator.py:121–126`](../../../../src/core/application/cluster_orchestrator.py)); civic только если `dual_civic_lenses`. Pack exact по-прежнему payload-only ([`pack_engine.py:100–105`](../../../../src/core/schema/pack_engine.py)).

**Historical (pre-P3):** кода пути B не было: `is_schema_bound` → только `_process_pack_bound_story`; pack не читал labels; loader не парсил dual-ключ.

## Verified current state

| Fact | Ref |
|------|-----|
| Bound fork | [`cluster_orchestrator.py:274–275`](../../../../src/core/application/cluster_orchestrator.py) → `_process_bound_story` |
| Dual opt-in | `_dual_civic_enabled` [`:90–95`](../../../../src/core/application/cluster_orchestrator.py); `SchemaContext.dual_civic_lenses` default False |
| Civic skip bound (unbound pool) | `_civic_ready` исключает schema-bound [`:87–88`](../../../../src/core/application/cluster_orchestrator.py) |
| Pack algorithm | только `exact`; иначе skip [`pack_engine.py:100–101`](../../../../src/core/schema/pack_engine.py) |
| Loader keys | [`schema-packs/README.md:28`](../../../../schema-packs/README.md) optional `dual_civic_lenses` |
| `ClusterLens` | 10 членов [`types.py:10–22`](../../../../src/core/cluster/types.py) |
| Membership PK | `(story_id, lens)` TEXT — civic enum value и pack `lens_id` сосуществуют на одном `story_id` |

## Стыковка

**Запрет:** `ClusterLens.NEW = …`. Civic engine по-прежнему enum.

Имя ключа в `pack.json` (например «также гонять civic lenses») — **не** замораживать в этой стори сверх: таблица в `schema-packs/README.md` после refine (SCHEMA-005: один loader).

Promote: две кучи (civic cluster_id vs `schema:…`) — отдельные candidates. Не смешивать civic `readiness_score_for_cluster` с pack knobs на одном candidate.

Default pack **без** нового ключа = текущее поведение (только exact) — иначе сломается legal_process.

## Подзадачи (первый слой)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **R1** | Contract | Имя+семантика pack-флага dual vs exact-only; default exact-only | Frozen диалект до refine |
| **T01** | Orchestrator | Если pack говорит dual: civic memberships + pack exact на той же story | Всегда civic для любого binding; расширять enum |
| **T02** | Promote | Не гнать pack candidate через civic type-gate as-is; civic candidate — civic policy | Один Issue на оба lens id без решения |
| **T03** | Tests | Unbound civic green; legal_process exact-only green; dual fixture: labels+payload → два вида lens | Прогонять dual через один `cluster_id` |

## Target / AC

- [x] Pack MAY объявить dual; absent/false = T-wave поведение.
- [x] Dual: membership и civic-линз (enum value) и pack `lens_id` на одном `story_id`.
- [x] `ClusterLens` по-прежнему 10.
- [x] Civic без binding зелёный.
- [x] Нет нового HTTP.

## Dependencies

- SSR-04/05 Done. SSR-08 параллелен (путь A), не блокер пути B.
- GPT: dual осмыслен, если labels **и** payload приходят на intake (sibling REQ-45 + существующий taxonomy в envelope).
