"""Adapter protocols for future Product API transports and block gateways."""

from __future__ import annotations

from typing import Protocol, TypeVar

from .context import ProductRequestContext
from .responses import ProductResponse

T = TypeVar("T")


class ProductOperation(Protocol[T]):
    """Callable contract for a Product API operation.

    Implementations may call internal blocks, but Product API foundation remains
    transport-agnostic and framework-agnostic.
    """

    def __call__(self, context: ProductRequestContext) -> ProductResponse[T]: ...
