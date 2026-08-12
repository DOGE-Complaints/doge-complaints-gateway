# Taxonomy fidelity (persist без потерь + clustering) — backend story package · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/taxonomy-fidelity/`
**Тип:** backlog (постановки; глубина — при активации).
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — факты по фактическому коду, пути указаны.
**Эпик-дом (gateway):** `EPIC-M2-23-taxonomy-fidelity`.

## Контекст одной фразой
GPT извлекает богатую **13-осевую** таксономию (§12-24 [функц-описания GPT](../../../../../GPT%20UI/docs/analysis/DOGEstonia-Custom-GPT-Functional-Description-for-Marketing-Agent.md)), но шлёт её **плоским списком**, а gateway пере-угадывает ось словарями (лоссово) → часть меток **resolve to `unknown`** (§33) и не участвует в кластеризации. Пакет закрывает: (1) хранить без потерь с **точно замапленной** осью; (2) использовать в **кластеризации**.

## SSOT решений
- **Интервью 2026-07-13:** [`interview-taxonomy-persistence-clustering-2026-07-13.md`](../../../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md) — решения **D-TAX-1..4**. Стори ссылаются на него в моментах решений.
- **Gap-источник:** функц-описание GPT §12-24 (оси), §33 (GPT vs Gateway).

## Целевое состояние (D-TAX)
```
GPT per-axis → intake accepts {axis:[{label,disposition}]} → story_labels(story_id,axis,label,disposition)
   → public read-filter (internal никогда не на карточке) → clustering: composite-primary `civic_domain+failure_pattern` + оси service_object/deep_need/ecosystem_signal, пороги по-линзово (D-CLUST)
```

## Стори пакета

| Order | Story | Цель | Решения | Status |
|-------|-------|------|---------|--------|
| 1 | [GW-TAX-01 — Taxonomy persistence fidelity](./STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) → [pipeline](../../epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) | **Цель 1** (не терять + точно замаплено) | D-TAX-1/2/3 | 🔵 Done (Awaiting Commits) pkg-000054 |
| 2 | [GW-TAX-02 — Clustering axis expansion](./STORY-GW-TAX-02-clustering-axis-expansion.md) → [pipeline](../../epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-02-clustering-axis-expansion/STORY-GW-TAX-02-clustering-axis-expansion.md) | **Цель 2** (в кластеризации) | D-CLUST-1..4 (уточняет D-TAX-4) | 🔵 Done (gate PASS 2026-07-15 pkg-000055) |
| 3 | [GW-TAX-03 — Align story_labels migration text FK](./STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) → [pipeline](../../epics/EPIC-M2-23-taxonomy-fidelity/stories/STORY-GW-TAX-03-align-story-labels-migration-text-fk/STORY-GW-TAX-03-align-story-labels-migration-text-fk.md) | Migration SSOT hygiene (UUID→text) | elegance debt G1 | 🔵 Done (Awaiting Commits) pkg-000058 · P6 audit T06–T08 Done (`run_mode=gw_tax_03_audit_followup`) |
| 4 | [GW-TAX-04 — ALTER story_labels UUID residual hosts](./STORY-GW-TAX-04-alter-story-labels-uuid-residual-hosts.md) | Ops successor ALTER if UUID table already applied | TAX-03 audit G2 | ⏸ Deferred |

**Progress:** active product **2/2 Done (100%)**; TAX-03 **Done** (pkg-000058) — repo `migrations/20260714_…` text FK + RLS; dual-path closed. TAX-04 Deferred (residual UUID hosts). Fresh-host: apply `supabase/migrations/` as-is for `story_labels`. End-to-end fidelity гейтится **GPT-TAX-01** (GPT UI). Hosted DDL was DRAFT-07 (not reopened).

## Кросс-репо зависимость (producer-side)
- **GPT-TAX-01** (репо **GPT UI**, пакет [`taxonomy-contract`](../../../../../GPT%20UI/docs/tasks/backlog-stories/taxonomy-contract/INDEX.md)) — GPT OpenAPI + инструкции отдают per-axis таксономию. **Предпосылка GW-TAX-01** (D-TAX-1). Отслеживается в GPT UI backlog, не в gateway-счётчике.

## Verified-факты (по коду gateway, post GW-TAX-01 pkg-000054)
- Приём: `narrative.taxonomy` per-axis ([intake/contracts.py:316](../../../../src/core/intake/contracts.py#L316)) + legacy flat `canonical_labels` fallback; ось из контракта via [`story_labels_from_narrative`](../../../../src/core/taxonomy/story_labels.py).
- Хранение: таблица/port `story_labels(story_id,axis,label,disposition)` — 3 адаптера (sqlite [db_sqlite.py:378](../../../../src/core/infrastructure/db_sqlite.py#L378), supabase, in-memory); persist on save ([services.py:299](../../../../src/core/application/services.py#L299)).
- Public read-filter: `canonical`-only ([disposition.py:16](../../../../src/core/taxonomy/disposition.py#L16)); applied on card-build ([extraction_policy.py:44](../../../../src/core/projection/extraction_policy.py#L44)).
- Legacy: flat labels → `legacy_flat_labels_to_story_labels` / `infer_axis_for_flat_label`; end-to-end per-axis value gated on **GPT-TAX-01** (producer).
- Кластеризация (**post GW-TAX-02 pkg-000055**): primary-линза = **composite** `civic_domain+failure_pattern` ([`composite_primary_cluster_key`](../../../../src/core/cluster/engine.py#L90), default `CLUSTER_PRIMARY_LENS=composite_primary_micro`); `SignalDimension` включает `service_object`/`ecosystem_signal` ([contracts.py:191](../../../../src/core/domain/contracts.py#L191)); новые линзы + `deep_need→NEED` ([engine.py:66](../../../../src/core/cluster/engine.py#L66)); per-lens `CLUSTER_MIN_SIZE_BY_LENS` (composite=8); источник сигналов из `story_labels` per-axis ([enrichment.py:87](../../../../src/core/profile/enrichment.py#L87)) с legacy-fallback. Богатые оси инертны end-to-end до **GPT-TAX-01** (в fallback `service_object`/`need`/`ecosystem_signal`=`unknown`).
- SSOT runtime/audit: pipeline story + [`audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md`](../../../analysis/audit-gw-tax-01-taxonomy-persistence-fidelity-2026-07-14.md).

## Границы пакета
- **In scope:** gateway intake-контракт (приём per-axis), хранение `story_labels`, public read-filter, расширение кластеризации; **TAX-03** — migration SSOT hygiene (text FK).
- **Кросс-репо:** GPT-контракт — GPT UI (GPT-TAX-01), producer-side.
- **НЕ трогаем:** identity.

## Порядок
GPT-TAX-01 (GPT UI) → **GW-TAX-01** → **GW-TAX-02** → hosted DDL [GW-DRAFT-07](../story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) → **GW-TAX-03** Done (repo migration text FK SSOT) → **GW-TAX-04** Deferred (ALTER residual UUID hosts only if needed).

## Hygiene / audits
- Elegance (DRAFT-07 debt → TAX-03 **Closed** 2026-08-07): [`audit-gw-draft-07-architectural-elegance-2026-08-07.md`](../../../analysis/audit-gw-draft-07-architectural-elegance-2026-08-07.md)
- TAX-03 execution audit 2026-08-07: [`audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md`](../../../analysis/audit-gw-tax-03-align-story-labels-migration-text-fk-2026-08-07.md) — P6 Done T06–T08 (`run_mode=gw_tax_03_audit_followup`); [`run-summary-audit`](../../run-reports/run-summary-20260807-1030-gw-tax-03-audit-p6.md)
