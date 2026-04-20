from __future__ import annotations

import hashlib
from dataclasses import dataclass

from core.config.schema import DeploymentProfile

from core.adapters.types import TxReceipt


def _digest(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
    return h.hexdigest()[:24]


@dataclass(frozen=True)
class DemoWalletPushAdapter:
    profile: DeploymentProfile

    def push(self, *, channel: str, body: str) -> str:
        return f"push-{_digest(self.profile.value, channel, body)}"


@dataclass(frozen=True)
class DemoSignRequestAdapter:
    profile: DeploymentProfile

    def request_signature(self, *, payload_digest_hex: str) -> str:
        return f"signreq-{_digest(self.profile.value, payload_digest_hex)}"


@dataclass(frozen=True)
class DemoTxBroadcastAdapter:
    profile: DeploymentProfile

    def broadcast(self, *, signed_tx_hex: str) -> TxReceipt:
        tx_id = f"tx-{_digest(self.profile.value, signed_tx_hex)}"
        return TxReceipt(tx_id=tx_id, status="stub_submitted", chain_profile=self.profile.value)
