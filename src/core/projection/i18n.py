from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class I18nText:
    """SPA text bundle `{ et, ru, en }` (required for issue card fields)."""

    et: str
    ru: str
    en: str

    def as_dict(self) -> dict[str, str]:
        return {"et": self.et, "ru": self.ru, "en": self.en}
