"""GW-SSR-32: Contour1 wire axes — open normalize_axis (D-SSR-11)."""

from __future__ import annotations

import pytest

from core.cluster.types import ClusterLens
from core.domain import SignalDimension, StoryLabel
from core.intake import IntakeValidationError, parse_story_intake_request
from core.taxonomy.axes import TAXONOMY_AXIS_VALUES, normalize_axis
from core.taxonomy.story_labels import parse_taxonomy_payload, signals_from_story_labels
from tests.intake_v2_fixtures import valid_v2_intake_payload


def test_normalize_axis_accepts_custom_id() -> None:
    assert normalize_axis("Signal_Type") == "signal_type"
    assert normalize_axis("signal_type") not in TAXONOMY_AXIS_VALUES


def test_normalize_axis_rejects_empty_and_non_string() -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        normalize_axis("")
    with pytest.raises(ValueError, match="non-empty string"):
        normalize_axis("   ")
    with pytest.raises(ValueError, match="non-empty string"):
        normalize_axis(None)
    with pytest.raises(ValueError, match="non-empty string"):
        normalize_axis(12)


def test_parse_taxonomy_payload_accepts_custom_axis() -> None:
    entries = parse_taxonomy_payload(
        {
            "signal_type": [{"label": "problem", "disposition": "canonical"}],
        }
    )
    assert len(entries) == 1
    assert entries[0].axis == "signal_type"
    assert entries[0].label == "problem"
    assert entries[0].disposition == "canonical"


def test_intake_accepts_custom_axis_on_wire() -> None:
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            narrative={
                "taxonomy": {
                    "signal_type": [
                        {"label": "problem", "disposition": "canonical"},
                    ],
                }
            }
        )
    )
    assert len(request.narrative.taxonomy) == 1
    assert request.narrative.taxonomy[0].axis == "signal_type"
    assert request.narrative.taxonomy[0].label == "problem"


def test_intake_rejects_blank_axis() -> None:
    payload = valid_v2_intake_payload(
        narrative={
            "taxonomy": {
                "": [{"label": "roads", "disposition": "canonical"}],
            }
        }
    )
    with pytest.raises(IntakeValidationError, match="non-empty string"):
        parse_story_intake_request(payload)


def test_civic_skip_unmapped_axes_no_invented_dimension() -> None:
    labels = (
        StoryLabel(
            story_id="s1",
            axis="signal_type",
            label="problem",
            disposition="canonical",
        ),
    )
    signals = signals_from_story_labels(canonical_type="complaint", labels=labels)
    assert SignalDimension.CIVIC_DOMAIN.value in signals
    assert signals[SignalDimension.CIVIC_DOMAIN.value] == "unknown"
    assert "signal_type" not in signals
    assert SignalDimension.CANONICAL_TYPE.value in signals


def test_civic_mapped_axis_still_fills_dimension() -> None:
    labels = (
        StoryLabel(
            story_id="s1",
            axis="topic_domain",
            label="transport",
            disposition="canonical",
        ),
        StoryLabel(
            story_id="s1",
            axis="signal_type",
            label="problem",
            disposition="canonical",
        ),
    )
    signals = signals_from_story_labels(canonical_type="complaint", labels=labels)
    assert signals[SignalDimension.CIVIC_DOMAIN.value] == "transport"


def test_classic_thirteen_axis_wire_still_parses() -> None:
    taxonomy = {
        axis: [{"label": f"label_{axis}", "disposition": "canonical"}]
        for axis in sorted(TAXONOMY_AXIS_VALUES)
    }
    entries = parse_taxonomy_payload(taxonomy)
    assert len(entries) == 13
    assert {e.axis for e in entries} == TAXONOMY_AXIS_VALUES

    request = parse_story_intake_request(
        valid_v2_intake_payload(narrative={"taxonomy": taxonomy})
    )
    assert len(request.narrative.taxonomy) == 13


def test_cluster_lens_unchanged() -> None:
    assert len(ClusterLens) == 10
