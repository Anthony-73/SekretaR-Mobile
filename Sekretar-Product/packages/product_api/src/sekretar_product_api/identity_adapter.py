"""Identity-to-Product API mapping helpers.

This module translates Identity errors into Product API errors. It must not
implement login, session validation, device grant policy, beta activation, or
any other Identity business logic.
"""

from __future__ import annotations

from sekretar_identity.errors import (
    AccountNotFound,
    ActiveDeviceLimitExceeded,
    BetaAccessInvalid,
    DeviceNotFound,
    GrantNotValid,
    IdentityError,
    SessionInvalid,
    UserNotFound,
)

from .errors import ProductError, ProductErrorCode


def map_identity_error(error: IdentityError) -> ProductError:
    """Map an Identity-layer error into a Product API error envelope."""

    if isinstance(error, (AccountNotFound, UserNotFound)):
        return ProductError(
            code=ProductErrorCode.IDENTITY_NOT_FOUND,
            message=str(error),
            category="identity",
        )

    if isinstance(error, DeviceNotFound):
        return ProductError(
            code=ProductErrorCode.DEVICE_NOT_REGISTERED,
            message=str(error),
            category="identity",
        )

    if isinstance(error, GrantNotValid):
        return ProductError(
            code=ProductErrorCode.DEVICE_GRANT_INVALID,
            message=str(error),
            category="identity",
        )

    if isinstance(error, ActiveDeviceLimitExceeded):
        return ProductError(
            code=ProductErrorCode.DEVICE_LIMIT_EXCEEDED,
            message=str(error),
            category="identity",
        )

    if isinstance(error, SessionInvalid):
        return ProductError(
            code=ProductErrorCode.SESSION_INVALID,
            message=str(error),
            category="identity",
        )

    if isinstance(error, BetaAccessInvalid):
        return ProductError(
            code=ProductErrorCode.ACCESS_DENIED,
            message=str(error),
            category="identity",
        )

    return ProductError(
        code=ProductErrorCode.INTERNAL_ERROR,
        message=str(error),
        category="identity",
    )
