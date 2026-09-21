"""Active-pack shell settings payload for service-auth pull (STORY-GW-THR-02).

Maps THR-01 ``ShellCapabilitiesBlock`` into a settings DTO for threads.
Source = active ``NODE_SCHEMA_*`` pair only (no client-chosen pack id).
JSON field names are an implement-wave lock (Open in REQ) — not written into REQ.
"""

from __future__ import annotations

from typing import Any, Mapping

from core.config import ConfigError
from core.schema.contracts import SchemaRef, ShellCapabilitiesBlock
from core.schema.errors import UnknownSchemaError, UnsupportedVersionError
from core.schema.resolver import default_packs_root, resolve_pack

# Envelope key for the settings object (implement-wave HTTP/JSON lock).
PACK_SHELL_SETTINGS_KEY = "pack_shell_settings"

# Forbidden narrative / ThreadContext composition fields (D19 / AC-GW-THR02-03).
_FORBIDDEN_STORY_KEYS: frozenset[str] = frozenset(
    {
        "story",
        "stories",
        "story_body",
        "narrative",
        "original_text",
        "thread_context",
        "ThreadContext",
    }
)


def shell_capabilities_to_settings_dict(
    caps: ShellCapabilitiesBlock,
    *,
    schema_id: str,
    schema_version: str,
) -> dict[str, Any]:
    """Build settings DTO from already-validated shell capabilities (no Story bodies)."""
    payload: dict[str, Any] = {
        PACK_SHELL_SETTINGS_KEY: {
            "active_schema": {
                "schema_id": schema_id,
                "schema_version": schema_version,
            },
            "verification": {
                "validation_type": caps.validation_type,
                "integration_name": caps.integration_name,
            },
            "threads": {
                "tree": {"max_depth": caps.max_depth},
                "reactions": {
                    "max_reactions_per_actor": caps.max_reactions_per_actor,
                    "enable": dict(caps.reaction_enables),
                    "min_overlap_to_use": {
                        k: float(v) for k, v in caps.reaction_min_overlap.items()
                    },
                    "catalog_ref": caps.catalog_ref,
                },
                "media": {"allowed_types": list(caps.media_allowed_types)},
            },
        }
    }
    assert_no_story_narrative(payload)
    return payload


def assert_no_story_narrative(payload: Mapping[str, Any]) -> None:
    """Reject payloads that embed Story narrative / ThreadContext (D19)."""
    stack: list[Any] = [payload]
    while stack:
        cur = stack.pop()
        if isinstance(cur, Mapping):
            for key, value in cur.items():
                if str(key) in _FORBIDDEN_STORY_KEYS:
                    raise ConfigError(
                        f"pack shell settings must not include Story/ThreadContext "
                        f"field {key!r} (D19 / AC-GW-THR02-03)"
                    )
                stack.append(value)
        elif isinstance(cur, (list, tuple)):
            stack.extend(cur)


def build_active_pack_shell_settings(
    *,
    schema_id: str,
    schema_version: str,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Resolve active NODE_SCHEMA pack and return settings DTO (fail-closed)."""
    packs_root = default_packs_root(environ=environ) if environ is not None else None
    try:
        context = resolve_pack(
            SchemaRef(schema_id=schema_id, schema_version=schema_version),
            packs_root=packs_root,
        )
    except (UnknownSchemaError, UnsupportedVersionError) as exc:
        raise ConfigError(
            f"NODE_SCHEMA_ID/NODE_SCHEMA_VERSION={schema_id!r}/{schema_version!r} "
            f"does not resolve to a pack with shell capabilities: {exc}"
        ) from exc
    return shell_capabilities_to_settings_dict(
        context.shell_capabilities,
        schema_id=schema_id,
        schema_version=schema_version,
    )
