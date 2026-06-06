from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sekretar_identity.entities import (  # noqa: E402
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
from sekretar_identity.enums import DeviceGrantStatus  # noqa: E402
from sekretar_identity.services import IdentityService  # noqa: E402


class InMemoryAccountRepository:
    def __init__(self) -> None:
        self.items: dict[str, Account] = {}

    def add(self, account: Account) -> None:
        self.items[account.id] = account

    def get(self, account_id: str) -> Account | None:
        return self.items.get(account_id)


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.items: dict[str, User] = {}

    def add(self, user: User) -> None:
        self.items[user.id] = user

    def get(self, user_id: str) -> User | None:
        return self.items.get(user_id)


class InMemoryUserProfileRepository:
    def __init__(self) -> None:
        self.items: dict[str, UserProfile] = {}

    def add(self, profile: UserProfile) -> None:
        self.items[profile.id] = profile

    def get_by_user_id(self, user_id: str) -> UserProfile | None:
        return next((p for p in self.items.values() if p.user_id == user_id), None)


class InMemoryAccountMembershipRepository:
    def __init__(self) -> None:
        self.items: dict[str, AccountMembership] = {}

    def add(self, membership: AccountMembership) -> None:
        self.items[membership.id] = membership

    def list_by_account_id(self, account_id: str) -> list[AccountMembership]:
        return [m for m in self.items.values() if m.account_id == account_id]


class InMemoryDeviceRepository:
    def __init__(self) -> None:
        self.items: dict[str, Device] = {}

    def add(self, device: Device) -> None:
        self.items[device.id] = device

    def get(self, device_id: str) -> Device | None:
        return self.items.get(device_id)


class InMemoryDeviceGrantRepository:
    def __init__(self) -> None:
        self.items: dict[str, DeviceGrant] = {}

    def add(self, grant: DeviceGrant) -> None:
        self.items[grant.id] = grant

    def get(self, grant_id: str) -> DeviceGrant | None:
        return self.items.get(grant_id)

    def update(self, grant: DeviceGrant) -> None:
        self.items[grant.id] = grant

    def list_by_account_id(self, account_id: str) -> list[DeviceGrant]:
        return [g for g in self.items.values() if g.account_id == account_id]

    def list_by_status(
        self,
        account_id: str,
        status: DeviceGrantStatus,
    ) -> list[DeviceGrant]:
        return [
            g for g in self.items.values()
            if g.account_id == account_id and g.status is status
        ]


class InMemorySessionRepository:
    def __init__(self) -> None:
        self.items: dict[str, Session] = {}

    def add(self, session: Session) -> None:
        self.items[session.id] = session

    def get(self, session_id: str) -> Session | None:
        return self.items.get(session_id)

    def update(self, session: Session) -> None:
        self.items[session.id] = session


class InMemoryBetaAccessRepository:
    def __init__(self) -> None:
        self.items: dict[str, BetaAccess] = {}

    def add(self, beta_access: BetaAccess) -> None:
        self.items[beta_access.id] = beta_access

    def get_by_code(self, code: str) -> BetaAccess | None:
        return next((b for b in self.items.values() if b.code == code), None)

    def update(self, beta_access: BetaAccess) -> None:
        self.items[beta_access.id] = beta_access


class InMemoryIdentityEventRepository:
    def __init__(self) -> None:
        self.items: dict[str, IdentityEvent] = {}

    def add(self, event: IdentityEvent) -> None:
        self.items[event.id] = event

    def list_by_account_id(self, account_id: str) -> list[IdentityEvent]:
        return [e for e in self.items.values() if e.account_id == account_id]


def make_identity_repositories():
    return {
        "accounts": InMemoryAccountRepository(),
        "users": InMemoryUserRepository(),
        "profiles": InMemoryUserProfileRepository(),
        "memberships": InMemoryAccountMembershipRepository(),
        "devices": InMemoryDeviceRepository(),
        "device_grants": InMemoryDeviceGrantRepository(),
        "sessions": InMemorySessionRepository(),
        "beta_access": InMemoryBetaAccessRepository(),
        "events": InMemoryIdentityEventRepository(),
    }


def make_identity_service(identity_repositories=None):
    if identity_repositories is None:
        identity_repositories = make_identity_repositories()
    return IdentityService(**identity_repositories)


def make_account_user_profile(identity_service):
    return identity_service.create_account_with_user_profile(
        display_name="Test User",
        language="ru",
        timezone="Asia/Novosibirsk",
    )
