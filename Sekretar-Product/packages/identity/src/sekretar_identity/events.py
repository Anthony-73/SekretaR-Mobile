"""Identity event helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .entities import IdentityEvent
from .enums import IdentityEventType


def create_identity_event(
    event_type: IdentityEventType,
    *,
    account_id: str | None = None,
    user_id: str | None = None,
    device_id: str | None = None,
    session_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> IdentityEvent:
    return IdentityEvent(
        id=str(uuid4()),
        event_type=event_type,
        account_id=account_id,
        user_id=user_id,
        device_id=device_id,
        session_id=session_id,
        metadata=metadata or {},
        created_at=datetime.now(timezone.utc),
    )
