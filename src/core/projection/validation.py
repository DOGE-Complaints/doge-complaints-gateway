from __future__ import annotations

import re

from core.projection.enums import DOGEIssueStatus, DOGEIssueType, DOGEIssueLabel

ARWEAVE_TXID_RE = re.compile(r"^[A-Za-z0-9_-]{43}$")


class ProjectionContractError(ValueError):
    """Raised when SPA projection inputs violate governed enums or tx rules."""


def validate_governed_enums(*, status: str, issue_type: str, labels: tuple[str, ...]) -> None:
    if status not in {s.value for s in DOGEIssueStatus}:
        raise ProjectionContractError(f"Unknown SPA status: {status!r}.")
    if issue_type not in {t.value for t in DOGEIssueType}:
        raise ProjectionContractError(f"Unknown SPA issue type: {issue_type!r}.")
    allowed = {lbl.value for lbl in DOGEIssueLabel}
    for label in labels:
        if label not in allowed:
            raise ProjectionContractError(f"Unknown SPA label: {label!r}.")


def validate_arweave_txid(txid: str) -> bool:
    """Validate Arweave transaction ID format (43 chars base64url). REQ-38 §3."""
    return bool(ARWEAVE_TXID_RE.match(txid))


def validate_optional_tx_fields(
    *,
    arweave_txid: str | None,
    image_txid: str | None,
) -> None:
    """Reject obvious placeholder tx ids; do not generate fake txids in mapper."""
    for name, value in (("arweave_txid", arweave_txid), ("image_txid", image_txid)):
        if value is None:
            continue
        stripped = value.strip()
        if not stripped:
            raise ProjectionContractError(f"{name} cannot be empty string; use null/omit instead.")
        lowered = stripped.lower()
        if lowered in {"fake", "placeholder", "todo"} or stripped == "0x0":
            raise ProjectionContractError(f"{name} looks like a placeholder: {value!r}.")
        if name == "arweave_txid" and not validate_arweave_txid(stripped):
            raise ProjectionContractError(
                f"{name} must be 43 base64url characters; got length {len(stripped)}."
            )
        if name == "image_txid" and not validate_arweave_txid(stripped):
            raise ProjectionContractError(
                f"{name} must be 43 base64url characters; got length {len(stripped)}."
            )
