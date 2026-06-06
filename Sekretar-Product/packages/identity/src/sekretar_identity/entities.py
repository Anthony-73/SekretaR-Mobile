"""Identity entities.

These are persistence-agnostic business entities. They intentionally do not
depend on FastAPI, SQLAlchemy, or any database layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .enums import (
    BetaAccessStatus,
    ClientType,
    DeviceGrantStatus,
    IdentityEventType,
    SessionStatus,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid4())


@dataclass(slots=True)
class Account:
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    is_active: bool = True


@dataclass(slots=True)
class User:
    account_id: str
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    is_active: bool = True


@dataclass(slots=True)
class UserProfile:
    user_id: str
    display_name: str
    language: str = "ru"
    timezone: str = "UTC"
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)


@dataclass(slots=True)
class AccountMembership:
    account_id: str
    user_id: str
    role: str = "owner"
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    is_active: bool = True


@dataclass(slots=True)
class Device:
    client_type: ClientType
    display_name: str | None = None
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    last_seen_at: datetime | None = None


@dataclass(slots=True)
class DeviceGrant:
    account_id: str
    user_id: str
    device_id: str
    status: DeviceGrantStatus = DeviceGrantStatus.ACTIVE
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    @property
    def is_active(self) -> bool:
        return self.status is DeviceGrantStatus.ACTIVE


@dataclass(slots=True)
class Session:
    account_id: str
    user_id: str
    device_id: str | None = None
    device_grant_id: str | None = None
    status: SessionStatus = SessionStatus.ACTIVE
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    expires_at: datetime | None = None
    ended_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.status is SessionStatus.ACTIVE


@dataclass(slots=True)
class BetaAccess:
    code: str
    account_id: str | None = None
    user_id: str | None = None
    status: BetaAccessStatus = BetaAccessStatus.AVAILABLE
    id: str = field(default_factory=new_id)
    created_at: datetime = field(default_factory=utcnow)
    activated_at: datetime | None = None

    @property
    def is_available(self) -> bool:
        return self.status is BetaAccessStatus.AVAILABLE


@dataclass(slots=True)
class IdentityEvent:
    event_type: IdentityEventType
    id: str = field(default_factory=new_id)
    account_id: str | None = None
    user_id: str | None = None
    device_id: str | None = None
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utcnow)
