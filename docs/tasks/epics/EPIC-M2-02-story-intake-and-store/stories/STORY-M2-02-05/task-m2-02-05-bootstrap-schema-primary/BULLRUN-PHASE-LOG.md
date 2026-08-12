# BULLRUN phase log — STORY-M2-02-05 wave

Окно: `gateway-cursor-build-window--STORY-M2-02-05.md`  
План процесса: `.cursor/plans/Gateway_builder.plan.md` + `m2-epic-story-execution-pipeline.md`

| Phase | Task README | Outcome |
|-------|----------------|---------|
| T01 | `task-m2-02-05-t01-gap-bootstrap-stories-geo-columns` | Geo columns в `000_full_init.sql` + forward migration `20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql` |
| T02 | `task-m2-02-05-t02-gap-bootstrap-embeddings-not-null` | GAP-08 **вариант A**: `embedding` nullable на `story_embeddings` / `doge_issue_embeddings`; README bootstrap обновлён |
| T03 | `task-m2-02-05-t03-gap-jsonb-read-issue-candidates-audit` | `_coerce_jsonb_text_id_sequence` + регрессионные тесты |
| Primary | `task-m2-02-05-bootstrap-schema-primary` | `acceptance-verification-STORY-M2-02-05.md`, story gate, verify + pytest |

Закрытие story-gate: [`../story-acceptance-gate-STORY-M2-02-05.md`](../story-acceptance-gate-STORY-M2-02-05.md).
