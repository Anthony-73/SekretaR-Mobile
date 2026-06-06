"""SekretaR Product API foundation package."""

from .context import (
    ProductActor,
    ProductClient,
    ProductDeviceContext,
    ProductRequestContext,
    ProductSessionContext,
)
from .errors import ProductError, ProductErrorCode
from .metadata import RequestMetadata
from .responses import ProductResponse
from .versioning import ApiVersion

__all__ = [
    "ApiVersion",
    "ProductActor",
    "ProductClient",
    "ProductDeviceContext",
    "ProductError",
    "ProductErrorCode",
    "ProductRequestContext",
    "ProductResponse",
    "ProductSessionContext",
    "RequestMetadata",
]
