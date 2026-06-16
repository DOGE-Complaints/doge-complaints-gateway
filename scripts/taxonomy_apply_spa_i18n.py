#!/usr/bin/env python3
"""Apply SPA i18n patches from taxonomy manifest (TC5). Edits spa-app from gateway repo script."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.taxonomy.cycle_lib import decisions_from_manifest, parse_decisions_yaml  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DICTIONARIES = _REPO_ROOT / "spa-app/src/i18n/dictionaries.js"
_LABEL_KEYS = _REPO_ROOT / "spa-app/src/i18n/labelKeys.js"
_LOCALES = ("et", "ru", "en")


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


def _default_translations(spa_label: str) -> dict[str, str]:
    return {
        "et": f"TODO: product copy ({spa_label})",
        "ru": f"TODO: product copy ({spa_label})",
        "en": _title_case(spa_label),
    }


def _ensure_label_in_block(block: str, spa_label: str, translation: str) -> str:
    pattern = re.compile(rf"(\s+{re.escape(spa_label)}:\s*)'[^']*'")
    if pattern.search(block):
        return block
    insert_at = block.rfind("\n    },")
    if insert_at < 0:
        insert_at = block.rfind("\n    }")
    if insert_at < 0:
        raise ValueError("Cannot locate labels block closing brace.")
    line = f"\n      {spa_label}: '{translation.replace(chr(39), '')}',"
    return block[:insert_at] + line + block[insert_at:]


def _patch_dictionaries(text: str, spa_label: str, translations: dict[str, str]) -> str:
    for locale in _LOCALES:
        locale_pattern = re.compile(
            rf"({locale}:\s*\{{[\s\S]*?labels:\s*\{{)([\s\S]*?)(\n\s*\}},)",
            re.MULTILINE,
        )
        match = locale_pattern.search(text)
        if not match:
            raise ValueError(f"Cannot locate labels block for locale {locale!r}.")
        prefix, body, suffix = match.groups()
        translation = translations.get(locale) or _default_translations(spa_label)[locale]
        new_body = _ensure_label_in_block(body, spa_label, translation)
        replacement = prefix + new_body + suffix
        text = text[: match.start()] + replacement + text[match.end() :]
    return text


def _patch_label_keys(text: str, spa_label: str) -> str:
    if spa_label in text:
        return text
    marker = "export const AVAILABLE_LABELS = Object.freeze(["
    start = text.find(marker)
    if start < 0:
        raise ValueError("Cannot locate AVAILABLE_LABELS in labelKeys.js.")
    close = text.find("])", start)
    if close < 0:
        raise ValueError("Cannot locate end of AVAILABLE_LABELS array.")
    insertion = f"\n  '{spa_label}',"
    return text[:close] + insertion + text[close:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply SPA taxonomy i18n manifest (TC5).")
    parser.add_argument("--manifest", required=True, type=Path, help="taxonomy-decisions.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Print planned edits without writing.")
    args = parser.parse_args()
    data = parse_decisions_yaml(args.manifest.read_text(encoding="utf-8"))
    decisions = decisions_from_manifest(data)

    dict_text = _DICTIONARIES.read_text(encoding="utf-8")
    keys_text = _LABEL_KEYS.read_text(encoding="utf-8")
    applied = 0

    for decision in decisions:
        if decision.action not in ("translate_only", "new_board_label"):
            continue
        spa_label = decision.spa_label or decision.target_label or decision.label_key
        translations = decision.translations or _default_translations(spa_label)
        dict_text = _patch_dictionaries(dict_text, spa_label, translations)
        if decision.action == "new_board_label":
            keys_text = _patch_label_keys(keys_text, spa_label)
        applied += 1

    if applied == 0:
        print("No SPA i18n apply actions in manifest.")
        return

    if args.dry_run:
        print(f"Dry-run: would apply {applied} SPA i18n decision(s).")
        return

    _DICTIONARIES.write_text(dict_text, encoding="utf-8")
    _LABEL_KEYS.write_text(keys_text, encoding="utf-8")
    print(f"Applied {applied} SPA i18n decision(s) → dictionaries.js + labelKeys.js.")


if __name__ == "__main__":
    main()
