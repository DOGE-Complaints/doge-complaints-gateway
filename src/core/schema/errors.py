"""Typed Schema Runtime errors (REQ3-RUNTIME-005)."""

from __future__ import annotations


class SchemaRuntimeError(ValueError):
    """Base validation/resolve failure. ``code`` distinguishes RUNTIME-005 classes."""

    code: str = "schema_runtime_error"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code


class UnknownSchemaError(SchemaRuntimeError):
    code = "unknown_schema"


class UnsupportedVersionError(SchemaRuntimeError):
    code = "unsupported_version"


class InvalidTypeError(SchemaRuntimeError):
    code = "invalid_type"


class MissingRequiredError(SchemaRuntimeError):
    code = "missing_required"


class ForbiddenFieldError(SchemaRuntimeError):
    code = "forbidden"


class InvalidConstraintError(SchemaRuntimeError):
    code = "invalid_constraint"


class PolicyViolationError(SchemaRuntimeError):
    code = "policy_violation"


class ProfileIncompatibilityError(SchemaRuntimeError):
    code = "profile_incompatibility"
