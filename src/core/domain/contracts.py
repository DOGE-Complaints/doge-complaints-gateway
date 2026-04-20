from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class HealthReport:
    status: str


class HealthRepository(Protocol):
    def get_health(self) -> HealthReport:
        """Return current health snapshot."""

