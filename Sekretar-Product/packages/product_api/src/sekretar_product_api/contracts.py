"""Shared Product API contract primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Pagination:
    """Pagination contract shared by future Product API list operations."""

    limit: int = 50
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit <= 0:
            raise ValueError("Pagination limit must be positive.")
        if self.offset < 0:
            raise ValueError("Pagination offset must be non-negative.")


@dataclass(frozen=True, slots=True)
class ContractMetadata:
    """Optional metadata for Product API contracts."""

    values: dict[str, Any] = field(default_factory=dict)
