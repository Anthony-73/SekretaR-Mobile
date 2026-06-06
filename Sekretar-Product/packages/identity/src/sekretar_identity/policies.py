"""Identity policies."""

from __future__ import annotations

from .constants import MAX_ACTIVE_DEVICES_PER_ACCOUNT
from .entities import DeviceGrant
from .enums import DeviceGrantStatus
from .errors import ActiveDeviceLimitExceeded


NON_ACTIVE_GRANT_STATUSES = {
    DeviceGrantStatus.REVOKED,
    DeviceGrantStatus.LOST,
    DeviceGrantStatus.BLOCKED,
    DeviceGrantStatus.REPLACED,
    DeviceGrantStatus.EXPIRED,
}


def count_active_device_grants(grants: list[DeviceGrant]) -> int:
    return sum(1 for grant in grants if grant.status is DeviceGrantStatus.ACTIVE)


def ensure_active_device_grant_limit(
    grants: list[DeviceGrant],
    *,
    limit: int = MAX_ACTIVE_DEVICES_PER_ACCOUNT,
) -> None:
    active_count = count_active_device_grants(grants)
    if active_count >= limit:
        raise ActiveDeviceLimitExceeded(
            f"Account already has {active_count} active device grants; limit is {limit}."
        )
