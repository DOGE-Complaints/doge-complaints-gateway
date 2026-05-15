"""Helpers for multilingual narrative fields (REQ-33 v2)."""

from __future__ import annotations

import json
from typing import Any, Mapping

I18N_LANGS: tuple[str, ...] = ("et", "ru", "en")


def parse_required_i18n_dict(
    payload: Mapping[str, Any],
    *,
    field_name: str,
    parent: str = "narrative",
) -> dict[str, str]:
    if not isinstance(payload, Mapping):
        raise ValueError(
            f"Missing or invalid {parent}.{field_name}. Expected object with et/ru/en string values."
        )
    result: dict[str, str] = {}
    for lang in I18N_LANGS:
        raw = payload.get(lang)
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"Missing or invalid {parent}.{field_name}.{lang}.")
        result[lang] = raw.strip()
    return result


def parse_optional_i18n_dict(
    payload: Any,
    *,
    field_name: str,
    parent: str = "narrative",
) -> dict[str, str] | None:
    if payload is None:
        return None
    if not isinstance(payload, Mapping):
        raise ValueError(
            f"Missing or invalid {parent}.{field_name}. Expected object with et/ru/en string values."
        )
    return parse_required_i18n_dict(payload, field_name=field_name, parent=parent)


def i18n_dict_to_json(value: dict[str, str] | None) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def i18n_dict_from_json(raw: str | None) -> dict[str, str] | None:
    if raw is None or not str(raw).strip():
        return None
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object for i18n narrative field.")
    return {str(k): str(v) for k, v in parsed.items()}


def primary_i18n_text(
    texts: dict[str, str],
    *,
    session_language: str | None,
    fallback_language: str | None,
) -> str:
    if session_language and session_language in texts:
        return texts[session_language]
    if fallback_language and fallback_language in texts:
        return texts[fallback_language]
    for lang in I18N_LANGS:
        if texts.get(lang):
            return texts[lang]
    return ""


def story_primary_title(
    *,
    narrative_title: dict[str, str] | None,
    narrative_session_language: str | None,
    narrative_language: str | None,
) -> str:
    if not narrative_title:
        return ""
    return primary_i18n_text(
        narrative_title,
        session_language=narrative_session_language,
        fallback_language=narrative_language,
    )


def narrative_v2_complete(
    *,
    original_text: str,
    language: str,
    title: dict[str, str],
    description: dict[str, str],
    session_language: str,
) -> bool:
    return bool(
        original_text.strip()
        and language.strip()
        and session_language.strip()
        and all(title[lang].strip() for lang in I18N_LANGS)
        and all(description[lang].strip() for lang in I18N_LANGS)
    )
