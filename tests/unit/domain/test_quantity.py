from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.exceptions import InvalidFinancialOperationError
from domain.models.quantity import Quantity


class TestQuantityCreationAndInvariants:
    """Verify Quantity object creation and invariant"""

    def test_create_valid_quantity(self) -> None:
        """A valid positive Decimal number"""
        qty = Quantity(Decimal("10.5"))
        assert qty._units == Decimal("10.5")
        assert str(qty) == "10.5"

    def test_create_zero_quantity(self) -> None:
        """Invalid boundry number 0"""
        qty1 = Quantity(Decimal("0"))
        assert qty1._units == Decimal("0")
