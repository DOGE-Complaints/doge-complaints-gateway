from __future__ import annotations

from core.domain import StoryRecord


def alpha_score(story: StoryRecord) -> float:
    """REQ-36 §2.2: deterministic story quality score (0–100)."""
    score = 0.0

    if story.narrative_canonical_type and story.narrative_canonical_type.strip():
        score += 12.0
    label_count = len(story.narrative_canonical_labels)
    score += min(label_count * 6, 18)

    text_len = len(story.narrative_original_text.strip())
    score += min(text_len / 15.0, 20.0)
    if story.narrative_summary:
        score += 10.0
    if story.narrative_consistency_notes:
        score += 10.0

    if story.geo is not None:
        score += 10.0
        score += story.geo.confidence * 20.0

    return score
