# Decision Points — STORY-M2-02-02

## DP-01: Lifecycle baseline
- Решение: стартовый статус `accepted` через `StoryLifecycleStatus`.
- Причина: intake факт принят, enrichment/cluster этапы еще впереди.

## DP-02: Immutable narrative strategy
- Решение: хранить `narrative_original_text` как отдельное поле `StoryRecord`.
- Причина: защита от forced collapse и потери исходного текста.

## DP-03: Authorship linkage
- Решение: сохранять `submitter_external_user_id` + optional `submitter_identity_issuer`.
- Причина: lineage и трассировка авторства без навязывания формата user id.
