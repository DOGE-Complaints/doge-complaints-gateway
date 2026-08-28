"""GW-SSR-01: SchemaRuntime pack load, JSON Schema validate, no pack code exec."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from core.cluster.types import ClusterLens
from core.intake.contracts import INTAKE_SCHEMA_VERSION
from core.schema import (
    ForbiddenFieldError,
    InvalidConstraintError,
    InvalidTypeError,
    LEGACY_M2_ENVELOPE_ID,
    LegacyM2StorySchema,
    LocalSchemaRuntime,
    MissingRequiredError,
    PolicyViolationError,
    ProfileIncompatibilityError,
    SchemaRef,
    UnknownSchemaError,
    UnsupportedVersionError,
)
from core.schema.validator import MAX_NESTING_DEPTH, MAX_PAYLOAD_BYTES, assert_schema_safe

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

CLUSTERLENS_BASELINE = (
    "composite_primary_micro",
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "desired_outcome_local",
    "affected_group_local",
    "geographic_district_micro",
    "service_object_micro",
    "deep_need_local",
    "ecosystem_signal_systemic",
)


def _runtime() -> LocalSchemaRuntime:
    return LocalSchemaRuntime(packs_root=PACKS_ROOT)


def test_clusterlens_baseline_unchanged() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE


def test_jsonschema_importable() -> None:
    assert hasattr(jsonschema, "Draft202012Validator")


def test_resolve_two_packs_same_runtime() -> None:
    runtime = _runtime()
    legal = runtime.resolve(SchemaRef("legal_process", "v1"))
    mobility = runtime.resolve(SchemaRef("mobility_observation", "v1"))
    assert legal.ref.schema_id == "legal_process"
    assert mobility.ref.schema_id == "mobility_observation"
    assert legal.exact_lenses[0].readiness_policy.min_readiness_score == 40
    assert legal.exact_lenses[0].readiness_policy.min_stories == 3
    assert legal.exact_lenses[0].readiness_policy.require_actionable_canonical_type is False
    assert mobility.exact_lenses[0].readiness_policy.min_readiness_score == 25
    assert mobility.exact_lenses[0].readiness_policy.min_stories == 4
    assert mobility.exact_lenses[0].readiness_policy.require_actionable_canonical_type is False


def test_unknown_schema() -> None:
    with pytest.raises(UnknownSchemaError) as exc:
        _runtime().resolve(SchemaRef("no_such_schema", "v1"))
    assert exc.value.code == "unknown_schema"


def test_unsupported_version() -> None:
    with pytest.raises(UnsupportedVersionError) as exc:
        _runtime().resolve(SchemaRef("legal_process", "v9"))
    assert exc.value.code == "unsupported_version"


def test_validate_legal_pass() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    payload = {"institution": {"office_id": "station-1", "name": "Nõmme"}}
    runtime.validate(ctx, payload)
    canonical = runtime.canonicalize(ctx, payload)
    assert canonical == payload
    assert "invented" not in canonical


def test_validate_missing_required() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    with pytest.raises(MissingRequiredError) as exc:
        runtime.validate(ctx, {})
    assert exc.value.code == "missing_required"


def test_validate_invalid_type() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    with pytest.raises(InvalidTypeError) as exc:
        runtime.validate(ctx, {"institution": {"office_id": 12}})
    assert exc.value.code == "invalid_type"


def test_validate_invalid_constraint_enum() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    with pytest.raises(InvalidConstraintError) as exc:
        runtime.validate(
            ctx,
            {"institution": {"office_id": "s1"}, "process": {"stage": "nope"}},
        )
    assert exc.value.code == "invalid_constraint"


def test_forbidden_field_policy() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    payload = {"institution": {"office_id": "s1"}, "secret_note": "leak"}
    runtime.validate(ctx, payload)
    with pytest.raises(ForbiddenFieldError) as exc:
        runtime.enforce_policy(ctx, payload, policy_context={})
    assert exc.value.code == "forbidden"


def test_profile_incompatibility() -> None:
    runtime = _runtime()
    with pytest.raises(ProfileIncompatibilityError) as exc:
        runtime.resolve(SchemaRef("legal_process", "v1"), profile_ref="other")
    assert exc.value.code == "profile_incompatibility"


def test_enforce_policy_without_identity_claims() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    payload = {"institution": {"office_id": "s1"}}
    runtime.enforce_policy(
        ctx,
        payload,
        policy_context={"profile_ref": "legal_access"},
    )


def test_canonicalize_does_not_invent_required() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    empty: dict[str, Any] = {}
    out = runtime.canonicalize(ctx, empty)
    assert out == {}
    assert "institution" not in out


def test_build_index_and_project_are_stubs() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("mobility_observation", "v1"))
    payload = {"route_id": "t1"}
    with pytest.raises(NotImplementedError, match="SSR-06"):
        runtime.build_index(ctx, payload)
    with pytest.raises(NotImplementedError, match="SSR-07"):
        runtime.project(payload, SchemaRef("legal_process", "v1"))


def test_legacy_m2_marker_does_not_change_intake_version() -> None:
    marker = LegacyM2StorySchema()
    assert marker.envelope_id == LEGACY_M2_ENVELOPE_ID
    assert INTAKE_SCHEMA_VERSION == "m2.story_intake_envelope.v2"
    assert marker.envelope_id == INTAKE_SCHEMA_VERSION


def test_no_code_exec_from_pack_bytes(tmp_path: Path) -> None:
    pack_dir = tmp_path / "evil" / "v1"
    pack_dir.mkdir(parents=True)
    (pack_dir / "pack.json").write_text(
        json.dumps(
            {
                "schema_id": "evil",
                "schema_version": "v1",
                "payload_schema": "payload.schema.json",
                "field_policy": {"x": "optional"},
                "exact_lenses": [
                    {
                        "lens_id": "x",
                        "source_fields": ["x"],
                        "algorithm": "exact",
                        "scope": "node",
                        "scale": "micro",
                        "missing_value_policy": "skip",
                        "min_size": 1,
                        "version": "v1",
                        "readiness_policy": {
                            "min_readiness_score": 1,
                            "min_stories": 1,
                            "require_actionable_canonical_type": False,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (pack_dir / "payload.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {
                    "x": {"type": "string"},
                    "$comment": "import os; os.system('echo pwned')",
                },
            }
        ),
        encoding="utf-8",
    )
    runtime = LocalSchemaRuntime(packs_root=tmp_path)
    ctx = runtime.resolve(SchemaRef("evil", "v1"))
    runtime.validate(ctx, {"x": "ok"})
    # Loader used json.loads only; pack bytes are not imported as Python.


def test_cyclic_ref_rejected() -> None:
    schema = {
        "$defs": {
            "a": {"$ref": "#/$defs/b"},
            "b": {"$ref": "#/$defs/a"},
        },
        "$ref": "#/$defs/a",
    }
    with pytest.raises(InvalidConstraintError, match="cyclic"):
        assert_schema_safe(schema)


def test_oversized_payload_rejected() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("mobility_observation", "v1"))
    huge = {"route_id": "x" * (MAX_PAYLOAD_BYTES + 10)}
    with pytest.raises(PolicyViolationError) as exc:
        runtime.validate(ctx, huge)
    assert exc.value.code == "policy_violation"


def test_payload_deeper_than_max_nesting_depth_rejected() -> None:
    runtime = _runtime()
    ctx = runtime.resolve(SchemaRef("mobility_observation", "v1"))
    nested: Any = "leaf"
    for _ in range(MAX_NESTING_DEPTH + 1):
        nested = {"k": nested}
    with pytest.raises(PolicyViolationError) as exc:
        runtime.validate(ctx, nested)
    assert exc.value.code == "policy_violation"
    assert MAX_NESTING_DEPTH == 32


def test_intake_contracts_have_no_schema_binding() -> None:
    text = (GATEWAY_ROOT / "src/core/intake/contracts.py").read_text(encoding="utf-8")
    assert "schema_binding" not in text


def test_intake_services_do_not_call_schema_runtime() -> None:
    text = (GATEWAY_ROOT / "src/core/application/services.py").read_text(encoding="utf-8")
    assert "core.schema" not in text
    assert "LocalSchemaRuntime" not in text
    assert "SchemaRuntime" not in text
