-- REQ-38 GAP-38-03: index for story_id lookups on issue_story_links
CREATE INDEX IF NOT EXISTS idx_issue_story_links_story ON issue_story_links(story_id);
