# 05. Module: Story Intake & Story Store

## Responsibilities
- Сохранить story как immutable первичное свидетельство.
- Принять optional structured signals без потери original narrative.
- Поддержать readiness-состояния (partial, cluster-ready, projection-ready).
- Сохранить origin linkage (GPT intake reference, timestamps, version).
- Сохранить **авторство**: `submitter.external_user_id` (opaque, формат не фиксируется) и при необходимости `identity_issuer` из OAuth на стороне GPT/IdP — в `story_origin` или связанной сущности без потери на intake.

## Data model (logical)
- `stories` (immutable narrative core).
- `story_versions` (normalization/enrichment revisions).
- `story_origin` (source metadata + **внешний субъект/автор** при логине через GPT).
- `story_status` (readiness lifecycle).

## Lifecycle states
`accepted` -> `profiled` -> `cluster_eligible` -> `issue_candidate_linked` -> `projected`

## Storage rules
- Original narrative never overwritten.
- Interpretation fields versioned.
- PII fields optional and isolated by classification tier.

## Migration strategy from legacy
- Legacy `complaints` -> `stories` seed migration.
- Mapping table for old IDs to new story IDs.
- Dual-read period for validation.
