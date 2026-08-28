"""COMPAT-001 conceptual civic envelope marker. Does not change intake version."""

from __future__ import annotations

from dataclasses import dataclass

# Civic envelope id (intake constant). Named here; INTAKE_SCHEMA_VERSION is not mutated.
LEGACY_M2_ENVELOPE_ID = "m2.story_intake_envelope.v2"


@dataclass(frozen=True)
class LegacyM2StorySchema:
    """Marker adapter for existing Tallinn civic envelope (REQ3-COMPAT-001)."""

    envelope_id: str = LEGACY_M2_ENVELOPE_ID
