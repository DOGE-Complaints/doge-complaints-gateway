-- GW-TAX-01: per-axis taxonomy persistence (D-TAX-2/3)
-- GW-TAX-03: align story_id to text FK (SSOT with bootstrap / peer migrations / hosted).
--
-- GUARD: do NOT use UUID for story_labels.story_id on hosts where
-- public.stories.story_id is text — UUID DDL is incompatible and will fail FK
-- (or recreate the readiness hole). Fresh hosts: apply this file as text FK.
-- Public Node (post DRAFT-07) already has text FK via ops DDL — do not re-apply
-- solely for TAX-03.

CREATE TABLE IF NOT EXISTS story_labels (
    story_id text NOT NULL REFERENCES stories(story_id) ON DELETE CASCADE,
    axis TEXT NOT NULL,
    label TEXT NOT NULL,
    disposition TEXT NOT NULL,
    PRIMARY KEY (story_id, axis, label)
);

CREATE INDEX IF NOT EXISTS idx_story_labels_story ON story_labels(story_id);
CREATE INDEX IF NOT EXISTS idx_story_labels_axis ON story_labels(axis);

ALTER TABLE story_labels ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS story_labels_service_role_all ON story_labels;
CREATE POLICY story_labels_service_role_all
ON story_labels
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- GRANT: aligned with proposed DRAFT-07 ops DDL (story-draft-handoff/proposed-migration-…).
-- Bootstrap historically RLS+policy only for story_labels (no GRANT) — GRANT here is
-- proposed-path parity, not bootstrap GRANT sync.
GRANT ALL ON TABLE story_labels TO service_role;
GRANT SELECT ON TABLE story_labels TO anon, authenticated;
