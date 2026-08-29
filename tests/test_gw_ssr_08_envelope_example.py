"""GW-SSR-08 T05: gateway envelope example (not GPT UI)."""

from __future__ import annotations

import json
from pathlib import Path

from core.schema import LocalSchemaRuntime, SchemaRef

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = GATEWAY_ROOT / "tests/fixtures/gw_ssr_08_tallinn_civic_envelope.json"


def test_envelope_fixture_validates_against_tallinn_civic_pack() -> None:
    body = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert body["schema_version"] == "m2.story_intake_envelope.v2"
    binding = body["schema_binding"]
    assert binding["schema_id"] == "tallinn_civic"
    assert binding["schema_version"] == "v1"
    assert "title" in body["narrative"]
    assert "description" in body["narrative"]
    runtime = LocalSchemaRuntime(packs_root=GATEWAY_ROOT / "schema-packs")
    ctx = runtime.resolve(SchemaRef("tallinn_civic", "v1"))
    runtime.validate(ctx, binding["structured_payload"])
