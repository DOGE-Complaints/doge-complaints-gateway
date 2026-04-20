from __future__ import annotations

from typing import Protocol

from core.adapters.types import TxReceipt


class WalletPushAdapter(Protocol):
    """Outbound wallet / device push notification (demo/pilot abstracted)."""

    def push(self, *, channel: str, body: str) -> str:
        """Return opaque message id."""


class SignRequestAdapter(Protocol):
    """Prepare or track a signing request (no real HSM in demo scope)."""

    def request_signature(self, *, payload_digest_hex: str) -> str:
        """Return opaque sign-request id."""


class TxBroadcastAdapter(Protocol):
    """Submit a signed transaction payload (stubbed chain)."""

    def broadcast(self, *, signed_tx_hex: str) -> TxReceipt:
        """Broadcast and return a receipt with deterministic stub tx id."""
