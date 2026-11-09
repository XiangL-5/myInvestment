from dataclasses import dataclass
from decimal import Decimal

import domain.exceptions as exception


@dataclass(frozen=True, slots=True)
class Quantity:
    _units: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self._units, Decimal):
            raise TypeError("units should Decimal type, don't accept float or Str")
        if not self._units.is_finite():
            raise exception.InvalidQuantityError()
        if not self._units >= Decimal("0"):
            raise exception.InvalidQuantityError()

    def __str__(self) -> str:
        return str(self._units)
