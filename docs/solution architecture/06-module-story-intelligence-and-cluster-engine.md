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
