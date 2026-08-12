# Story acceptance gate — STORY-GW-DRAFT-07

- **Story:** Hosted schema blocks browser submit
- **Package:** `pkg-000056-20260806-gw-draft-07-hosted-schema-blocks-browser-submit.yaml`
- **Result:** PASS
- **Date:** 2026-08-07T07:04:17Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `GET https://dogestonia-tallinn.up.railway.app/ready` → `db.ready: true`, `checks.schema: true`. | PASS | T04; ready `trace_id` `35bdafee-34c4-4eb3-af1f-58a26bb30277` |
| Verified user + filled draft: Submit → **202** (не 503 `service_down` на happy path). | PASS | T05; submit `62e65b0a-…` / `24525dad-…` |
| Повторный Submit того же consumed draft — idempotent **202** + same `story_id` (без ложной второй публикации); GET draft → **404**. | PASS | T05; as-built [`handlers.py:656-713`](../../../../../../../../src/core/api/handlers.py) `_story_intake_replay_from_idempotency`; GET draft → **404** |
| Evidence artifact в `doge-complaints-gateway/docs/analysis/` (sanitized ready JSON + submit 202 trace_id) после Done. | PASS | [`evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md`](../../../../../../analysis/evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md) |
| FE-HANDOFF-03 / SPA-BUG-01 могут закрыть regression на новом draft после этого Done. | PASS | Root cause cleared (`schema=true`); SPA retest unblocked — no FE hotfix required |

## Commands (live verification 2026-08-07)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
curl -sS https://dogestonia-tallinn.up.railway.app/ready | python3 -m json.tool
# Stash (service token) + submit (verified user Bearer) → 202; retry same draft_id → 202 same story_id; GET draft → 404
```

**Live run:** verify ok 6 paths; `/ready` ready+schema true; DDL `draft_07_story_labels_text_fk`; redeploy `66629cac-…` SUCCESS; submit 202 + idempotent retry.

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
