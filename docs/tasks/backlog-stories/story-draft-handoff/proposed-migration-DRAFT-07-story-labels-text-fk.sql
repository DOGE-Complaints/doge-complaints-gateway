-- PROPOSAL for STORY-GW-DRAFT-07 (operator applies in gateway session — not auto-applied).
-- Hosted Public Node (lvfrdtglpksmaywqlohj): gateway /ready checks.schema=false
-- because table story_labels is missing (blocks POST /story-drafts/{id}/submit → 503).
--
-- Why text (not UUID): hosted public.stories.story_id is text
--   (information_schema 2026-08-06). Repo file
--   doge-complaints-gateway/supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql
--   uses UUID and would fail FK on this host. Bootstrap already documents text FK:
--   doge-complaints-gateway/supabase/bootstrap/000_full_init.sql (story_labels).
--
-- After apply: redeploy doge-complaints-gateway (ApiDependencies db_ready is
-- lru_cache'd at process start — schema flip alone does not refresh readiness).

CREATE TABLE IF NOT EXISTS public.story_labels (
    story_id text NOT NULL REFERENCES public.stories(story_id) ON DELETE CASCADE,
    axis text NOT NULL,
    label text NOT NULL,
    disposition text NOT NULL,
    PRIMARY KEY (story_id, axis, label)
);

CREATE INDEX IF NOT EXISTS idx_story_labels_story ON public.story_labels(story_id);
CREATE INDEX IF NOT EXISTS idx_story_labels_axis ON public.story_labels(axis);

ALTER TABLE public.story_labels ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS story_labels_service_role_all ON public.story_labels;
CREATE POLICY story_labels_service_role_all
ON public.story_labels
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

GRANT ALL ON TABLE public.story_labels TO service_role;
GRANT SELECT ON TABLE public.story_labels TO anon, authenticated;
