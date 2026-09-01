"""SSR-28: section-scoped extract of GPT story-label-taxonomy.md §4/§5/§6.

No invent: only markdown tables inside those sections. Do not parse §7
disposition tokens into canonical_keys.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping

from core.taxonomy.axes import TAXONOMY_AXIS_VALUES
from core.taxonomy.disposition import LABEL_DISPOSITION_VALUES

SECTION_4_HEADING_TO_AXIS: Mapping[str, str] = {
    "4.1": "topic_domain",
    "4.2": "failure_mode",
    "4.3": "civic_signal",
    "4.4": "issue_archetype_support",
    "4.5": "service_object",
    "4.6": "affected_scope",
    "4.7": "deep_need",
    "4.8": "desired_outcome",
    "4.9": "ecosystem_signal",
    "4.10": "governance_signal",
}

# GPT §6 prose split (story SSOT) — not invent.
RISK_PRIVACY_SAFETY_KEYS: frozenset[str] = frozenset(
    {
        "pii_present",
        "redaction_needed",
        "limited_depth",
        "minor_context",
        "health_context",
        "violence_context",
    }
)
CONFIDENCE_STATE_KEYS: frozenset[str] = frozenset(
    {
        "confirmed_by_user",
        "gpt_hypothesis",
        "needs_clarification",
        "low_confidence",
        "conflict_unresolved",
    }
)

# Stable axis order for taxonomy.json (matches GPT §3 / prior tallinn WIP).
AXES_ORDER: tuple[str, ...] = (
    "topic_domain",
    "service_object",
    "location_context",
    "failure_mode",
    "issue_archetype_support",
    "affected_scope",
    "civic_signal",
    "deep_need",
    "desired_outcome",
    "ecosystem_signal",
    "governance_signal",
    "risk_privacy_safety",
    "confidence_state",
)

INTERNAL_AXES: tuple[str, ...] = ("risk_privacy_safety", "confidence_state")

MIN_AXIS_TO_SIGNAL_MAP: Mapping[str, str] = {
    "topic_domain": "signals.civic_domain",
    "failure_mode": "signals.failure_pattern",
}

DISPOSITIONS_ORDER: tuple[str, ...] = (
    "canonical",
    "metadata_only",
    "needs_clarification",
    "rejected",
    "internal",
)

_KEY_MEANING_ROW = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|",
    flags=re.MULTILINE,
)
_SECTION_SPLIT = re.compile(r"(?=^## )", flags=re.MULTILINE)


def workspace_root_from_gateway(gateway_root: Path) -> Path:
    return gateway_root.resolve().parent


def default_gpt_taxonomy_md(gateway_root: Path) -> Path:
    return (
        workspace_root_from_gateway(gateway_root)
        / "GPT UI"
        / "instructions"
        / "story-label-taxonomy.md"
    )


def _section_body(md: str, heading_prefix: str) -> str:
    parts = _SECTION_SPLIT.split(md)
    for part in parts:
        if part.startswith(heading_prefix):
            return part
    raise ValueError(f"Missing markdown section starting with {heading_prefix!r}")


def _append_unique(
    inventory: dict[str, list[tuple[str, str]]],
    axis: str,
    key: str,
    meaning: str,
) -> None:
    bucket = inventory.setdefault(axis, [])
    if any(existing == key for existing, _ in bucket):
        return
    bucket.append((key, meaning))


def extract_canonical_inventory(md_text: str) -> dict[str, list[tuple[str, str]]]:
    """Return axis → ordered (key, meaning) from GPT §4 + §5 + §6 only."""
    inventory: dict[str, list[tuple[str, str]]] = {axis: [] for axis in AXES_ORDER}

    sec4 = _section_body(md_text, "## 4.")
    for match in re.finditer(r"^### (4\.\d+)\s+.+$", sec4, flags=re.MULTILINE):
        num = match.group(1)
        if num not in SECTION_4_HEADING_TO_AXIS:
            raise ValueError(f"Unmapped §4 heading number: {num}")
        axis = SECTION_4_HEADING_TO_AXIS[num]
        start = match.end()
        nxt = re.search(r"^### ", sec4[start:], flags=re.MULTILINE)
        chunk = sec4[start : start + nxt.start()] if nxt else sec4[start:]
        for row in _KEY_MEANING_ROW.finditer(chunk):
            key = row.group(1).strip()
            if key.lower() in {"key", "label"}:
                continue
            meaning = row.group(2).strip()
            _append_unique(inventory, axis, key, meaning)

    sec5 = _section_body(md_text, "## 5.")
    for row in _KEY_MEANING_ROW.finditer(sec5):
        axis = row.group(1).strip()
        if axis.lower() == "axis" or axis not in TAXONOMY_AXIS_VALUES:
            continue
        rest = row.group(2)
        for key in re.findall(r"`([^`]+)`", rest):
            _append_unique(
                inventory,
                axis,
                key,
                "metadata-only candidate (GPT §5)",
            )

    sec6 = _section_body(md_text, "## 6.")
    for row in _KEY_MEANING_ROW.finditer(sec6):
        key = row.group(1).strip()
        if key.lower() == "key":
            continue
        meaning = row.group(2).strip()
        if key in RISK_PRIVACY_SAFETY_KEYS:
            _append_unique(inventory, "risk_privacy_safety", key, meaning)
        elif key in CONFIDENCE_STATE_KEYS:
            _append_unique(inventory, "confidence_state", key, meaning)
        else:
            raise ValueError(f"§6 key not assigned by story split: {key!r}")

    # §7 must not leak into inventory (naive whole-file grep pitfall).
    if "## 7." in md_text:
        sec7 = _section_body(md_text, "## 7.")
        for row in _KEY_MEANING_ROW.finditer(sec7):
            token = row.group(1).strip()
            if token.lower() in {"disposition", "key"}:
                continue
            for axis, items in inventory.items():
                if any(k == token for k, _ in items) and axis not in {
                    "confidence_state",
                    "risk_privacy_safety",
                }:
                    # Disposition names may overlap English words; only fail if
                    # a §7-only disposition landed on a public axis.
                    if token in LABEL_DISPOSITION_VALUES and axis not in INTERNAL_AXES:
                        raise AssertionError(
                            f"§7 disposition token {token!r} leaked onto axis {axis}"
                        )

    missing_axes = TAXONOMY_AXIS_VALUES - set(inventory)
    if missing_axes:
        raise ValueError(f"Inventory missing axes: {sorted(missing_axes)}")
    empty = [a for a, items in inventory.items() if not items]
    if empty:
        raise ValueError(f"Inventory empty for axes: {empty}")
    return inventory


def inventory_key_sets(
    inventory: Mapping[str, list[tuple[str, str]]],
) -> dict[str, frozenset[str]]:
    return {axis: frozenset(k for k, _ in items) for axis, items in inventory.items()}


def assert_no_silent_rename_vs_prior(
    current: Mapping[str, frozenset[str]],
    prior: Mapping[str, frozenset[str]],
) -> None:
    """HARD STOP if a prior §4 export key disappeared (silent rename / drop)."""
    for axis, prior_keys in prior.items():
        cur = current.get(axis, frozenset())
        missing = prior_keys - cur
        if missing:
            raise AssertionError(
                f"HARD STOP: axis {axis!r} lost keys vs prior export: {sorted(missing)}"
            )


def build_taxonomy_document(
    inventory: Mapping[str, list[tuple[str, str]]],
    *,
    schema_id: str = "tallinn_civic",
    schema_version: str = "v1",
) -> dict:
    if set(AXES_ORDER) != TAXONOMY_AXIS_VALUES:
        raise AssertionError("AXES_ORDER must equal TAXONOMY_AXIS_VALUES")
    if set(DISPOSITIONS_ORDER) != LABEL_DISPOSITION_VALUES:
        raise AssertionError("DISPOSITIONS_ORDER must equal LABEL_DISPOSITION_VALUES")

    canonical_keys: dict[str, list[dict[str, str]]] = {}
    for axis in AXES_ORDER:
        entries = inventory[axis]
        canonical_keys[axis] = [{"key": k, "meaning": m} for k, m in entries]

    return {
        "schema_id": schema_id,
        "schema_version": schema_version,
        "axes": list(AXES_ORDER),
        "internal_axes": list(INTERNAL_AXES),
        "canonical_keys": canonical_keys,
        "axis_to_signal_map": dict(MIN_AXIS_TO_SIGNAL_MAP),
        "dispositions": list(DISPOSITIONS_ORDER),
    }
