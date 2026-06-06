"""Identity domain errors."""


class IdentityError(Exception):
    """Base class for identity errors."""


class ActiveDeviceLimitExceeded(IdentityError):
    """Raised when an account already has the maximum number of active grants."""


class AccountNotFound(IdentityError):
    """Raised when an account cannot be found."""


class UserNotFound(IdentityError):
    """Raised when a user cannot be found."""


class DeviceNotFound(IdentityError):
    """Raised when a device cannot be found."""


class GrantNotValid(IdentityError):
    """Raised when a device grant is missing or not valid."""


class BetaAccessInvalid(IdentityError):
    """Raised when beta access cannot be activated."""


class SessionInvalid(IdentityError):
    """Raised when a session is missing or not valid."""
