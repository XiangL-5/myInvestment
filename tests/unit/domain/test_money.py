from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.exceptions import (
    CurrencyMismatchError,
    InvalidFinancialOperationError,
    InvalidMoneyError,
)
from domain.models.money import Money
