-- GW-TAX-01: per-axis taxonomy persistence (D-TAX-2/3)
CREATE TABLE IF NOT EXISTS story_labels (
    story_id UUID NOT NULL REFERENCES stories(story_id) ON DELETE CASCADE,
    axis TEXT NOT NULL,
    label TEXT NOT NULL,
    disposition TEXT NOT NULL,
    PRIMARY KEY (story_id, axis, label)
);

CREATE INDEX IF NOT EXISTS idx_story_labels_story ON story_labels(story_id);
CREATE INDEX IF NOT EXISTS idx_story_labels_axis ON story_labels(axis);
