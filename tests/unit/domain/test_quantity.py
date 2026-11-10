from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.exceptions import InvalidQuantityError
from domain.models.quantity import Quantity


class TestQuantityCreationAndInvariants:
    """Verify Quantity object creation and invariant"""

    def test_create_valid_quantity(self) -> None:
        """A valid positive Decimal number"""
        qty1 = Quantity(Decimal("10.5"))
        assert qty1.units == Decimal("10.5")
        assert str(qty1) == "10.50"

        qty2 = Quantity(Decimal("0.01"))
        assert qty2.units == Decimal("0.01")
        assert str(qty2) == "0.01"

    def test_create_zero_quantity(self) -> None:
        """Invalid boundry number 0"""
        qty1 = Quantity(Decimal("0"))
        assert qty1.units == Decimal("0")

    def test_reject_non_decimal_quantity(self) -> None:
        """Passing float or str type instance"""
        with pytest.raises(TypeError, match="units must be a Decimal"):
            Quantity(10.5)

        with pytest.raises(TypeError, match="units must be a Decimal"):
            Quantity("10.5")

        with pytest.raises(TypeError, match="units must be a Decimal"):
            Quantity(10)

    def test_reject_non_finite_quantity(self) -> None:
        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            Quantity(Decimal("NaN"))

        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            Quantity(Decimal("Infinity"))

        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            Quantity(Decimal("-Infinity"))

    def test_reject_negative_quantity(self) -> None:
        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            Quantity(Decimal("-1"))

        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            Quantity(Decimal("-0.01"))

    def test_enforce_immutability(self) -> None:
        qty = Quantity(Decimal("10"))
        with pytest.raises(FrozenInstanceError):
            qty.units = Decimal("20")


class TestQuantityArithmeticAndComparison:
    """Verification of arithmetic operation and comparison"""

    def test_addition_return_new_quantity(self) -> None:
        """Adding 2 Quantity objects and return a Quantity Object"""
        qty1 = Quantity(Decimal("10.5"))
        qty2 = Quantity(Decimal("5.32"))
        result = qty1 + qty2

        assert isinstance(result, Quantity)
        assert result.units == Decimal("15.82")
        assert str(result) == "15.82"

    def test_substraction_valid(self) -> None:
        """verify a sub operation with smaller or equal Quantity produce valid result"""
        qty1 = Quantity(Decimal("10"))
        qty2 = Quantity(Decimal("1"))
        result = qty1 - qty2

        assert isinstance(result, Quantity)
        assert result.units == Decimal("9")

        qty1 = Quantity(Decimal("10"))
        qty2 = Quantity(Decimal("10"))
        result = qty1 - qty2

        assert isinstance(result, Quantity)
        assert result.units == Decimal("0")

    def test_substraction_negative_result(self) -> None:
        """very a sub operation with more units than the avaible"""
        qty1 = Quantity(Decimal("10"))
        qty2 = Quantity(Decimal("20"))
        qty3 = Quantity(Decimal("10.1"))

        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            _ = qty1 - qty2
        with pytest.raises(InvalidQuantityError, match="must be a finite or no negative number"):
            _ = qty1 - qty3

    def test_operation_with_primitives(self) -> None:
        """operations with primitives(Decimal, int, float...) must be rejected"""
        qty1 = Quantity(Decimal("10"))
        with pytest.raises(TypeError):
            _ = qty1 + Decimal("5")

        with pytest.raises(TypeError):
            _ = qty1 + int("5")

        with pytest.raises(TypeError):
            _ = qty1 + float("5.0")

    def test_structural_equality_and_ordering(self) -> None:
        """Quantities with the same numeric value are equal regardless of scale."""
        qty_1 = Quantity(Decimal("10.0"))
        qty_2 = Quantity(Decimal("10.00"))
        qty_3 = Quantity(Decimal("15.0"))

        assert qty_1 == qty_2
        assert qty_1 < qty_3
        assert qty_1 <= qty_2
        assert qty_3 > qty_1
