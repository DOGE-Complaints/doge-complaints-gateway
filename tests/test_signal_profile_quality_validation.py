from __future__ import annotations

from datetime import UTC, datetime

from core.application import SignalProfileService
from core.domain import SignalProfileRecord
from core.infrastructure import InMemorySignalProfileRepository


def test_signal_profile_quality_validation_passes_for_enriched_profile() -> None:
    service = SignalProfileService(repository=InMemorySignalProfileRepository())
    profile = service.create_or_update_profile(
        story_id="story-3",
        narrative_text="Public road blocked and people cannot pass.",
    )
    assert service.validate_quality(profile) == []


def test_signal_profile_quality_validation_detects_missing_dimensions() -> None:
    service = SignalProfileService(repository=InMemorySignalProfileRepository())
    profile = SignalProfileRecord(
        story_id="story-4",
        version=1,
        user_asserted={},
        system_inferred={},
        created_at=datetime.now(UTC),
    )
    errors = service.validate_quality(profile)
    assert any("civic_domain" in item for item in errors)


def test_signal_profile_quality_validation_detects_duplicate_user_system_values() -> None:
    service = SignalProfileService(repository=InMemorySignalProfileRepository())
    profile = SignalProfileRecord(
        story_id="story-5",
        version=1,
        user_asserted={"topic": "infrastructure"},
        system_inferred={"topic": "infrastructure"},
        created_at=datetime.now(UTC),
    )
    errors = service.validate_quality(profile)
    assert any("Duplicate user/system value for topic" in item for item in errors)

