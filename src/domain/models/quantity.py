from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import domain.exceptions as exception


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable Value Object representing a non-negative asset quantity."""

    units: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.units, Decimal):
            raise TypeError("units must be a Decimal instance")
        if not self.units.is_finite():
            raise exception.InvalidQuantityError()
        if self.units < Decimal("0"):
            raise exception.InvalidQuantityError()

    def __str__(self) -> str:
        return str(self.units)

    def __add__(self, other: object) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        return Quantity(self.units + other.units)

    def __sub__(self, other: object) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        if self < other:
            raise exception.InvalidQuantityError()
        return Quantity(self.units - other.units)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.units < other.units

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.units <= other.units
