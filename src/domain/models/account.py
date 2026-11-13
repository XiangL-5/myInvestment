import re
from dataclasses import dataclass
from uuid import UUID

from domain.exceptions import InvalidAccountError


@dataclass(frozen=True, slots=True, kw_only=True)
class Account:
    id: UUID
    name: str
    base_currency: str
    description: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID) or self.id.version != 4:
            raise InvalidAccountError("Account ID must be a UUID version 4.")
        if not isinstance(self.name, str):
            raise InvalidAccountError("The name must be a string")
        name = self.name.strip()
        if not name:
            raise InvalidAccountError("The account name cannot be empty")
        if not isinstance(self.base_currency, str):
            raise InvalidAccountError("The currency must be a string")

        currency = self.base_currency.strip()
        if not re.fullmatch(r"[A-Za-z]{3}", currency):
            raise InvalidAccountError("Base currency must contain three ASCII letters.")

        if not isinstance(self.description, str):
            raise InvalidAccountError("Account description must be a string.")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "base_currency", currency.upper())
