from __future__ import annotations

from dataclasses import dataclass

from core.config.schema import AppConfig

from core.adapters.demo import (
    DemoSignRequestAdapter,
    DemoTxBroadcastAdapter,
    DemoWalletPushAdapter,
)
from core.adapters.protocols import SignRequestAdapter, TxBroadcastAdapter, WalletPushAdapter


@dataclass(frozen=True)
class AdapterBundle:
    """All pilot-ready adapter surfaces wired to the same deployment profile."""

    wallet_push: WalletPushAdapter
    sign_request: SignRequestAdapter
    tx_broadcast: TxBroadcastAdapter


def build_adapter_bundle(config: AppConfig) -> AdapterBundle:
    """Resolve demo in-memory adapters; profile comes from centralized config.

    Pilot profile uses the same stub implementations (deterministic, no chain);
    swap real adapters later without changing call sites.
    """
    profile = config.profile
    return AdapterBundle(
        wallet_push=DemoWalletPushAdapter(profile=profile),
        sign_request=DemoSignRequestAdapter(profile=profile),
        tx_broadcast=DemoTxBroadcastAdapter(profile=profile),
    )


def adapter_runtime_flags(config: AppConfig) -> dict[str, str | bool]:
    """Feature-flag + profile snapshot for deterministic adapter mode (demo vs pilot)."""
    return {
        "deployment_profile": config.profile.value,
        "wallet_adapter": config.flags.wallet_adapter,
        "blockchain_adapter": config.flags.blockchain_adapter,
        "tokenization_pipeline": config.flags.tokenization_pipeline,
    }
