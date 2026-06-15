from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

_I18N_LANGS: tuple[str, ...] = ("et", "ru", "en")


@dataclass(frozen=True)
class I18nText:
    """SPA text bundle `{ et, ru, en }` (required for issue card fields)."""

    et: str
    ru: str
    en: str

    def as_dict(self) -> dict[str, str]:
        return {"et": self.et, "ru": self.ru, "en": self.en}


def i18n_text_from_optional_dict(
    source: Mapping[str, str] | None,
    *,
    fallback_text: str,
) -> I18nText:
    """Map optional per-locale dict to I18nText; empty slots use fallback string."""
    fallback = i18n_text_from_plain_text(fallback_text)
    if source is None:
        return fallback
    has_any = any(
        isinstance(source.get(lang), str) and str(source.get(lang)).strip()
        for lang in _I18N_LANGS
    )
    if not has_any:
        return fallback
    return I18nText(
        et=_locale_or_fallback(source, "et", fallback.et),
        ru=_locale_or_fallback(source, "ru", fallback.ru),
        en=_locale_or_fallback(source, "en", fallback.en),
    )


def i18n_text_from_plain_text(text: str) -> I18nText:
    normalized = text.strip()
    if not normalized:
        normalized = "Issue details pending clarification"
    return I18nText(et=normalized, ru=normalized, en=normalized)


def _locale_or_fallback(source: Mapping[str, str], lang: str, fallback: str) -> str:
    raw = source.get(lang)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return fallback
