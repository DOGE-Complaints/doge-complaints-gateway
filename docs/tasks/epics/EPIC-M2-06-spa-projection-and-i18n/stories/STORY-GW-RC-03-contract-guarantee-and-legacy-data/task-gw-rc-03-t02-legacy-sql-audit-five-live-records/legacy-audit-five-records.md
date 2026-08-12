# Legacy audit — five live records (GW-RC-03 T02)

**Date:** 2026-05-29  
**Source:** [`report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md) — 5 issues in live Supabase snapshot.

## Audit SQL (run against target `doge_issues`)

```sql
SELECT
  issue_id,
  status AS column_status,
  created_at,
  payload_json::jsonb ? 'id' AS payload_has_id,
  payload_json::jsonb ? 'status' AS payload_has_status,
  payload_json::jsonb ->> 'type' AS payload_type_raw,
  payload_json::jsonb ? 'institution' AS payload_has_institution,
  payload_json::jsonb ? 'geo' AS payload_has_geo,
  payload_json::jsonb ? 'original_locale' AS payload_has_original_locale,
  payload_json::jsonb ? 'arweave_txid' AS payload_has_arweave_txid,
  payload_json::jsonb ? 'image_txid' AS payload_has_image_txid,
  payload_json::jsonb ? 'image_hash' AS payload_has_image_hash
FROM doge_issues
ORDER BY created_at DESC
LIMIT 5;
```

SQLite variant: replace `payload_json::jsonb` with `json_extract(payload_json, '$.<key>') IS NOT NULL`.

## Findings (from verified live snapshot + code facts)

| Field | Live legacy (5 records) | Read-path after RC-01/02 | Gap type |
|-------|-------------------------|--------------------------|----------|
| `id` | missing in payload | column merge → present in API | closed (RC-01) |
| `status` | missing in payload | column merge → present in API | closed (RC-01) |
| `type` | lowercase `improvement` | canonicalized → `IMPROVEMENT` | closed (RC-02) |
| `institution` | missing in payload | pass-through from payload if present | data-only |
| `geo` | missing in payload | pass-through from payload if present | data-only |
| `original_locale` | missing in payload | pass-through from payload if present | data-only |
| `arweave_txid` / `image_txid` / `image_hash` | missing in payload | pass-through from payload if present | data-only |

**Conclusion:** Dashboard blocker fields (`id`, `status`, canonical `type`) are guaranteed on read by RC-01/02 + T01 contract tests. Optional legacy enrichment fields remain **data-only** — read-path already returns them when present in payload ([`dto.py:37-50`](../../../../../../../src/core/projection/dto.py#L37-L50)).

## Backfill decision

| Decision | **`defer`** |
|----------|-------------|
| Rationale | D-RC-3: read-path resilient without DB migration; fields appear on next re-project ([`interview-issues-read-contract-2026-06-19.md`](../../../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) §4) |
| T03 gate | **Skip / N/A** — no mandatory backfill in this wave |
