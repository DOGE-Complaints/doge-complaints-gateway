from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TxReceipt:
    """Result of a (stub) on-chain broadcast."""

    tx_id: str
    status: str
    chain_profile: str
