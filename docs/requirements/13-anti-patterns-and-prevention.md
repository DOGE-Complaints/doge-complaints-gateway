# 13. Anti-patterns и их предотвращение

## AP-01: Instant collapse story -> ticket
- **Симптом:** потеря narrative.
- **Профилактика:** обязательный story-layer до любой issue-проекции.

## AP-02: Flat dedup by words
- **Симптом:** ложные склейки разных проблем.
- **Профилактика:** multi-signal matching + human review на пограничных кейсах.

## AP-03: Rigid one-time clusters
- **Симптом:** невозможность переосмыслить corpus.
- **Профилактика:** dynamic views + re-cluster policy.

## AP-04: Issue without evidence
- **Симптом:** карточка без происхождения.
- **Профилактика:** hard rule `no evidence linkage -> no publish`.

## AP-05: Story swamp
- **Симптом:** хранилище растёт, управляемость падает.
- **Профилактика:** readiness pipeline и SLA на перевод в кластеры.

## AP-06: Analytics without humanity
- **Симптом:** “чистая статистика” без гражданского смысла.
- **Профилактика:** narrative summary как обязательный артефакт кластера/issue.

## AP-07: Narrative without governability
- **Симптом:** богатые истории без операционной полезности.
- **Профилактика:** distinct issue promotion framework.

## AP-08: SPA contract bloat
- **Симптом:** поломка UI из-за перегруженной проекции.
- **Профилактика:** zero-change contract gate + optional extensions only.
