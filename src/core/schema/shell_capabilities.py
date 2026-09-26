"""Active-pack shell capabilities (STORY-GW-THR-01 / REQ52 / REQ7 §7–§8.2).

Implement-wave lock (THR-01 P3): mandatory capabilities live in a **sidecar**
``shell_capabilities.json`` next to ``pack.json`` — not as invented product key
strings inside ``pack.json`` (those remain Open per REQ52 AC-GW-THR-01).

Capability **ids** below are REQ7 shell-knob vocabulary (families / catalog ids),
validated as typed entries. Missing / invalid sidecar → fail-closed
(``UnsupportedVersionError`` → ConfigError on NODE_SCHEMA boot).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from core.schema.contracts import ShellCapabilitiesBlock
from core.schema.errors import UnsupportedVersionError

SHELL_CAPABILITIES_FILENAME = "shell_capabilities.json"
SHELL_CAPABILITIES_SCHEMA = "shell_capabilities.v1"
REACTIONS_CATALOG_REF = "reactions.v1"

# Capability ids = REQ7 §7 / T-REQ7-04 vocabulary (not pack.json product aliases).
CAP_VERIFICATION_VALIDATION_TYPE = "verification.validation_type"
CAP_VERIFICATION_INTEGRATION_NAME = "verification.integration_name"
CAP_THREADS_TREE_MAX_DEPTH = "threads.tree.max_depth"
CAP_THREADS_REACTIONS_MAX_PER_ACTOR = "threads.reactions.max_reactions_per_actor"
CAP_THREADS_REACTIONS_ENABLE = "threads.reactions.enable"
CAP_THREADS_REACTIONS_MIN_OVERLAP = "threads.reactions.min_overlap_to_use"
CAP_THREADS_MEDIA_ALLOWED_TYPES = "threads.media.allowed_types"

REQUIRED_CAPABILITY_IDS: frozenset[str] = frozenset(
    {
        CAP_VERIFICATION_VALIDATION_TYPE,
        CAP_VERIFICATION_INTEGRATION_NAME,
        CAP_THREADS_TREE_MAX_DEPTH,
        CAP_THREADS_REACTIONS_MAX_PER_ACTOR,
        CAP_THREADS_REACTIONS_ENABLE,
        CAP_THREADS_REACTIONS_MIN_OVERLAP,
        CAP_THREADS_MEDIA_ALLOWED_TYPES,
    }
)

VALIDATION_TYPES: frozenset[str] = frozenset({"phone", "eID"})

# reactions.v1 catalog ids (REQ7 §8.2 / Emotional reactions SSOT).
REACTIONS_V1_IDS: frozenset[str] = frozenset(
    {
        "acknowledge",
        "support",
        "empathy",
        "concern",
        "hopeful",
        "sad",
        "outraged_situation",
        "amused",
        "agree",
        "disagree",
        "useful_fact",
        "insightful",
        "needs_evidence",
        "off_topic",
        "aggressive",
    }
)

# Topic-guarded presentation defaults (REQ7 §8.2 / D15).
TOPIC_GUARDED_REACTION_ENABLES: dict[str, bool] = {
    "acknowledge": True,
    "support": True,
    "empathy": True,
    "concern": True,
    "hopeful": False,
    "sad": True,
    "outraged_situation": True,
    "amused": False,
    "agree": True,
    "disagree": True,
    "useful_fact": True,
    "insightful": True,
    "needs_evidence": True,
    "off_topic": True,
    "aggressive": True,
}

TOPIC_GUARDED_MIN_OVERLAP: dict[str, float] = {
    "amused": 0.70,
}

TOPIC_GUARDED_MAX_REACTIONS_PER_ACTOR = 3
TOPIC_GUARDED_MAX_DEPTH = 6

# Media types within parent §9 floors (node allowlist; CSAM floor is platform).
TOPIC_GUARDED_MEDIA_ALLOWED_TYPES: tuple[str, ...] = (
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "application/pdf",
)


def topic_guarded_document(
    *,
    validation_type: str,
    integration_name: str,
    max_depth: int = TOPIC_GUARDED_MAX_DEPTH,
    max_reactions_per_actor: int = TOPIC_GUARDED_MAX_REACTIONS_PER_ACTOR,
    media_allowed_types: tuple[str, ...] = TOPIC_GUARDED_MEDIA_ALLOWED_TYPES,
) -> dict[str, Any]:
    """Build a Topic-guarded sidecar document (pack content, not silent code defaults)."""
    if validation_type not in VALIDATION_TYPES:
        raise ValueError(f"validation_type must be one of {sorted(VALIDATION_TYPES)}")
    if not integration_name or not str(integration_name).strip():
        raise ValueError("integration_name must be a non-empty string")
    return {
        "schema": SHELL_CAPABILITIES_SCHEMA,
        "catalog_ref": REACTIONS_CATALOG_REF,
        "entries": [
            {"id": CAP_VERIFICATION_VALIDATION_TYPE, "value": validation_type},
            {
                "id": CAP_VERIFICATION_INTEGRATION_NAME,
                "value": str(integration_name).strip(),
            },
            {"id": CAP_THREADS_TREE_MAX_DEPTH, "value": max_depth},
            {
                "id": CAP_THREADS_REACTIONS_MAX_PER_ACTOR,
                "value": max_reactions_per_actor,
            },
            {
                "id": CAP_THREADS_REACTIONS_ENABLE,
                "value": dict(TOPIC_GUARDED_REACTION_ENABLES),
            },
            {
                "id": CAP_THREADS_REACTIONS_MIN_OVERLAP,
                "value": dict(TOPIC_GUARDED_MIN_OVERLAP),
            },
            {
                "id": CAP_THREADS_MEDIA_ALLOWED_TYPES,
                "value": list(media_allowed_types),
            },
        ],
    }


def write_shell_capabilities(
    pack_dir: Path,
    document: Mapping[str, Any] | None = None,
    *,
    validation_type: str = "phone",
    integration_name: str = "demo_phone_sms",
) -> Path:
    """Write ``shell_capabilities.json`` under ``pack_dir`` (tests / migrate)."""
    body = document or topic_guarded_document(
        validation_type=validation_type,
        integration_name=integration_name,
    )
    path = pack_dir / SHELL_CAPABILITIES_FILENAME
    path.write_text(
        json.dumps(body, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def load_shell_capabilities(pack_dir: Path) -> ShellCapabilitiesBlock:
    """Load and validate mandatory shell capabilities; fail-closed if absent/invalid."""
    path = pack_dir / SHELL_CAPABILITIES_FILENAME
    if not path.is_file():
        raise UnsupportedVersionError(
            f"missing mandatory {SHELL_CAPABILITIES_FILENAME} "
            f"(shell capabilities required; no silent defaults)"
        )
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UnsupportedVersionError(
            f"{SHELL_CAPABILITIES_FILENAME} is not valid JSON: {exc}"
        ) from exc
    return parse_shell_capabilities(raw)


def parse_shell_capabilities(raw: Any) -> ShellCapabilitiesBlock:
    """Parse sidecar document into ``ShellCapabilitiesBlock`` (fail-closed)."""
    if not isinstance(raw, dict):
        raise UnsupportedVersionError(
            f"{SHELL_CAPABILITIES_FILENAME} must be a JSON object"
        )
    schema = raw.get("schema")
    if schema != SHELL_CAPABILITIES_SCHEMA:
        raise UnsupportedVersionError(
            f"{SHELL_CAPABILITIES_FILENAME} schema must be "
            f"{SHELL_CAPABILITIES_SCHEMA!r}, got {schema!r}"
        )
    catalog_ref = raw.get("catalog_ref", REACTIONS_CATALOG_REF)
    if catalog_ref != REACTIONS_CATALOG_REF:
        raise UnsupportedVersionError(
            f"catalog_ref must be {REACTIONS_CATALOG_REF!r}, got {catalog_ref!r}"
        )
    entries = raw.get("entries")
    if not isinstance(entries, list) or not entries:
        raise UnsupportedVersionError(
            f"{SHELL_CAPABILITIES_FILENAME} entries must be a non-empty array"
        )
    by_id: dict[str, Any] = {}
    for index, item in enumerate(entries):
        if not isinstance(item, dict):
            raise UnsupportedVersionError(
                f"entries[{index}] must be an object"
            )
        cap_id = item.get("id")
        if not isinstance(cap_id, str) or not cap_id:
            raise UnsupportedVersionError(
                f"entries[{index}].id must be a non-empty string"
            )
        if cap_id in by_id:
            raise UnsupportedVersionError(f"duplicate capability id: {cap_id}")
        if "value" not in item:
            raise UnsupportedVersionError(
                f"entries[{index}] missing value for id={cap_id!r}"
            )
        by_id[cap_id] = item["value"]

    missing = REQUIRED_CAPABILITY_IDS - frozenset(by_id)
    if missing:
        raise UnsupportedVersionError(
            "missing mandatory shell capabilities: "
            + ", ".join(sorted(missing))
            + " (no silent defaults)"
        )

    validation_type = by_id[CAP_VERIFICATION_VALIDATION_TYPE]
    if validation_type not in VALIDATION_TYPES:
        raise UnsupportedVersionError(
            f"{CAP_VERIFICATION_VALIDATION_TYPE} must be one of "
            f"{sorted(VALIDATION_TYPES)}, got {validation_type!r}"
        )

    integration_name = by_id[CAP_VERIFICATION_INTEGRATION_NAME]
    if not isinstance(integration_name, str) or not integration_name.strip():
        raise UnsupportedVersionError(
            f"{CAP_VERIFICATION_INTEGRATION_NAME} must be a non-empty string"
        )

    max_depth = _require_positive_int(
        by_id[CAP_THREADS_TREE_MAX_DEPTH],
        name=CAP_THREADS_TREE_MAX_DEPTH,
    )
    max_reactions = _require_positive_int(
        by_id[CAP_THREADS_REACTIONS_MAX_PER_ACTOR],
        name=CAP_THREADS_REACTIONS_MAX_PER_ACTOR,
    )

    enables_raw = by_id[CAP_THREADS_REACTIONS_ENABLE]
    if not isinstance(enables_raw, dict) or not enables_raw:
        raise UnsupportedVersionError(
            f"{CAP_THREADS_REACTIONS_ENABLE} must be a non-empty object"
        )
    reaction_enables: dict[str, bool] = {}
    for reaction_id, enabled in enables_raw.items():
        if reaction_id not in REACTIONS_V1_IDS:
            raise UnsupportedVersionError(
                f"unknown reaction_id in enable map: {reaction_id!r}"
            )
        if not isinstance(enabled, bool):
            raise UnsupportedVersionError(
                f"enable flag for {reaction_id!r} must be boolean"
            )
        reaction_enables[str(reaction_id)] = enabled
    missing_reactions = REACTIONS_V1_IDS - frozenset(reaction_enables)
    if missing_reactions:
        raise UnsupportedVersionError(
            "reaction enable map missing catalog ids: "
            + ", ".join(sorted(missing_reactions))
        )

    overlap_raw = by_id[CAP_THREADS_REACTIONS_MIN_OVERLAP]
    if not isinstance(overlap_raw, dict):
        raise UnsupportedVersionError(
            f"{CAP_THREADS_REACTIONS_MIN_OVERLAP} must be an object"
        )
    reaction_min_overlap: dict[str, float] = {}
    for reaction_id, threshold in overlap_raw.items():
        if reaction_id not in REACTIONS_V1_IDS:
            raise UnsupportedVersionError(
                f"unknown reaction_id in min_overlap map: {reaction_id!r}"
            )
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
            raise UnsupportedVersionError(
                f"min_overlap for {reaction_id!r} must be a number"
            )
        value = float(threshold)
        if not 0.0 <= value <= 1.0:
            raise UnsupportedVersionError(
                f"min_overlap for {reaction_id!r} must be in [0, 1], got {value}"
            )
        reaction_min_overlap[str(reaction_id)] = value
    # Topic-guarded: amused may be off; if enabled, catalog requires 0.70.
    if reaction_enables.get("amused") and reaction_min_overlap.get("amused") != 0.70:
        raise UnsupportedVersionError(
            "amused enabled requires min_overlap_to_use=0.70 (REQ7 §8.2)"
        )

    media_raw = by_id[CAP_THREADS_MEDIA_ALLOWED_TYPES]
    if not isinstance(media_raw, list) or not media_raw:
        raise UnsupportedVersionError(
            f"{CAP_THREADS_MEDIA_ALLOWED_TYPES} must be a non-empty array"
        )
    media_types: list[str] = []
    for item in media_raw:
        if not isinstance(item, str) or not item.strip():
            raise UnsupportedVersionError(
                f"{CAP_THREADS_MEDIA_ALLOWED_TYPES} entries must be non-empty strings"
            )
        media_types.append(item.strip())

    return ShellCapabilitiesBlock(
        validation_type=str(validation_type),
        integration_name=str(integration_name).strip(),
        max_depth=max_depth,
        max_reactions_per_actor=max_reactions,
        reaction_enables=reaction_enables,
        reaction_min_overlap=reaction_min_overlap,
        media_allowed_types=tuple(media_types),
        catalog_ref=str(catalog_ref),
    )


def _require_positive_int(raw: Any, *, name: str) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise UnsupportedVersionError(f"{name} must be a positive integer")
    if raw <= 0:
        raise UnsupportedVersionError(f"{name} must be a positive integer, got {raw}")
    return raw
