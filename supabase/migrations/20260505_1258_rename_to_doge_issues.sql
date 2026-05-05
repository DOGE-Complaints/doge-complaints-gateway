-- Requirement 27: rename issue projection tables to DOGE domain names.

ALTER TABLE IF EXISTS public.spa_issue_projections
    RENAME TO doge_issues;

ALTER TABLE IF EXISTS public.spa_issue_projection_embeddings
    RENAME TO doge_issue_embeddings;

DROP POLICY IF EXISTS projections_service_role_all ON public.doge_issues;
CREATE POLICY doge_issues_service_role_all
    ON public.doge_issues
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS projection_embeddings_service_role_all ON public.doge_issue_embeddings;
CREATE POLICY doge_issue_embeddings_service_role_all
    ON public.doge_issue_embeddings
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
