#!/usr/bin/env python3
"""Apply gateway taxonomy decisions: extraction_policy + optional DOGEIssueLabel (TC4)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.taxonomy.cycle_lib import (  # noqa: E402
    decisions_from_manifest,
    parse_decisions_yaml,
    patch_canonical_mapping,
    patch_doge_issue_label_enum,
)

_GATEWAY_ROOT = Path(__file__).resolve().parents[1]
_EXTRACTION_POLICY = _GATEWAY_ROOT / "src/core/projection/extraction_policy.py"
_ENUMS = _GATEWAY_ROOT / "src/core/projection/enums.py"


from core.taxonomy.cycle_lib import member_name_for_label  # noqa: E402


def _member_name_for_label(value: str) -> str:
    return member_name_for_label(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply gateway taxonomy manifest (TC4).")
    parser.add_argument("--manifest", required=True, type=Path, help="taxonomy-decisions.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Print planned edits without writing.")
    args = parser.parse_args()
    data = parse_decisions_yaml(args.manifest.read_text(encoding="utf-8"))
    decisions = decisions_from_manifest(data)

    policy_text = _EXTRACTION_POLICY.read_text(encoding="utf-8")
    enums_text = _ENUMS.read_text(encoding="utf-8")
    applied = 0

    for decision in decisions:
        if decision.action == "map":
            if not decision.target_label:
                raise SystemExit(f"map decision for {decision.label_key!r} requires target_label.")
            policy_text = patch_canonical_mapping(
                policy_text,
                canonical=decision.label_key,
                spa_label=decision.target_label,
            )
            applied += 1
        elif decision.action == "new_board_label":
            if not decision.new_board_label:
                raise SystemExit(
                    f"new_board_label action for {decision.label_key!r} requires new_board_label: true in manifest."
                )
            if not decision.target_label:
                raise SystemExit(
                    f"new_board_label for {decision.label_key!r} requires target_label (enum value)."
                )
            member = _member_name_for_label(decision.target_label)
            enums_text = patch_doge_issue_label_enum(
                enums_text,
                member_name=member,
                value=decision.target_label,
            )
            policy_text = patch_canonical_mapping(
                policy_text,
                canonical=decision.label_key,
                spa_label=decision.target_label,
            )
            applied += 1
        elif decision.action in ("ignore", "translate_only", "pending"):
            continue
        else:
            raise SystemExit(f"Unsupported gateway action: {decision.action!r}")

    if applied == 0:
        print("No gateway apply actions in manifest.")
        return

    if args.dry_run:
        print(f"Dry-run: would apply {applied} gateway decision(s).")
        return

    _EXTRACTION_POLICY.write_text(policy_text, encoding="utf-8")
    _ENUMS.write_text(enums_text, encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            "-c",
            "from core.projection.extraction_policy import spa_labels_from_canonical; "
            "assert spa_labels_from_canonical(('roads',)) == ('infrastructure',)",
        ],
        cwd=str(_GATEWAY_ROOT / "src"),
        check=True,
    )
    print(f"Applied {applied} gateway decision(s); smoke import OK.")


if __name__ == "__main__":
    main()
