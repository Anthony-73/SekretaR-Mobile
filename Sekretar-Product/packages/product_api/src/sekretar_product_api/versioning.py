"""API version primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiVersion:
    """Semantic version marker for Product API contracts."""

    major: int
    minor: int = 0

    def __post_init__(self) -> None:
        if self.major < 0 or self.minor < 0:
            raise ValueError("API version numbers must be non-negative.")

    @classmethod
    def parse(cls, value: str) -> "ApiVersion":
        """Parse a version string like '1' or '1.0'."""

        parts = value.strip().split(".")
        if len(parts) == 1:
            return cls(major=int(parts[0]), minor=0)
        if len(parts) == 2:
            return cls(major=int(parts[0]), minor=int(parts[1]))
        raise ValueError(f"Unsupported API version format: {value}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"
