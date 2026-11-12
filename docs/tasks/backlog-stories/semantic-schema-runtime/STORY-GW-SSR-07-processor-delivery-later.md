# STORY-GW-SSR-07 — Generic / optional processor delivery (post-T-wave Draft)

## Meta
- **Key:** `STORY-GW-SSR-07-processor-delivery-later`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 📝 **Draft (post-T-wave refine)** — sequence **7** (последняя в пакете). Не T-wave close. Доработать после основного скоупа и после refine SSR-06.
- **Приоритет:** ⚪ LOW — later 51 / parent §33.2
- **Тип:** implement (processors) — **не активировать** до refine
- **Parent REQ:** 51 §4.7, §5 item 12; AC-009/010; SEC-003
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](./orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-01; refine **после** SSR-08…15 и **после** SSR-06 (порядок конца очереди; не overnight post-T-wave)

## Зачем простыми словами

Черновик later-51: generic processor + optional registered processor, который при падении не уничтожает Story. Сейчас постановка тонкая — **обязательно refine** после T-wave. Не закрывает REQ-51 T-wave (AC-018).

## Scope / Out of scope

**In when refined/activated:** schema with no custom processor works via Generic Schema Processor (AC-009); registered optional processor; failure MUST NOT destroy original Story (AC-010); SEC-003 trust id.

**Out now:** WASM; untrusted remote schema auto-executing processors; T-wave delivery; identity (**D-SSR-3**).

## Verified current state

| Fact | Ref |
|------|-----|
| `src/core/schema/` processor pipeline | **Not found** (Glob/Grep) |
| Intake success path | [`StoryIntakeService`](../../../../src/core/application/services.py) persist story **до** gpt_signals ([`:298`](../../../../src/core/application/services.py) vs [`:390`](../../../../src/core/application/services.py)) — Story уже saved; processor later должен быть **после** accept, failure не `delete_story` |
| SEC-003 | нет registry trusted processor ids в src |

## Стыковка (inventory, не execute)

Честный вывод: процессоров нет. T-wave **не** должен их «почти» сделать. AC-010 later = failure isolation относительно **уже persisted** Story (intake уже так делает для gpt_signals fail → warning, story остаётся [`services.py:126`](../../../../src/core/application/services.py) pattern).

Нельзя закрыть AC-009 иллюзией «Generic Processor = validate()». Validate ≠ processor delivery.

## Подзадачи (только refine-inventory — не P3)

| ID | Слой | Задача | Не делать сейчас |
|----|------|--------|------------------|
| **R1** | Boundary | Processor id registry + config allowlist (SEC-003). | WASM / remote auto-exec |
| **R2** | Isolation | Fail processor → Story row intact (`get_story` still binding). | delete on enrich fail |
| **R3** | Generic | Что считается Generic Schema Processor vs SSR-01 validate. | Притворяться что T-wave закрыл PROC |

## Target / AC (после refine)

- [ ] AC-GW-REQ3-08 / AC-009/010 when processors are in the wave
- [ ] Refine pass: trust registry, failure isolation tests (§29 Failure: unavailable optional processor)

## Границы

- **Не** T-wave sequence 1–5.
- **Всегда** последняя в порядковом процессе пакета (после SSR-06).

## Условие refine / активации

- T-wave SSR-01…05 Done и SSR-06 refined **или** явная команда оператора.
- Иначе остаётся Draft; T-wave close от этой стори не зависит.
