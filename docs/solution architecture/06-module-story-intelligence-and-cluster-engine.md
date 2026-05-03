# 06. Module: Story Intelligence & Cluster Engine

## Responsibilities
- Извлечение signal profile из story.
- Многолинзовая кластеризация (dynamic views).
- Управление cluster readiness и narrative explanation.
- Обеспечение explainability для review.

## Signal profile dimensions
- topic framing
- geo/space context
- system-failure type
- deep need
- desired state
- repeatability/public relevance

## Cluster engine model
- multi-membership story <-> cluster;
- multi-scale clusters: micro/local/systemic;
- lens versioning (`cluster_lens_version`);
- recalculation support (no permanent “truth cluster”).

## Outputs
- `cluster_view` (runtime or materialized snapshot);
- `cluster_narrative` (human-readable meaning);
- `issue_readiness_score`.

## Reviewability
- why-in-cluster explanation per story;
- top contributing signals;
- split/merge/reframe action hooks.

## Детальное техническое решение

Полная SA-проработка вынесена в `cluster-engine/` subdirectory:

- `cluster-engine/00-overview-and-decisions.md` — архитектурный обзор, keep/redesign table, ADRs
- `cluster-engine/01-data-model-and-contracts.md` — типы, протоколы, схема БД
- `cluster-engine/02-signal-extraction.md` — извлечение сигналов из GPT canonical labels
- `cluster-engine/03-engine-and-orchestrator.md` — ClusteringEngine, orchestrator, lifecycle
