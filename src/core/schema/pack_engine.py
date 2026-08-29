"""Schema-pack exact lens membership (SSR-04). Civic ClusterLens is not extended."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from core.domain import StoryRecord
from core.schema.contracts import ExactLensBlock, SchemaContext, SchemaRef
from core.schema.errors import PackLensMissingPathError
from core.schema.runtime import LocalSchemaRuntime

_MISSING = object()


def is_schema_bound(story: StoryRecord) -> bool:
    """True when persist binding is present (SSR-02). None stays civic."""
    return bool(story.schema_id) and bool(story.bound_schema_version)


def _dotted_get(payload: Mapping[str, Any] | None, path: str) -> object:
    if payload is None or not path:
        return _MISSING
    current: object = payload
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _leaf_token(value: object) -> str | None:
    """Stable token for exact-key join. Not a narrative; never dump mappings."""
    if value is _MISSING or value is None:
        return None
    if isinstance(value, Mapping) or isinstance(value, (list, tuple, dict)):
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip()
    return text or None


def pack_cluster_id(*, schema_id: str, lens_id: str, field_tokens: tuple[str, ...]) -> str:
    joined = "|".join(field_tokens)
    return f"schema:{schema_id}:{lens_id}:{joined}"


@dataclass(frozen=True)
class PackMembership:
    story_id: str
    lens: str
    cluster_id: str


class SchemaPackClusterEngine:
    """Exact membership from pack ``exact_lenses`` source_fields. No ClusterLens."""

    def __init__(self, schema_runtime: LocalSchemaRuntime | None = None) -> None:
        self._runtime = schema_runtime or LocalSchemaRuntime()

    def memberships_for_story(self, story: StoryRecord) -> tuple[PackMembership, ...]:
        if not is_schema_bound(story):
            return ()
        context = self._runtime.resolve(
            SchemaRef(schema_id=story.schema_id or "", schema_version=story.bound_schema_version or ""),
            profile_ref=story.profile_id,
        )
        return self.memberships_for_context(story, context)

    def dual_civic_lenses_for(self, story: StoryRecord) -> bool:
        """True only when the bound pack opts into civic+exact (SSR-10)."""
        if not is_schema_bound(story):
            return False
        context = self._runtime.resolve(
            SchemaRef(schema_id=story.schema_id or "", schema_version=story.bound_schema_version or ""),
            profile_ref=story.profile_id,
        )
        return context.dual_civic_lenses

    def lens_block_for(self, story: StoryRecord, lens_id: str) -> ExactLensBlock | None:
        """Return the pack ExactLensBlock matching lens_id, or None."""
        if not is_schema_bound(story):
            return None
        context = self._runtime.resolve(
            SchemaRef(schema_id=story.schema_id or "", schema_version=story.bound_schema_version or ""),
            profile_ref=story.profile_id,
        )
        for lens in context.exact_lenses:
            if lens.lens_id == lens_id:
                return lens
        return None

    def memberships_for_context(
        self, story: StoryRecord, context: SchemaContext
    ) -> tuple[PackMembership, ...]:
        found: list[PackMembership] = []
        for lens in context.exact_lenses:
            membership = self._membership_for_lens(story, context, lens)
            if membership is not None:
                found.append(membership)
        return tuple(found)

    def _membership_for_lens(
        self,
        story: StoryRecord,
        context: SchemaContext,
        lens: ExactLensBlock,
    ) -> PackMembership | None:
        if lens.algorithm != "exact":
            return None
        tokens: list[str] = []
        payload = story.structured_payload
        for path in lens.source_fields:
            raw = _dotted_get(payload, path)
            token = _leaf_token(raw)
            if token is None:
                policy = (lens.missing_value_policy or "skip").strip().lower()
                if policy == "skip":
                    return None
                raise PackLensMissingPathError(
                    f"missing source field {path!r} for lens {lens.lens_id!r}"
                )
            tokens.append(token)
        if not tokens:
            return None
        cluster_id = pack_cluster_id(
            schema_id=context.ref.schema_id,
            lens_id=lens.lens_id,
            field_tokens=tuple(tokens),
        )
        return PackMembership(
            story_id=story.story_id,
            lens=lens.lens_id,
            cluster_id=cluster_id,
        )
