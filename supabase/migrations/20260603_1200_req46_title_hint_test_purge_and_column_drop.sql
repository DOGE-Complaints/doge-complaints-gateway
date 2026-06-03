-- REQ-46 STORY-M2-02-12 T11: purge test stories with legacy narrative_title_hint* data,
-- delete derived doge_issues (any_link policy), then DROP dead columns.
-- DESTRUCTIVE. No DOWN. Operator: confirm hosted DB is test-only before apply.
-- Ref: docs/analysis/req46-t07-narrative-title-hint-gate-unblock-runbook-2026-06-02.md

-- =============================================================================
-- PREFLIGHT (run manually before BEGIN; do not rely on commented counts in CI)
-- =============================================================================
-- SELECT COUNT(*) AS purge_story_count FROM public.stories
-- WHERE narrative_title_hint IS NOT NULL
--    OR narrative_title_hint_et IS NOT NULL
--    OR narrative_title_hint_ru IS NOT NULL
--    OR narrative_title_hint_en IS NOT NULL;
--
-- SELECT COUNT(DISTINCT isl.issue_id) AS purge_issue_count
-- FROM public.issue_story_links isl
-- INNER JOIN public.stories s ON s.story_id = isl.story_id
-- WHERE s.narrative_title_hint IS NOT NULL
--    OR s.narrative_title_hint_et IS NOT NULL
--    OR s.narrative_title_hint_ru IS NOT NULL
--    OR s.narrative_title_hint_en IS NOT NULL;

BEGIN;

CREATE TEMP TABLE _req46_purge_stories ON COMMIT DROP AS
SELECT story_id
FROM public.stories
WHERE narrative_title_hint IS NOT NULL
   OR narrative_title_hint_et IS NOT NULL
   OR narrative_title_hint_ru IS NOT NULL
   OR narrative_title_hint_en IS NOT NULL;

CREATE TEMP TABLE _req46_purge_issues ON COMMIT DROP AS
SELECT DISTINCT isl.issue_id
FROM public.issue_story_links isl
INNER JOIN _req46_purge_stories p ON p.story_id = isl.story_id;

CREATE TEMP TABLE _req46_purge_candidates ON COMMIT DROP AS
SELECT ic.candidate_id
FROM public.issue_candidates ic
WHERE EXISTS (
    SELECT 1
    FROM jsonb_array_elements_text(ic.story_ids_json) AS elem(story_id)
    INNER JOIN _req46_purge_stories p ON p.story_id = elem.story_id
);

-- issue_candidates / audit (no FK to stories)
DELETE FROM public.review_audit_log
WHERE candidate_id IN (SELECT candidate_id FROM _req46_purge_candidates);

DELETE FROM public.issue_candidates
WHERE candidate_id IN (SELECT candidate_id FROM _req46_purge_candidates);

-- issues derived from purge-set stories (any_link)
DELETE FROM public.doge_issue_embeddings
WHERE issue_id IN (SELECT issue_id FROM _req46_purge_issues);

DELETE FROM public.issue_story_links
WHERE story_id IN (SELECT story_id FROM _req46_purge_stories);

DELETE FROM public.doge_issues
WHERE issue_id IN (SELECT issue_id FROM _req46_purge_issues);

-- stories: cascades idempotency_keys, story_embeddings, story_signals, cluster_memberships
DELETE FROM public.stories
WHERE story_id IN (SELECT story_id FROM _req46_purge_stories);

-- Post-purge gate (must be 0 before DROP)
DO $$
DECLARE
    remaining bigint;
BEGIN
    SELECT COUNT(*) INTO remaining
    FROM public.stories
    WHERE narrative_title_hint IS NOT NULL
       OR narrative_title_hint_et IS NOT NULL
       OR narrative_title_hint_ru IS NOT NULL
       OR narrative_title_hint_en IS NOT NULL;
    IF remaining > 0 THEN
        RAISE EXCEPTION 'REQ-46 T11: % stories still have non-null narrative_title_hint*; aborting DROP', remaining;
    END IF;
END $$;

ALTER TABLE public.stories
  DROP COLUMN IF EXISTS narrative_title_hint,
  DROP COLUMN IF EXISTS narrative_title_hint_et,
  DROP COLUMN IF EXISTS narrative_title_hint_ru,
  DROP COLUMN IF EXISTS narrative_title_hint_en;

COMMIT;
