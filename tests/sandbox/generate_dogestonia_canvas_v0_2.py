#!/usr/bin/env python3
"""Generate dogestonia_simulation_canvas_v0_2.json for GW-SEED-02 (dense clusters)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

OUTPUT = Path(__file__).resolve().parent / "dogestonia_simulation_canvas_v0_2.json"

CLUSTER_SPECS: tuple[dict[str, Any], ...] = (
    {
        "cluster_id": "C1-waste-kalamaja",
        "scenario_group": "environment",
        "scenario_subgroup": "waste_bins_kalamaja",
        "civic_domain": "waste",
        "labels": [
            "waste",
            "environment",
            "safety",
            "maintenance_gap",
            "recurring_issue",
            "residents",
        ],
        "location_query": "yard waste bins, Tallinn, Estonia (kalamaja_waste_cluster_v02)",
        "title_en": "Overflowing waste bins in Kalamaja courtyard",
        "title_et": "Ülevoolvad prügikastid Kalamaja hoovis",
        "title_ru": "Переполненные мусорные баки во дворе Каламая",
        "summary_en": "Residents report bins overflowing again in the same Kalamaja block.",
        "personas": ("parent_worried", "elderly_resident_practical", "tenant_calm"),
        "languages": ("en", "et", "ru"),
        "count": 9,
        "id_prefix": "DOGE-EST-V02-W",
    },
    {
        "cluster_id": "C2-roads-lasnamae",
        "scenario_group": "infrastructure",
        "scenario_subgroup": "road_potholes_lasnamae",
        "civic_domain": "roads",
        "labels": [
            "roads",
            "safety",
            "broken_infrastructure",
            "unsafe_condition",
            "recurring_issue",
            "pedestrians",
        ],
        "location_query": "pothole street, Tallinn, Estonia (lasnamae_roads_cluster_v02)",
        "title_en": "Potholes on Lasnamäe residential street",
        "title_et": "Augud Lasnamäe elamutänaval",
        "title_ru": "Выбоины на жилой улице в Ласнамяэ",
        "summary_en": "Pedestrians report recurring potholes on the same Lasnamäe route.",
        "personas": ("parent_worried", "cyclist_practical", "commuter_frustrated"),
        "languages": ("en", "et", "ru"),
        "count": 9,
        "id_prefix": "DOGE-EST-V02-R",
    },
)


def _scenario(
    *,
    simulation_id: str,
    spec: dict[str, Any],
    variant_index: int,
    lang: str,
    persona: str,
) -> dict[str, Any]:
    summary_en = str(spec["summary_en"])
    variant_suffix = f" Report variant {variant_index + 1}."
    summary = {
        "en": summary_en + variant_suffix,
        "et": summary_en + variant_suffix,
        "ru": summary_en + variant_suffix,
    }
    title = {
        "en": spec["title_en"],
        "et": spec["title_et"],
        "ru": spec["title_ru"],
    }
    labels = list(spec["labels"])
    return {
        "simulation_id": simulation_id,
        "scenario_group": spec["scenario_group"],
        "scenario_subgroup": spec["scenario_subgroup"],
        "resident_profile": {
            "persona_key": persona,
            "role": "resident",
            "language": lang,
            "tone": "frustrated" if variant_index % 2 else "calm",
            "precision_level": "medium",
        },
        "resident_input": {
            "raw_message": summary["en"],
            "input_quality": "complete",
            "noise_profile": ["emotional_language"] if variant_index % 3 == 0 else [],
            "noise_level": "medium",
            "has_location": True,
            "has_time_context": True,
            "has_desired_outcome": variant_index % 4 != 0,
            "has_photo_reference": False,
            "location_query": spec["location_query"],
        },
        "interview_context": {
            "missing_information": [],
            "clarification_questions_expected": [],
            "phase_7_confirmation_needed": False,
            "accepted_uncertainty": [],
        },
        "expected_interview_path": {
            "phase_1_entry": f"Resident reports civic signal for {spec['cluster_id']}.",
            "phase_7_summary": summary["en"],
        },
        "normalized_issue_payload": {
            "canonical_payload": {
                "type": "complaint",
                "labels": labels,
                "title": title,
                "summary": summary,
                "description": {
                    "en": summary["en"] + " Cluster seed v0_2 dense variant.",
                    "et": summary["et"] + " Cluster seed v0_2 dense variant.",
                    "ru": summary["ru"] + " Cluster seed v0_2 dense variant.",
                },
            },
            "normalization_metadata": {
                "session_language": lang,
                "ingest_validation_report_ref": f"sim_validation_{simulation_id}",
                "safety_compliance_report_ref": f"sim_safety_{simulation_id}",
                "policy_gate_ref": {
                    "policy_ref": "simulated_operator_rulebook",
                    "rulebook_version": "simulation-v1",
                    "status": "approved",
                },
            },
        },
        "cluster_metadata": {
            "primary_cluster_key": f"{spec['cluster_id']}_ignored_by_gateway",
            "cluster_type": "seed_v02_dense",
        },
        "test_metadata": {
            "seed_cluster_target": spec["cluster_id"],
            "variant_index": variant_index,
        },
    }


def build_canvas() -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for spec in CLUSTER_SPECS:
        personas = tuple(spec["personas"])
        languages = tuple(spec["languages"])
        for i in range(int(spec["count"])):
            sim_id = f"{spec['id_prefix']}{i + 1:03d}"
            scenarios.append(
                _scenario(
                    simulation_id=sim_id,
                    spec=spec,
                    variant_index=i,
                    lang=languages[i % len(languages)],
                    persona=personas[i % len(personas)],
                )
            )
    return scenarios


def main() -> None:
    canvas = build_canvas()
    OUTPUT.write_text(json.dumps(canvas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(canvas)} scenarios to {OUTPUT}")


if __name__ == "__main__":
    main()
