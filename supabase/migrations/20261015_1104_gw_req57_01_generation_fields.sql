-- GW-REQ57-01: Issue generation lifecycle fields on doge_issues (DP5 — no job table)
ALTER TABLE doge_issues ADD COLUMN IF NOT EXISTS generation_status text;
ALTER TABLE doge_issues ADD COLUMN IF NOT EXISTS generation_version text;
ALTER TABLE doge_issues ADD COLUMN IF NOT EXISTS poster_url text;
ALTER TABLE doge_issues ADD COLUMN IF NOT EXISTS generation_reason_class text;
