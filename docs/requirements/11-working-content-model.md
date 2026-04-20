# 11. Рабочая content-модель

## Story Layer
- original narrative;
- normalized narrative;
- language/location hint/affected object;
- emotional meaning/deep need/desired state;
- public relevance/repeatability signal.

## Story Intelligence Layer
- topic framing;
- system-failure framing;
- needs + desired-state framing;
- suggested institutional relevance;
- cluster eligibility markers.

## Cluster Layer
- lens/scope/narrative;
- dominant patterns;
- evidence volume;
- issue-readiness markers.

## Distinct Issue Layer
- dashboard-ready title;
- summary + full description;
- type + labels + institution (optional);
- creation timestamp + evidence linkage.

## Evidence Layer
- story references;
- supporting materials;
- cluster snapshot;
- issue snapshot;
- tokenization readiness marker.

## CTO notes по модели
- отдельно хранить immutable narrative и mutable интерпретации;
- вводить version_id для signal/profile и cluster lenses;
- обеспечить полную lineage-трассу между слоями.
