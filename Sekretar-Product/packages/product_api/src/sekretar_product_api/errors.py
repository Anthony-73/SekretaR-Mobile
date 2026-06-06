"""Product API error contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProductErrorCode(str, Enum):
    """Stable error codes exposed by the Product API layer."""

    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_REQUIRED = "authentication_required"
    IDENTITY_NOT_FOUND = "identity_not_found"
    DEVICE_NOT_REGISTERED = "device_not_registered"
    DEVICE_GRANT_INVALID = "device_grant_invalid"
    DEVICE_LIMIT_EXCEEDED = "device_limit_exceeded"
    SESSION_INVALID = "session_invalid"
    ACCESS_DENIED = "access_denied"
    CAPABILITY_REQUIRED = "capability_required"
    RATE_LIMITED = "rate_limited"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNSUPPORTED_CLIENT = "unsupported_client"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"


@dataclass(frozen=True, slots=True)
class ProductError:
    """Framework-agnostic Product API error envelope."""

    code: ProductErrorCode
    message: str
    category: str = "product_api"
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation of the error."""

        return {
            "code": self.code.value,
            "message": self.message,
            "category": self.category,
            "details": self.details,
        }
