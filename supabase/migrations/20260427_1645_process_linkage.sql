-- Story-first process/linkage persistence: candidates, audit, and issue->stories links.

CREATE TABLE IF NOT EXISTS issue_candidates (
    candidate_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    story_ids_json JSONB NOT NULL,
    readiness_score INTEGER NOT NULL CHECK (readiness_score >= 0 AND readiness_score <= 100),
    title TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS review_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    related_cluster_id TEXT NOT NULL,
    related_story_ids_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_review_audit_candidate ON review_audit_log(candidate_id);

CREATE TABLE IF NOT EXISTS issue_story_links (
    issue_id TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    story_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (issue_id, story_id)
);
CREATE INDEX IF NOT EXISTS idx_issue_story_links_issue ON issue_story_links(issue_id);
