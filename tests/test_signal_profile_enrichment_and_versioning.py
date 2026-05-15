from __future__ import annotations

from core.application import SignalProfileService
from core.infrastructure import InMemorySignalProfileRepository


def test_signal_profile_service_creates_enriched_profile_version_one() -> None:
    service = SignalProfileService(repository=InMemorySignalProfileRepository())
    profile = service.create_or_update_profile(
        story_id="story-1",
        narrative_text="Road blocked again near school with broken surface and citizens need access.",
        user_asserted={"topic": "mobility"},
    )
    assert profile.version == 1
    assert profile.user_asserted["topic"] == "mobility"
    assert profile.system_inferred.get("civic_domain") == "unknown"
    assert profile.system_inferred.get("failure_pattern") == "unknown"
    assert profile.system_inferred.get("civic_weight") == "isolated"
    assert profile.system_inferred.get("canonical_type") == "unknown"


def test_signal_profile_service_tracks_versions_for_audit_trail() -> None:
    repository = InMemorySignalProfileRepository()
    service = SignalProfileService(repository=repository)

    first = service.create_or_update_profile(
        story_id="story-2",
        narrative_text="Water leak detected in district center.",
    )
    second = service.create_or_update_profile(
        story_id="story-2",
        narrative_text="Water leak repeated again and escalated.",
        user_asserted={"need": "urgent_repair"},
    )

    assert first.version == 1
    assert second.version == 2
    versions = service.get_versions("story-2")
    assert [item.version for item in versions] == [1, 2]
    assert versions[1].user_asserted["need"] == "urgent_repair"


def test_signal_profile_repository_get_latest_returns_highest_version() -> None:
    """TC-20: direct get_latest contract (latest version + missing story)."""
    repository = InMemorySignalProfileRepository()
    service = SignalProfileService(repository=repository)

    service.create_or_update_profile(
        story_id="story-latest",
        narrative_text="Road damage first report.",
    )
    second = service.create_or_update_profile(
        story_id="story-latest",
        narrative_text="Road damage escalated with photos.",
    )

    latest = repository.get_latest("story-latest")
    assert latest is not None
    assert latest.version == second.version
    assert repository.get_latest("no-such-story") is None

