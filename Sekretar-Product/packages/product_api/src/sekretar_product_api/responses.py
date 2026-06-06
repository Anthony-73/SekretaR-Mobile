"""Product API response contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from .errors import ProductError

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ProductResponse(Generic[T]):
    """Transport-agnostic response envelope for Product API operations."""

    success: bool
    data: T | None = None
    error: ProductError | None = None
    request_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        data: T,
        *,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ProductResponse[T]":
        """Create a successful Product API response."""

        return cls(
            success=True,
            data=data,
            error=None,
            request_id=request_id,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        error: ProductError,
        *,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ProductResponse[None]":
        """Create a failed Product API response."""

        return cls(
            success=False,
            data=None,
            error=error,
            request_id=request_id,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation of the response."""

        return {
            "success": self.success,
            "data": self.data,
            "error": self.error.to_dict() if self.error else None,
            "request_id": self.request_id,
            "metadata": self.metadata,
        }
