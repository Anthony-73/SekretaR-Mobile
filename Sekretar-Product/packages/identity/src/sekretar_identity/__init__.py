"""SekretaR Identity foundation package."""

from .constants import MAX_ACTIVE_DEVICES_PER_ACCOUNT
from .entities import (
    Account,
    AccountMembership,
    BetaAccess,
    Device,
    DeviceGrant,
    IdentityEvent,
    Session,
    User,
    UserProfile,
)
from .enums import (
    BetaAccessStatus,
    ClientType,
    DeviceGrantStatus,
    IdentityEventType,
    SessionStatus,
)
from .services import IdentityService

__all__ = [
    "Account",
    "AccountMembership",
    "BetaAccess",
    "BetaAccessStatus",
    "ClientType",
    "Device",
    "DeviceGrant",
    "DeviceGrantStatus",
    "IdentityEvent",
    "IdentityEventType",
    "IdentityService",
    "MAX_ACTIVE_DEVICES_PER_ACCOUNT",
    "Session",
    "SessionStatus",
    "User",
    "UserProfile",
]
