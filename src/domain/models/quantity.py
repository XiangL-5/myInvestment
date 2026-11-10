from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import domain.exceptions as exception


@dataclass(frozen=True, slots=True)
class Quantity:
    units: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.units, Decimal):
            raise TypeError("units must be a Decimal instance")
        if not self.units.is_finite():
            raise exception.InvalidQuantityError()
        if not self.units >= Decimal("0"):
            raise exception.InvalidQuantityError()
        object.__setattr__(self, "units", self.units.quantize(Decimal("0.01")))

    def __str__(self) -> str:
        return str(self.units)

    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError

        return Quantity(self.units + other.units)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError
        if self < other:
            raise exception.InvalidQuantityError

        return Quantity(self.units - other.units)

    def __lt__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise TypeError
        return self.units < other.units

    def __eq__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise TypeError
        return self.units == other.units

    def __le__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise TypeError
        return self.units <= other.units
