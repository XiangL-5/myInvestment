class DomainError(Exception):
    """Base exception for every violation of domain"""

    def __init__(self, message: str = "Rule error of Domain happens") -> None:
        super().__init__(message)
        self.message = message


class InvalidQuantityError(DomainError):
    """Erro when there is no allowed number: negative, infinite, NaN, fractional number"""

    def __init__(self, message: str = "must be a finite or no negative number") -> None:
        super().__init__(message)

    """!!! ZERO is allowed"""


class InvalidMoneyError(DomainError):
    """Error when there is a WRONG CURRENCY CODE, NEGATIVE IMPORT"""


class CurrencyMismatchError(DomainError):
    """Error when is operating two amounts in different currency"""


class InvalidFinancialOperationError(DomainError):
    """Error when is making math operations that lack of sense"""
