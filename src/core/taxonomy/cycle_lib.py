"""Shared logic for taxonomy cycle CLI scripts (classify, apply, YAML I/O)."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from core.projection.enums import DOGEIssueLabel
from core.projection.extraction_policy import _CANONICAL_TO_SPA_LABEL  # noqa: PLC2701

Action = Literal["map", "translate_only", "ignore", "pending", "new_board_label"]

LABEL_KEY_RE = re.compile(r"^[a-z][a-z0-9_]{1,48}$")
DEFAULT_MIN_MISS_COUNT = 3
DEFAULT_LOCALES = ("et", "ru", "en")


@dataclass(frozen=True)
class CanonicalSnapshot:
    canonical_keys: frozenset[str]
    canonical_to_spa: dict[str, str]
    doge_issue_label_values: frozenset[str]


@dataclass(frozen=True)
class LabelAggregate:
    label_key: str
    max_miss_count: int
    locales: tuple[str, ...]


@dataclass(frozen=True)
class Decision:
    label_key: str
    action: Action
    target_label: str | None = None
    spa_label: str | None = None
    locales: tuple[str, ...] = DEFAULT_LOCALES
    auto: bool = True
    reason: str = ""
    new_board_label: bool = False
    translations: dict[str, str] | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "label_key": self.label_key,
            "action": self.action,
            "locales": list(self.locales),
            "auto": self.auto,
            "reason": self.reason,
        }
        if self.target_label is not None:
            out["target_label"] = self.target_label
        if self.spa_label is not None:
            out["spa_label"] = self.spa_label
        if self.new_board_label:
            out["new_board_label"] = True
        if self.translations:
            out["translations"] = dict(self.translations)
        return out


def load_canonical_snapshot() -> CanonicalSnapshot:
    """Live snapshot from code — no hardcoded label lists."""
    return CanonicalSnapshot(
        canonical_keys=frozenset(_CANONICAL_TO_SPA_LABEL.keys()),
        canonical_to_spa=dict(_CANONICAL_TO_SPA_LABEL),
        doge_issue_label_values=frozenset(label.value for label in DOGEIssueLabel),
    )


def is_valid_label_key(label_key: str) -> bool:
    return bool(LABEL_KEY_RE.match(label_key))


def aggregate_miss_rows(rows: list[dict[str, Any]], *, min_miss_count: int) -> list[LabelAggregate]:
    by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row["label_key"]).strip().lower()
        locale = str(row["locale"]).strip().lower()
        miss_count = int(row["miss_count"])
        entry = by_key.setdefault(
            key,
            {"max_miss_count": 0, "locales": set()},
        )
        entry["max_miss_count"] = max(entry["max_miss_count"], miss_count)
        if miss_count >= min_miss_count:
            entry["locales"].add(locale)
    aggregates = [
        LabelAggregate(
            label_key=key,
            max_miss_count=entry["max_miss_count"],
            locales=tuple(sorted(entry["locales"])),
        )
        for key, entry in sorted(by_key.items())
    ]
    return aggregates


def classify_label(
    agg: LabelAggregate,
    *,
    snapshot: CanonicalSnapshot,
    min_miss_count: int = DEFAULT_MIN_MISS_COUNT,
) -> Decision:
    key = agg.label_key
    if not is_valid_label_key(key):
        return Decision(
            label_key=key,
            action="ignore",
            locales=agg.locales or DEFAULT_LOCALES,
            reason="invalid label_key pattern",
        )
    if agg.max_miss_count < min_miss_count:
        return Decision(
            label_key=key,
            action="ignore",
            locales=agg.locales or DEFAULT_LOCALES,
            reason=f"miss_count below threshold ({min_miss_count})",
        )
    locales = agg.locales or DEFAULT_LOCALES
    if key in snapshot.canonical_to_spa:
        return Decision(
            label_key=key,
            action="translate_only",
            spa_label=snapshot.canonical_to_spa[key],
            locales=locales,
            reason="canonical token already mapped in _CANONICAL_TO_SPA_LABEL",
        )
    if key in snapshot.doge_issue_label_values:
        return Decision(
            label_key=key,
            action="translate_only",
            spa_label=key,
            locales=locales,
            reason="key matches DOGEIssueLabel value",
        )
    return Decision(
        label_key=key,
        action="pending",
        locales=locales,
        reason="new canonical token — operator decision required",
    )


def classify_all(
    aggregates: list[LabelAggregate],
    *,
    snapshot: CanonicalSnapshot | None = None,
    min_miss_count: int = DEFAULT_MIN_MISS_COUNT,
) -> list[Decision]:
    snap = snapshot or load_canonical_snapshot()
    return [classify_label(agg, snapshot=snap, min_miss_count=min_miss_count) for agg in aggregates]


def _yaml_quote(value: str) -> str:
    if re.search(r"[:\[\]{}#&*!|>'\"%@`]", value) or value.startswith((" ", "-")):
        return json.dumps(value)
    return value


def _dump_yaml_scalar(key: str, value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, bool):
        return f"{pad}{key}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{pad}{key}: {value}"
    if isinstance(value, str):
        return f"{pad}{key}: {_yaml_quote(value)}"
    if isinstance(value, list):
        if not value:
            return f"{pad}{key}: []"
        lines = [f"{pad}{key}:"]
        for item in value:
            if isinstance(item, str):
                lines.append(f"{pad}  - {_yaml_quote(item)}")
            else:
                lines.append(f"{pad}  - {item}")
        return "\n".join(lines)
    if isinstance(value, dict):
        lines = [f"{pad}{key}:"]
        for sub_key, sub_val in value.items():
            lines.append(_dump_yaml_scalar(str(sub_key), sub_val, indent + 2))
        return "\n".join(lines)
    return f"{pad}{key}: {value!r}"


def write_decisions_yaml(
    path: Path,
    *,
    cycle_id: str,
    decisions: list[Decision],
    min_miss_count: int = DEFAULT_MIN_MISS_COUNT,
) -> None:
    lines = [
        f"cycle_id: {_yaml_quote(cycle_id)}",
        "thresholds:",
        f"  min_miss_count: {min_miss_count}",
        "decisions:",
    ]
    for decision in decisions:
        lines.append(f"  - label_key: {_yaml_quote(decision.label_key)}")
        lines.append(f"    action: {decision.action}")
        if decision.target_label is not None:
            lines.append(f"    target_label: {_yaml_quote(decision.target_label)}")
        if decision.spa_label is not None:
            lines.append(f"    spa_label: {_yaml_quote(decision.spa_label)}")
        lines.append(f"    locales: [{', '.join(decision.locales)}]")
        lines.append(f"    auto: {'true' if decision.auto else 'false'}")
        lines.append(f"    reason: {_yaml_quote(decision.reason)}")
        if decision.new_board_label:
            lines.append("    new_board_label: true")
        if decision.translations:
            lines.append("    translations:")
            for loc, text in sorted(decision.translations.items()):
                lines.append(f"      {loc}: {_yaml_quote(text)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_yaml_list_block(lines: list[str], start: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        stripped = line.lstrip()
        if not stripped.startswith("- "):
            break
        item_indent = len(line) - len(stripped)
        if item_indent > len(lines[start].lstrip()) + 2 and items:
            break
        body = stripped[2:].strip()
        if ":" in body and not body.startswith('"'):
            key, _, rest = body.partition(":")
            rest = rest.strip()
            item: dict[str, Any] = {key.strip(): _coerce_scalar(rest)}
            i += 1
            while i < len(lines):
                sub = lines[i]
                if not sub.strip():
                    i += 1
                    continue
                sub_stripped = sub.lstrip()
                if sub_stripped.startswith("- "):
                    break
                sub_indent = len(sub) - len(sub_stripped)
                if sub_indent <= item_indent:
                    break
                sub_key, _, sub_rest = sub_stripped.partition(":")
                sub_key = sub_key.strip()
                sub_rest = sub_rest.strip()
                if sub_rest == "" and i + 1 < len(lines):
                    nested_lines = []
                    j = i + 1
                    while j < len(lines):
                        nested = lines[j]
                        if not nested.strip():
                            j += 1
                            continue
                        nested_stripped = nested.lstrip()
                        nested_indent = len(nested) - len(nested_stripped)
                        if nested_indent <= sub_indent:
                            break
                        nested_lines.append(nested)
                        j += 1
                    if sub_key == "locales":
                        item[sub_key] = _parse_inline_or_block_list(nested_lines)
                    elif sub_key == "translations":
                        item[sub_key] = _parse_mapping_block(nested_lines, base_indent=sub_indent + 2)
                    i = j
                    continue
                item[sub_key] = _coerce_scalar(sub_rest)
                i += 1
            items.append(item)
            continue
        items.append(_coerce_scalar(body))
        i += 1
    return items, i


def _parse_inline_or_block_list(lines: list[str]) -> list[str]:
    if not lines:
        return []
    first = lines[0].lstrip()
    if first.startswith("- "):
        result, _ = _parse_yaml_list_block(lines, 0)
        return [str(x) for x in result]
    return []


def _parse_mapping_block(lines: list[str], *, base_indent: int) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent < base_indent:
            break
        key, _, rest = stripped.partition(":")
        out[key.strip()] = str(_coerce_scalar(rest.strip()))
    return out


def _coerce_scalar(raw: str) -> Any:
    if not raw:
        return ""
    if raw in ("true", "false"):
        return raw == "true"
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("'\"") for part in inner.split(",") if part.strip()]
    if raw[0] in "'\"" and raw[-1] == raw[0]:
        return raw[1:-1]
    if raw.isdigit():
        return int(raw)
    return raw


def parse_decisions_yaml(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    root: dict[str, Any] = {"decisions": []}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if key == "decisions" and rest == "":
            items, i = _parse_yaml_list_block(lines, i + 1)
            root["decisions"] = items
            continue
        if key == "thresholds" and rest == "":
            thresholds: dict[str, Any] = {}
            i += 1
            while i < len(lines):
                sub = lines[i]
                if not sub.strip():
                    i += 1
                    continue
                sub_stripped = sub.lstrip()
                if not sub_stripped.startswith("  ") or sub_stripped.startswith("- "):
                    break
                sub_key, _, sub_rest = sub_stripped.strip().partition(":")
                thresholds[sub_key.strip()] = _coerce_scalar(sub_rest.strip())
                i += 1
            root["thresholds"] = thresholds
            continue
        root[key] = _coerce_scalar(rest)
        i += 1
    return root


def decisions_from_manifest(data: dict[str, Any]) -> list[Decision]:
    raw_items = data.get("decisions") or []
    result: list[Decision] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        locales_raw = item.get("locales") or list(DEFAULT_LOCALES)
        locales = tuple(str(x) for x in locales_raw)
        translations = item.get("translations")
        result.append(
            Decision(
                label_key=str(item["label_key"]),
                action=str(item["action"]),  # type: ignore[arg-type]
                target_label=item.get("target_label"),
                spa_label=item.get("spa_label"),
                locales=locales,
                auto=bool(item.get("auto", True)),
                reason=str(item.get("reason", "")),
                new_board_label=bool(item.get("new_board_label", False)),
                translations=dict(translations) if isinstance(translations, dict) else None,
            )
        )
    return result


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def member_name_for_label(value: str) -> str:
    return value.upper()


def read_canonical_dict_from_source(source_text: str) -> dict[str, str]:
    """Parse _CANONICAL_TO_SPA_LABEL keys and resolved string values from source text."""
    pattern = re.compile(
        r'"([a-z][a-z0-9_]*)"\s*:\s*(?:DOGEIssueLabel\.([A-Z_]+)\.value|"([a-z][a-z0-9_]*)")'
    )
    block_start = source_text.find("_CANONICAL_TO_SPA_LABEL")
    if block_start < 0:
        raise ValueError("_CANONICAL_TO_SPA_LABEL dict not found in source.")
    block_end = source_text.find("\n}", block_start)
    if block_end < 0:
        raise ValueError("Cannot locate end of _CANONICAL_TO_SPA_LABEL block.")
    block = source_text[block_start:block_end]
    result: dict[str, str] = {}
    enum_values = {label.name: label.value for label in DOGEIssueLabel}
    for match in pattern.finditer(block):
        key = match.group(1)
        enum_member = match.group(2)
        literal = match.group(3)
        if enum_member is not None:
            value = enum_values.get(enum_member)
            if value is None:
                raise ValueError(f"Unknown DOGEIssueLabel member: {enum_member}")
            result[key] = value
        elif literal is not None:
            result[key] = literal
    if not result:
        raise ValueError("_CANONICAL_TO_SPA_LABEL dict not found in source.")
    return result


def patch_canonical_mapping(source_text: str, *, canonical: str, spa_label: str) -> str:
    current = read_canonical_dict_from_source(source_text)
    if canonical in current:
        if current[canonical] == spa_label:
            return source_text
        raise ValueError(
            f"Canonical key {canonical!r} already mapped to {current[canonical]!r}, not {spa_label!r}."
        )
    needle = "_CANONICAL_TO_SPA_LABEL: dict[str, str] = {"
    start = source_text.find(needle)
    if start < 0:
        raise ValueError("Cannot locate _CANONICAL_TO_SPA_LABEL block.")
    close = source_text.find("\n}", start)
    if close < 0:
        raise ValueError("Cannot locate end of _CANONICAL_TO_SPA_LABEL block.")
    insertion = f'\n    "{canonical}": DOGEIssueLabel.{member_name_for_label(spa_label)}.value,'
    return source_text[:close] + insertion + source_text[close:]


def read_doge_issue_labels_from_source(source_text: str) -> list[str]:
    module = ast.parse(source_text)
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == "DOGEIssueLabel":
            labels: list[str] = []
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            labels.append(ast.literal_eval(item.value))
            return labels
    raise ValueError("DOGEIssueLabel class not found in source.")


def patch_doge_issue_label_enum(source_text: str, *, member_name: str, value: str) -> str:
    existing = read_doge_issue_labels_from_source(source_text)
    if value in existing:
        return source_text
    needle = "class DOGEIssueLabel(StrEnum):"
    start = source_text.find(needle)
    if start < 0:
        raise ValueError("Cannot locate DOGEIssueLabel class.")
    close = source_text.find("\n\n", start)
    if close < 0:
        close = len(source_text)
    insertion = f'\n    {member_name} = "{value}"'
    return source_text[:close] + insertion + source_text[close:]
