"""D-S1 in-memory text match for public issue list (parity spa issueSearchMatch.js)."""

from __future__ import annotations

from typing import Any

# SPA LOCALE_CODES order: et, ru, en (spa-app/src/i18n/core.js).
LOCALE_CODES: tuple[str, ...] = ("et", "ru", "en")


def collect_localized_field_text(field: object) -> list[str]:
    """Collect non-empty locale strings from LocalizedText or plain string."""
    if field is None:
        return []
    if isinstance(field, str):
        trimmed = field.strip()
        return [field] if trimmed else []
    if not isinstance(field, dict):
        return []
    parts: list[str] = []
    for code in LOCALE_CODES:
        value = field.get(code)
        if isinstance(value, str) and value.strip():
            parts.append(value)
    return parts


def collect_issue_searchable_text(issue: dict[str, Any] | object) -> str:
    """Concatenate et+ru+en title and description (SPA collectIssueSearchableText)."""
    if isinstance(issue, dict):
        title = issue.get("title")
        description = issue.get("description")
    else:
        title = getattr(issue, "title", None)
        description = getattr(issue, "description", None)
    parts = collect_localized_field_text(title) + collect_localized_field_text(
        description
    )
    return " ".join(parts)


def issue_matches_search_query(issue: dict[str, Any] | object, query: object) -> bool:
    """Case-insensitive substring match; empty/whitespace query → match all (D-S1)."""
    normalized = query.strip() if isinstance(query, str) else ""
    if not normalized:
        return True
    haystack = collect_issue_searchable_text(issue).lower()
    return normalized.lower() in haystack
