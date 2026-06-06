"""Request metadata contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class RequestMetadata:
    """Transport-derived request metadata used by Product API orchestration."""

    request_id: str = field(default_factory=lambda: str(uuid4()))
    ip_address: str | None = None
    user_agent: str | None = None
    locale: str | None = None
    timezone: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
