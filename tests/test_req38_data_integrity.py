from __future__ import annotations

import pytest

from core.projection.validation import (
    ProjectionContractError,
    validate_arweave_txid,
    validate_optional_tx_fields,
)


def test_validate_arweave_txid_valid_43_chars() -> None:
    valid = "a" * 43
    assert validate_arweave_txid(valid) is True


def test_validate_arweave_txid_short() -> None:
    assert validate_arweave_txid("short") is False


def test_validate_arweave_txid_invalid_chars() -> None:
    assert validate_arweave_txid("!" * 43) is False


def test_validate_optional_tx_fields_rejects_invalid_arweave_txid() -> None:
    with pytest.raises(ProjectionContractError):
        validate_optional_tx_fields(arweave_txid="not-valid", image_txid=None)


def test_validate_optional_tx_fields_accepts_valid_arweave_txid() -> None:
    validate_optional_tx_fields(
        arweave_txid="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopq",
        image_txid=None,
    )
