"""Product API request context contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .metadata import RequestMetadata
from .versioning import ApiVersion


@dataclass(frozen=True, slots=True)
class ProductActor:
    """Validated actor identity for a Product API request."""

    account_id: str
    user_id: str


@dataclass(frozen=True, slots=True)
class ProductClient:
    """Client application metadata for a Product API request."""

    client_type: str
    client_version: str | None = None


@dataclass(frozen=True, slots=True)
class ProductDeviceContext:
    """Validated device context for a Product API request."""

    device_id: str | None = None
    device_grant_id: str | None = None


@dataclass(frozen=True, slots=True)
class ProductSessionContext:
    """Validated session context for a Product API request."""

    session_id: str | None = None


@dataclass(frozen=True, slots=True)
class ProductRequestContext:
    """Validated Product API context passed to internal block orchestration.

    This context is not a source of truth for Identity. It carries validated
    Identity-derived identifiers into Product API orchestration.
    """

    actor: ProductActor
    client: ProductClient
    api_version: ApiVersion
    metadata: RequestMetadata = field(default_factory=RequestMetadata)
    device: ProductDeviceContext = field(default_factory=ProductDeviceContext)
    session: ProductSessionContext = field(default_factory=ProductSessionContext)
    extensions: dict[str, Any] = field(default_factory=dict)

    @property
    def request_id(self) -> str:
        """Return the correlation id for the request."""

        return self.metadata.request_id

    @property
    def account_id(self) -> str:
        """Return the account id of the validated actor."""

        return self.actor.account_id

    @property
    def user_id(self) -> str:
        """Return the user id of the validated actor."""

        return self.actor.user_id

    @property
    def device_id(self) -> str | None:
        """Return the device id if the request is associated with a device."""

        return self.device.device_id

    @property
    def device_grant_id(self) -> str | None:
        """Return the device grant id if one was validated."""

        return self.device.device_grant_id

    @property
    def session_id(self) -> str | None:
        """Return the session id if one was validated."""

        return self.session.session_id
