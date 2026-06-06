"""Identity service layer.

The service coordinates Identity entities through repository interfaces. It is
framework-agnostic and persistence-agnostic by design.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .entities import (
    Account,
    AccountMembership,
    BetaAccess,
    Device,
    DeviceGrant,
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
from .errors import (
    AccountNotFound,
    BetaAccessInvalid,
    DeviceNotFound,
    GrantNotValid,
    SessionInvalid,
    UserNotFound,
)
from .events import create_identity_event
from .policies import ensure_active_device_grant_limit
from .repositories import (
    AccountMembershipRepository,
    AccountRepository,
    BetaAccessRepository,
    DeviceGrantRepository,
    DeviceRepository,
    IdentityEventRepository,
    SessionRepository,
    UserProfileRepository,
    UserRepository,
)


class IdentityService:
    def __init__(
        self,
        *,
        accounts: AccountRepository,
        users: UserRepository,
        profiles: UserProfileRepository,
        memberships: AccountMembershipRepository,
        devices: DeviceRepository,
        device_grants: DeviceGrantRepository,
        sessions: SessionRepository,
        beta_access: BetaAccessRepository,
        events: IdentityEventRepository,
    ) -> None:
        self.accounts = accounts
        self.users = users
        self.profiles = profiles
        self.memberships = memberships
        self.devices = devices
        self.device_grants = device_grants
        self.sessions = sessions
        self.beta_access = beta_access
        self.events = events

    def create_account_with_user_profile(
        self,
        *,
        display_name: str,
        language: str = "ru",
        timezone: str = "UTC",
    ) -> tuple[Account, User, UserProfile, AccountMembership]:
        account = Account()
        user = User(account_id=account.id)
        profile = UserProfile(
            user_id=user.id,
            display_name=display_name,
            language=language,
            timezone=timezone,
        )
        membership = AccountMembership(account_id=account.id, user_id=user.id)

        self.accounts.add(account)
        self.users.add(user)
        self.profiles.add(profile)
        self.memberships.add(membership)

        self._record_event(IdentityEventType.ACCOUNT_CREATED, account_id=account.id)
        self._record_event(
            IdentityEventType.USER_CREATED,
            account_id=account.id,
            user_id=user.id,
        )

        return account, user, profile, membership

    def register_device(
        self,
        *,
        client_type: ClientType,
        display_name: str | None = None,
    ) -> Device:
        device = Device(client_type=client_type, display_name=display_name)
        self.devices.add(device)
        self._record_event(
            IdentityEventType.DEVICE_REGISTERED,
            device_id=device.id,
            metadata={"client_type": client_type.value},
        )
        return device

    def create_device_grant(
        self,
        *,
        account_id: str,
        user_id: str,
        device_id: str,
    ) -> DeviceGrant:
        self._ensure_account(account_id)
        self._ensure_user_in_account(account_id, user_id)
        self._ensure_device(device_id)

        existing_grants = self.device_grants.list_by_account_id(account_id)
        ensure_active_device_grant_limit(existing_grants)

        grant = DeviceGrant(
            account_id=account_id,
            user_id=user_id,
            device_id=device_id,
            status=DeviceGrantStatus.ACTIVE,
        )
        self.device_grants.add(grant)
        self._record_event(
            IdentityEventType.DEVICE_GRANT_CREATED,
            account_id=account_id,
            user_id=user_id,
            device_id=device_id,
            metadata={"device_grant_id": grant.id},
        )
        return grant

    def update_device_grant_status(
        self,
        *,
        grant_id: str,
        status: DeviceGrantStatus,
    ) -> DeviceGrant:
        grant = self.device_grants.get(grant_id)
        if grant is None:
            raise GrantNotValid(f"Device grant not found: {grant_id}")

        grant.status = status
        grant.updated_at = datetime.now(timezone.utc)
        self.device_grants.update(grant)

        if status is DeviceGrantStatus.REVOKED:
            self._record_event(
                IdentityEventType.DEVICE_GRANT_REVOKED,
                account_id=grant.account_id,
                user_id=grant.user_id,
                device_id=grant.device_id,
                metadata={"device_grant_id": grant.id},
            )

        return grant

    def create_session(
        self,
        *,
        account_id: str,
        user_id: str,
        device_id: str | None = None,
        device_grant_id: str | None = None,
        expires_at: datetime | None = None,
    ) -> Session:
        self._ensure_account(account_id)
        self._ensure_user_in_account(account_id, user_id)

        if device_id is not None:
            self._ensure_device(device_id)

        if device_grant_id is not None:
            grant = self.device_grants.get(device_grant_id)
            if grant is None or not grant.is_active:
                raise GrantNotValid("Session requires an active device grant.")

        session = Session(
            account_id=account_id,
            user_id=user_id,
            device_id=device_id,
            device_grant_id=device_grant_id,
            expires_at=expires_at,
        )
        self.sessions.add(session)
        self._record_event(
            IdentityEventType.SESSION_CREATED,
            account_id=account_id,
            user_id=user_id,
            device_id=device_id,
            session_id=session.id,
        )
        self._record_event(
            IdentityEventType.USER_LOGGED_IN,
            account_id=account_id,
            user_id=user_id,
            device_id=device_id,
            session_id=session.id,
        )
        return session

    def logout_session(self, session_id: str) -> Session:
        session = self.sessions.get(session_id)
        if session is None:
            raise SessionInvalid(f"Session not found: {session_id}")

        session.status = SessionStatus.LOGGED_OUT
        session.ended_at = datetime.now(timezone.utc)
        self.sessions.update(session)
        self._record_event(
            IdentityEventType.USER_LOGGED_OUT,
            account_id=session.account_id,
            user_id=session.user_id,
            device_id=session.device_id,
            session_id=session.id,
        )
        return session

    def expire_session(self, session_id: str) -> Session:
        session = self.sessions.get(session_id)
        if session is None:
            raise SessionInvalid(f"Session not found: {session_id}")

        session.status = SessionStatus.EXPIRED
        session.ended_at = datetime.now(timezone.utc)
        self.sessions.update(session)
        self._record_event(
            IdentityEventType.SESSION_EXPIRED,
            account_id=session.account_id,
            user_id=session.user_id,
            device_id=session.device_id,
            session_id=session.id,
        )
        return session

    def create_beta_access_code(self, *, code: str) -> BetaAccess:
        beta_access = BetaAccess(code=code)
        self.beta_access.add(beta_access)
        return beta_access

    def activate_beta_access(
        self,
        *,
        code: str,
        account_id: str,
        user_id: str,
    ) -> BetaAccess:
        self._ensure_account(account_id)
        self._ensure_user_in_account(account_id, user_id)

        beta_access = self.beta_access.get_by_code(code)
        if beta_access is None or not beta_access.is_available:
            raise BetaAccessInvalid(f"Beta access cannot be activated: {code}")

        beta_access.account_id = account_id
        beta_access.user_id = user_id
        beta_access.status = BetaAccessStatus.ACTIVATED
        beta_access.activated_at = datetime.now(timezone.utc)
        self.beta_access.update(beta_access)

        self._record_event(
            IdentityEventType.BETA_ACCESS_ACTIVATED,
            account_id=account_id,
            user_id=user_id,
            metadata={"beta_access_id": beta_access.id},
        )
        return beta_access

    def _ensure_account(self, account_id: str) -> Account:
        account = self.accounts.get(account_id)
        if account is None:
            raise AccountNotFound(f"Account not found: {account_id}")
        return account

    def _ensure_device(self, device_id: str) -> Device:
        device = self.devices.get(device_id)
        if device is None:
            raise DeviceNotFound(f"Device not found: {device_id}")
        return device

    def _ensure_user_in_account(self, account_id: str, user_id: str) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFound(f"User not found: {user_id}")
        if user.account_id != account_id:
            raise UserNotFound(f"User {user_id} does not belong to account {account_id}")

        memberships = self.memberships.list_by_account_id(account_id)
        if not any(m.user_id == user_id and m.is_active for m in memberships):
            raise UserNotFound(f"User {user_id} is not an active account member")

        return user

    def _record_event(self, event_type: IdentityEventType, **kwargs: object) -> None:
        event = create_identity_event(event_type, **kwargs)  # type: ignore[arg-type]
        self.events.add(event)
