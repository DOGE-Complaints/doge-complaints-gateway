# STORY-GW-TAX-01 — Taxonomy persistence fidelity (per-axis, без потерь)

## Meta
- **Key:** `STORY-GW-TAX-01-taxonomy-persistence-fidelity`
- **Пакет:** [`taxonomy-fidelity/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — implemented via pipeline pkg-000054 (see SSOT below)
- **Приоритет:** 🟠 MED-HIGH — civic-смысл историй сейчас частично теряется/resolve to unknown
- **Тип:** feature (intake contract + storage + read-filter)
- **Цель:** **Цель 1** — данные GPT не теряются, хранятся с **точно замапленной** таксономией
- **Основание (решения):** [`interview-taxonomy-persistence-clustering-2026-07-13`](../../../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md) — **D-TAX-1** (per-axis от GPT), **D-TAX-2** (таблица `story_labels`), **D-TAX-3** (хранить всё + disposition)
- **Зависит от:** **GPT-TAX-01** (GPT UI — per-axis контракт, producer)
- **Разблокирует:** [GW-TAX-02](./STORY-GW-TAX-02-clustering-axis-expansion.md) (кластеризация по осям)

**SSOT (pipeline):** [`STORY-GW-TAX-01-taxonomy-persistence-fidelity.md`](../../epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) — решения D-TAX-1/2/3 + queue pkg-000054 T01–T08 gate PASS 2026-07-14.

## Зачем простыми словами
GPT понимает историю по 13 смысловым осям (что за сфера, какой объект, какая нужда, какой желаемый исход, …), но сейчас шлёт всё **одной кучей меток**, а gateway **угадывает** ось словарями. Метки, для которых словаря нет, **пропадают из смысла** (хранятся строкой, но «ось = неизвестно»). Нужно принимать таксономию **с осью** и хранить её **точно и полностью**.

## Требование / целевое состояние (D-TAX-1/2/3)
1. **Intake-контракт (D-TAX-1):** принимать per-axis таксономию от GPT — `narrative.taxonomy = {axis: [{label, disposition}]}` (обратная совместимость: плоский `canonical_labels` продолжает приниматься как legacy → axis via fallback-словари).
2. **Хранение (D-TAX-2):** новая таблица `story_labels(story_id, axis, label, disposition)` + порт-репозиторий + адаптеры (in-memory / sqlite / supabase) + миграция. Персист **всех** меток (D-TAX-3).
3. **disposition (D-TAX-3):** `canonical | metadata_only | needs_clarification | rejected | internal` (§13/§24).
4. **Public read-filter (D-TAX-3):** публичные поверхности (`/tallinn/issues` карточки, cabinet) отдают **только** dispositions, разрешённые публично (никогда `internal`; `metadata_only` — по правилу).
5. **Совместимость:** legacy-истории с плоскими метками читаются через существующий `infer_signals_from_canonical` (fallback), не ломаются.

## Что наблюдаю сейчас (verified по коду)
Эта pass-2 постановка **свернута**: факты по реализации и AC ведутся в pipeline SSOT (см. ссылку выше).

## Acceptance Criteria
Реализовано и проверено в pipeline (T01–T08, gate PASS 2026-07-14) — см. SSOT и [`audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md`](../../../analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md).

## Границы
- **In scope:** gateway приём/хранение/read-filter таксономии.
- **Вне scope:** расширение кластеризации → [GW-TAX-02](./STORY-GW-TAX-02-clustering-axis-expansion.md); GPT-контракт → GPT-TAX-01 (GPT UI).
- **Не трогаем:** identity.

## Примечание
Если нужно понять текущий runtime/контракт/тесты — см. pipeline story SSOT и audit:
- `docs/analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md`
