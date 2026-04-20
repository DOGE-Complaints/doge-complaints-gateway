from __future__ import annotations

from core.projection.enums import SpaIssueStatus, SpaIssueType, SpaLabel


class ProjectionContractError(ValueError):
    """Raised when SPA projection inputs violate governed enums or tx rules."""


def validate_governed_enums(*, status: str, issue_type: str, labels: tuple[str, ...]) -> None:
    if status not in {s.value for s in SpaIssueStatus}:
        raise ProjectionContractError(f"Unknown SPA status: {status!r}.")
    if issue_type not in {t.value for t in SpaIssueType}:
        raise ProjectionContractError(f"Unknown SPA issue type: {issue_type!r}.")
    allowed = {lbl.value for lbl in SpaLabel}
    for label in labels:
        if label not in allowed:
            raise ProjectionContractError(f"Unknown SPA label: {label!r}.")


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
