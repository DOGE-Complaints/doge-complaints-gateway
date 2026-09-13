"""GW-SSR-28: tallinn_civic/v1 taxonomy.json seed from GPT SSOT (no invent)."""

from __future__ import annotations

import json
from pathlib import Path

from core.cluster.types import ClusterLens
from core.cluster.vocabulary import CIVIC_DOMAIN_VOCABULARY, FAILURE_PATTERN_VOCABULARY
from core.schema import SchemaRef
from core.schema.contracts import TaxonomyPack
from core.schema.resolver import resolve_pack
from core.taxonomy.axes import TAXONOMY_AXIS_VALUES
from helpers.ssr28_gpt_taxonomy_extract import (
    assert_no_silent_rename_vs_prior,
    default_gpt_taxonomy_md,
    extract_canonical_inventory,
    inventory_key_sets,
)

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"
TALLINN_DIR = PACKS_ROOT / "tallinn_civic" / "v1"


def test_clusterlens_baseline_unchanged() -> None:
    assert len(ClusterLens) == 10


def test_manifest_declares_taxonomy_schema() -> None:
    manifest = json.loads((TALLINN_DIR / "pack.json").read_text(encoding="utf-8"))
    assert manifest["taxonomy_schema"] == "taxonomy.json"
    tax_path = TALLINN_DIR / manifest["taxonomy_schema"]
    assert tax_path.is_file()
    assert tax_path.read_bytes().endswith(b"\n")


def test_taxonomy_axes_seed_content_thirteen() -> None:
    """SSR-28 seed invariant: tallinn taxonomy.json *content* has reference 13 axes.

    Contour2 loader (SSR-31) no longer rejects packs with other axis sets;
    this assert is data lockstep for the official tallinn seed only.
    """
    body = json.loads((TALLINN_DIR / "taxonomy.json").read_text(encoding="utf-8"))
    assert body["schema_id"] == "tallinn_civic"
    assert body["schema_version"] == "v1"
    assert set(body["axes"]) == TAXONOMY_AXIS_VALUES
    assert len(body["axes"]) == 13
    assert set(body["internal_axes"]) == {
        "risk_privacy_safety",
        "confidence_state",
    }


def test_required_signals_covered_by_axis_to_signal_map() -> None:
    """AC-GW-SSR28-04."""
    manifest = json.loads((TALLINN_DIR / "pack.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((TALLINN_DIR / "taxonomy.json").read_text(encoding="utf-8"))
    required_signals = {
        path
        for path, state in manifest["field_policy"].items()
        if state == "required" and path.startswith("signals.")
    }
    mapped = set(taxonomy["axis_to_signal_map"].values())
    assert required_signals <= mapped


def test_canonical_keys_inventory_matches_gpt_md_section_four() -> None:
    """AC-GW-SSR28-05 — section-scoped §4/§5/§6; HARD STOP on silent rename."""
    md = default_gpt_taxonomy_md(GATEWAY_ROOT).read_text(encoding="utf-8")
    inventory = extract_canonical_inventory(md)
    expected = inventory_key_sets(inventory)

    body = json.loads((TALLINN_DIR / "taxonomy.json").read_text(encoding="utf-8"))
    on_disk = {
        axis: frozenset(entry["key"] for entry in entries)
        for axis, entries in body["canonical_keys"].items()
    }
    assert on_disk == expected
    # Explicit HARD STOP path vs live GPT extract (prior export = on-disk).
    assert_no_silent_rename_vs_prior(expected, on_disk)


def test_vocabulary_overlap_axes_subset_of_taxonomy_keys() -> None:
    body = json.loads((TALLINN_DIR / "taxonomy.json").read_text(encoding="utf-8"))
    topic_keys = {e["key"] for e in body["canonical_keys"]["topic_domain"]}
    failure_keys = {e["key"] for e in body["canonical_keys"]["failure_mode"]}
    assert CIVIC_DOMAIN_VOCABULARY <= topic_keys
    assert FAILURE_PATTERN_VOCABULARY <= failure_keys


def test_tallinn_resolve_requires_taxonomy_pack() -> None:
    """AC-GW-SSR28-06 — resolve_pack loads TaxonomyPack for tallinn.

    Axes equality to TAXONOMY_AXIS_VALUES is tallinn *seed content* (SSR-31),
    not a Contour2 loader reject rule for arbitrary packs.
    """
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert isinstance(ctx.taxonomy, TaxonomyPack)
    assert ctx.taxonomy.schema_id == "tallinn_civic"
    assert set(ctx.taxonomy.axes) == TAXONOMY_AXIS_VALUES
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    mobility = resolve_pack(
        SchemaRef("mobility_observation", "v1"), packs_root=PACKS_ROOT
    )
    assert legal.taxonomy is None
    assert mobility.taxonomy is None
