"""Identity enumerations."""

from enum import Enum


class ClientType(str, Enum):
    WEB = "web"
    ANDROID_RECORDER = "android_recorder"
    BROWSER_RECORDER = "browser_recorder"
    DESKTOP_RECORDER = "desktop_recorder"
    IOS_RECORDER = "ios_recorder"
    UNKNOWN = "unknown"


class DeviceGrantStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    LOST = "lost"
    BLOCKED = "blocked"
    REPLACED = "replaced"
    EXPIRED = "expired"


class SessionStatus(str, Enum):
    ACTIVE = "active"
    LOGGED_OUT = "logged_out"
    EXPIRED = "expired"


class BetaAccessStatus(str, Enum):
    AVAILABLE = "available"
    ACTIVATED = "activated"
    REVOKED = "revoked"
    EXPIRED = "expired"


class IdentityEventType(str, Enum):
    ACCOUNT_CREATED = "account_created"
    USER_CREATED = "user_created"
    USER_LOGGED_IN = "user_logged_in"
    USER_LOGGED_OUT = "user_logged_out"
    DEVICE_REGISTERED = "device_registered"
    DEVICE_GRANT_CREATED = "device_grant_created"
    DEVICE_GRANT_REVOKED = "device_grant_revoked"
    BETA_ACCESS_ACTIVATED = "beta_access_activated"
    SESSION_CREATED = "session_created"
    SESSION_EXPIRED = "session_expired"
