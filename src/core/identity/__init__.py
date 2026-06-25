"""Gateway → identity OAuth introspection (GW-GAUTH-02)."""

from core.identity.introspection_client import (
    IdentityIntrospectionClient,
    IdentityIntrospectionError,
    IntrospectionResult,
    build_identity_introspection_from_config,
)

__all__ = [
    "IdentityIntrospectionClient",
    "IdentityIntrospectionError",
    "IntrospectionResult",
    "build_identity_introspection_from_config",
]
