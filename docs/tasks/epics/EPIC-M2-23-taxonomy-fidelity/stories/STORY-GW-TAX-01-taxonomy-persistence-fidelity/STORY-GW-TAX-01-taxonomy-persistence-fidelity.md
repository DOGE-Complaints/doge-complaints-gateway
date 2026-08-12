# STORY-GW-TAX-01 — Taxonomy persistence fidelity (per-axis, без потерь)

## Meta
- **Key:** `STORY-GW-TAX-01-taxonomy-persistence-fidelity`
- **Parent Epic:** [`../../../EPIC-M2-23-taxonomy-fidelity.md`](../../../EPIC-M2-23-taxonomy-fidelity.md)
- **Type:** feature (intake contract + storage + read-filter)
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-07-14; [`run-summary`](../../../../run-reports/run-summary-20260714-2055-gw-tax-01-p3.md)
- **Приоритет:** 🟠 MED-HIGH — civic-смысл историй сейчас частично теряется/resolve to unknown
- **Цель:** **Цель 1** — данные GPT не теряются, хранятся с **точно замапленной** таксономией
- **source:** [`../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md`](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Основание (решения):** [`interview-taxonomy-persistence-clustering-2026-07-13`](../../../../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md) — **D-TAX-1** (per-axis от GPT), **D-TAX-2** (таблица `story_labels`), **D-TAX-3** (хранить всё + disposition)
- **Зависит от:** **GPT-TAX-01** (GPT UI — per-axis контракт, producer)
- **Разблокирует:** [GW-TAX-02](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-02-clustering-axis-expansion.md) (кластеризация по осям)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000054-20260714-gw-tax-01-taxonomy-persistence-fidelity.yaml`](../../../../gateway-active-packages/pkg-000054-20260714-gw-tax-01-taxonomy-persistence-fidelity.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **8** тасков T01–T08
- **decision_ref:** backlog + interview D-TAX-1/2/3

## Зачем простыми словами
GPT понимает историю по 13 смысловым осям (что за сфера, какой объект, какая нужда, какой желаемый исход, …), но сейчас шлёт всё **одной кучей меток**, а gateway **угадывает** ось словарями. Метки, для которых словаря нет, **пропадают из смысла** (хранятся строкой, но «ось = неизвестно»). Нужно принимать таксономию **с осью** и хранить её **точно и полностью**.

## Что наблюдаю сейчас (verified по коду)
| Элемент | Реальность |
|---------|-----------|
| Приём | `narrative.canonical_labels` — плоский список ([intake/contracts.py:294](../../../../../../src/core/intake/contracts.py#L294)); осей нет |
| Хранение | `StoryRecord.narrative_canonical_labels` — плоский tuple ([contracts.py:60](../../../../../../src/core/domain/contracts.py#L60)); `story_labels`-таблицы **нет** |
| Маппинг оси | пере-угадывание 5 словарями ([enrichment.py:37](../../../../../../src/core/profile/enrichment.py#L37)); ~8 осей не покрыты → `unknown` (§33) |
| disposition | не хранится (canonical/metadata_only/internal не различаются на записи) |

## Требование / целевое состояние (D-TAX-1/2/3)
1. **Intake-контракт (D-TAX-1):** принимать per-axis таксономию от GPT — `narrative.taxonomy = {axis: [{label, disposition}]}` (обратная совместимость: плоский `canonical_labels` продолжает приниматься как legacy → axis via fallback-словари).
2. **Хранение (D-TAX-2):** новая таблица `story_labels(story_id, axis, label, disposition)` + порт-репозиторий + адаптеры (in-memory / sqlite / supabase) + миграция. Персист **всех** меток (D-TAX-3).
3. **disposition (D-TAX-3):** `canonical | metadata_only | needs_clarification | rejected | internal` (§13/§24).
4. **Public read-filter (D-TAX-3):** публичные поверхности (`/tallinn/issues` карточки, cabinet) отдают **только** dispositions, разрешённые публично (никогда `internal`; `metadata_only` — по правилу).
5. **Совместимость:** legacy-истории с плоскими метками читаются через существующий `infer_signals_from_canonical` (fallback), не ломаются.

## Подзадачи (pipeline queue)
| ID | Task | Type | Status |
|----|------|------|--------|
| T01 | [Intake per-axis taxonomy contract](./task-gw-tax-01-t01-intake-per-axis-taxonomy-contract/README.md) | implement | 🔵 Done |
| T02 | [Domain StoryLabel repository](./task-gw-tax-01-t02-domain-story-label-repository/README.md) | implement | 🔵 Done |
| T03 | [Story label adapters migrations and DI](./task-gw-tax-01-t03-story-label-adapters-migrations-and-di/README.md) | implement | 🔵 Done |
| T04 | [Persist labels on story intake submit](./task-gw-tax-01-t04-persist-labels-on-story-intake-submit/README.md) | implement | 🔵 Done |
| T05 | [Public read-filter by disposition](./task-gw-tax-01-t05-public-read-filter-by-disposition/README.md) | implement | 🔵 Done |
| T06 | [Legacy flat labels fallback compat](./task-gw-tax-01-t06-legacy-flat-labels-fallback-compat/README.md) | implement | 🔵 Done |
| T07 | [Tests per-axis persist read-filter](./task-gw-tax-01-t07-tests-per-axis-persist-read-filter/README.md) | test | 🔵 Done |
| T08 | [Story acceptance gate](./task-gw-tax-01-t08-story-acceptance-gate/README.md) | gate | 🔵 Done |
| T09 | [Audit R1 backlog story sync](./task-gw-tax-01-t09-audit-r1-backlog-story-sync/README.md) | docs | 🔵 Done |

## Acceptance Criteria
- [x] Intake принимает per-axis таксономию; ось **не угадывается**, а берётся из контракта (D-TAX-1)
- [x] Все метки (canonical/metadata_only/internal) персистятся в `story_labels` с disposition (D-TAX-3)
- [x] Public read никогда не отдаёт `internal`-метки (§24)
- [x] Legacy плоские истории не ломаются (fallback)
- [x] Full offline suite green

## Границы
- **In scope:** gateway приём/хранение/read-filter таксономии.
- **Вне scope:** расширение кластеризации → [GW-TAX-02](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-02-clustering-axis-expansion.md); GPT-контракт → GPT-TAX-01 (GPT UI).
- **Не трогаем:** identity.

## Швы
- Приём: [`intake/contracts.py`](../../../../../../src/core/intake/contracts.py); домен: [`domain/contracts.py`](../../../../../../src/core/domain/contracts.py); хранение: [`infrastructure/`](../../../../../../src/core/infrastructure/) (`db_sqlite.py`/`db_supabase.py`/`repositories.py`); persist: [`api/handlers.py`](../../../../../../src/core/api/handlers.py) `handle_story_intake`; read-filter: [`projection/read_filters.py`](../../../../../../src/core/projection/read_filters.py).
