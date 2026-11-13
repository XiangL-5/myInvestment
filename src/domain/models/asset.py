import re
from dataclasses import dataclass, field
from uuid import UUID

from domain._asset_identifiers import (
    normalize_isin,
    normalize_optional_isin,
    normalize_optional_ticker,
    normalize_ticker,
)
from domain.exceptions import InvalidAssetError
from domain.models.asset_type import AssetType


@dataclass(frozen=True, slots=True, kw_only=True)
class Asset:
    id: UUID
    name: str
    asset_type: AssetType
    currency: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID) or self.id.version != 4:
            raise InvalidAssetError("Asset ID must be a UUID version 4.")

        if not isinstance(self.name, str):
            raise InvalidAssetError("Asset name must be a string.")

        name = self.name.strip()
        if not name:
            raise InvalidAssetError("Asset name cannot be empty.")

        if not isinstance(self.asset_type, AssetType):
            raise InvalidAssetError("Incorrect asset type.")

        if not isinstance(self.currency, str):
            raise InvalidAssetError("Currency must be a string.")

        currency = self.currency.strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise InvalidAssetError("Currency must contain three letters.")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "currency", currency)


@dataclass(frozen=True, slots=True, kw_only=True)
class StockAsset(Asset):
    asset_type: AssetType = field(init=False, default=AssetType.STOCK)
    ticker: str
    isin: str | None = None

    def __post_init__(self) -> None:
        Asset.__post_init__(self)
        object.__setattr__(self, "ticker", normalize_ticker(self.ticker))
        object.__setattr__(self, "isin", normalize_optional_isin(self.isin))


@dataclass(frozen=True, slots=True, kw_only=True)
class EtfAsset(Asset):
    asset_type: AssetType = field(init=False, default=AssetType.ETF)
    ticker: str
    isin: str

    def __post_init__(self) -> None:
        Asset.__post_init__(self)
        object.__setattr__(self, "ticker", normalize_ticker(self.ticker))
        object.__setattr__(self, "isin", normalize_isin(self.isin))


@dataclass(frozen=True, slots=True, kw_only=True)
class MutualFundAsset(Asset):
    asset_type: AssetType = field(init=False, default=AssetType.MUTUAL_FUND)
    isin: str
    ticker: str | None = None

    def __post_init__(self) -> None:
        Asset.__post_init__(self)
        object.__setattr__(self, "isin", normalize_isin(self.isin))
        object.__setattr__(self, "ticker", normalize_optional_ticker(self.ticker))


@dataclass(frozen=True, slots=True, kw_only=True)
class CryptoAsset(Asset):
    asset_type: AssetType = field(init=False, default=AssetType.CRYPTO)
    ticker: str

    def __post_init__(self) -> None:
        Asset.__post_init__(self)
        object.__setattr__(self, "ticker", normalize_ticker(self.ticker))
