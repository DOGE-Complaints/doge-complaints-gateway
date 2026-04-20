from __future__ import annotations

from core.application import SignalProfileService
from core.infrastructure import InMemorySignalProfileRepository


def test_signal_profile_service_creates_enriched_profile_version_one() -> None:
    service = SignalProfileService(repository=InMemorySignalProfileRepository())
    profile = service.create_or_update_profile(
        story_id="story-1",
        narrative_text="Road blocked again near school and citizens need access.",
        user_asserted={"topic": "mobility"},
    )
    assert profile.version == 1
    assert profile.user_asserted["topic"] == "mobility"
    assert profile.system_inferred["system_failure"] == "service_disruption"
    assert profile.system_inferred["repeatability"] == "recurrent"


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

