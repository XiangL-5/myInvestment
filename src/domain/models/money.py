from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

import domain.exceptions as exception


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable Value Object representing a monetary amount and ISO 4217 currency."""

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.currency, str):
            raise exception.InvalidMoneyError("Invalid currency code")
        object.__setattr__(self, "currency", self.currency.upper().strip())
        if not re.fullmatch(r"[A-Z]{3}", self.currency):
            raise exception.InvalidMoneyError("Invalid currency code")
        if not isinstance(self.amount, Decimal):
            raise TypeError("amount must be a Decimal")
        if not self.amount.is_finite():
            raise exception.InvalidMoneyError("must be a finite number")

    def __add__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise exception.CurrencyMismatchError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise exception.CurrencyMismatchError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: object) -> Money:
        if isinstance(other, (Decimal, int)):
            factor = Decimal(other) if isinstance(other, int) else other
            return Money(self.amount * factor, self.currency)
        raise exception.InvalidFinancialOperationError(
            "Money can only be multiplied by a numeric scalar (Decimal or int)."
        )

    def __neg__(self) -> Money:
        return Money(-self.amount, self.currency)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise exception.CurrencyMismatchError("Cannot compare different currencies")
        return self.amount < other.amount

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise exception.CurrencyMismatchError("Cannot compare different currencies")
        return self.amount <= other.amount
