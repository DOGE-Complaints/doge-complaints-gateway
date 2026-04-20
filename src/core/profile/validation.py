from __future__ import annotations

from core.domain import SignalProfileRecord
from core.profile.schema import REQUIRED_SIGNAL_DIMENSIONS


def validate_profile_minimum_quality(profile: SignalProfileRecord) -> list[str]:
    errors: list[str] = []

    if profile.version < 1:
        errors.append("Profile version must start from 1.")

    for dimension in REQUIRED_SIGNAL_DIMENSIONS:
        key = dimension.value
        user_value = profile.user_asserted.get(key, "").strip()
        inferred_value = profile.system_inferred.get(key, "").strip()
        if not user_value and not inferred_value:
            errors.append(f"Missing both user_asserted and system_inferred for {key}.")

    for key in profile.user_asserted:
        if key in profile.system_inferred and (
            profile.user_asserted[key].strip() == profile.system_inferred[key].strip()
        ):
            errors.append(f"Duplicate user/system value for {key}.")

    return errors

