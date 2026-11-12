from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.exceptions import (
    CurrencyMismatchError,
    InvalidFinancialOperationError,
    InvalidMoneyError,
)
from domain.models.money import Money


class TestMoneyCreationAndInvariants:
    """Verifies construction, formatting, and invariant validation for Money."""

    def test_create_valid_money(self) -> None:
        """Valid Decimal and ISO currency code must instantiate cleanly."""
        m = Money(Decimal("100.50"), "EUR")
        assert m.amount == Decimal("100.50")
        assert m.currency == "EUR"

    def test_currency_normalization(self) -> None:
        """Currencies with leading/trailing spaces or lowercase should be normalized."""
        m = Money(Decimal("50.00"), " usd   ")
        assert m.currency == "USD"

    def test_reject_invalid_currency_code(self) -> None:
        """Currency codes must strictly be 3 alphabetical characters (ISO 4217)."""
        with pytest.raises(InvalidMoneyError, match="Invalid currency code"):
            Money(Decimal("100"), "EURO")

        with pytest.raises(InvalidMoneyError, match="Invalid currency code"):
            Money(Decimal("100"), "12")

    def test_reject_non_decimal_amount(self) -> None:
        """Amount must strictly be a Decimal instance."""
        with pytest.raises(TypeError, match="amount must be a Decimal"):
            Money(100.5, "EUR")  # type: ignore[arg-type]

    def test_reject_non_finite_amount(self) -> None:
        """NaN or infinite amounts must be rejected immediately."""
        with pytest.raises(InvalidMoneyError, match="must be a finite number"):
            Money(Decimal("NaN"), "EUR")

        with pytest.raises(InvalidMoneyError, match="must be a finite number"):
            Money(Decimal("Infinity"), "EUR")

    def test_negative_amounts_are_allowed(self) -> None:
        """Money can be negative to represent realized losses, debts, or cash outflows."""
        loss = Money(Decimal("-250.75"), "EUR")
        assert loss.amount == Decimal("-250.75")

    def test_enforce_immutability(self) -> None:
        """Fields cannot be reassigned once created."""
        m = Money(Decimal("100"), "EUR")
        with pytest.raises(FrozenInstanceError):
            m.amount = Decimal("200")  # type: ignore[misc]


class TestMoneyOperations:
    """Verifies arithmetic, currency boundaries, and comparisons for Money."""

    def test_addition_same_currency(self) -> None:
        """Adding two amounts of the same currency produces a new Money object."""
        m1 = Money(Decimal("100.25"), "EUR")
        m2 = Money(Decimal("50.75"), "EUR")
        result = m1 + m2

        assert isinstance(result, Money)
        assert result.amount == Decimal("151.00")
        assert result.currency == "EUR"

    def test_addition_different_currencies_raises_error(self) -> None:
        """Adding distinct currencies without prior conversion is prohibited."""
        eur = Money(Decimal("100"), "EUR")
        usd = Money(Decimal("100"), "USD")

        with pytest.raises(CurrencyMismatchError, match="Cannot add different currencies"):
            _ = eur + usd

    def test_subtraction_same_currency(self) -> None:
        """Subtracting same-currency Money produces expected difference."""
        m1 = Money(Decimal("100.00"), "USD")
        m2 = Money(Decimal("40.00"), "USD")
        result = m1 - m2

        assert result == Money(Decimal("60.00"), "USD")

    def test_subtraction_different_currencies_raises_error(self) -> None:
        """Subtracting distinct currencies without conversion is prohibited."""
        m1 = Money(Decimal("100"), "EUR")
        m2 = Money(Decimal("50"), "USD")

        with pytest.raises(CurrencyMismatchError, match="Cannot subtract different currencies"):
            _ = m1 - m2

    def test_scalar_multiplication(self) -> None:
        """Multiplying Money by a numeric scalar (Decimal or int) is valid."""
        price = Money(Decimal("12.50"), "EUR")
        total = price * Decimal("4")

        assert isinstance(total, Money)
        assert total.amount == Decimal("50.00")
        assert total.currency == "EUR"

    def test_money_multiplication_by_money_is_prohibited(self) -> None:
        """Multiplying money by money is mathematically invalid in finance."""
        m1 = Money(Decimal("10"), "EUR")
        m2 = Money(Decimal("20"), "EUR")

        with pytest.raises(InvalidFinancialOperationError):
            _ = m1 * m2  # type: ignore[operator]

    def test_negation(self) -> None:
        """Unary negation flips the sign of the amount."""
        profit = Money(Decimal("300"), "EUR")
        loss = -profit

        assert loss == Money(Decimal("-300"), "EUR")

    def test_equality_across_currencies(self) -> None:
        """Amounts in different currencies are never equal."""
        m1 = Money(Decimal("100"), "EUR")
        m2 = Money(Decimal("100"), "USD")
        assert m1 != m2

    def test_ordering_different_currencies_raises_error(self) -> None:
        """Comparing magnitude across different currencies without exchange rates is invalid."""
        m1 = Money(Decimal("100"), "EUR")
        m2 = Money(Decimal("50"), "USD")

        with pytest.raises(CurrencyMismatchError, match="Cannot compare different currencies"):
            _ = m1 < m2
