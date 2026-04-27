-- Embedding pipeline policy versioning for story/issue vectors.

ALTER TABLE IF EXISTS story_embeddings
    ADD COLUMN IF NOT EXISTS embedding_policy_version TEXT NOT NULL DEFAULT 'm2.story_embedding_policy.v1';

ALTER TABLE IF EXISTS spa_issue_projection_embeddings
    ADD COLUMN IF NOT EXISTS embedding_policy_version TEXT NOT NULL DEFAULT 'm2.issue_embedding_policy.v1';
