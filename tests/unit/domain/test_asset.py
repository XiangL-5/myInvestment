from uuid import NAMESPACE_DNS, UUID, uuid4, uuid5

import pytest

from domain.exceptions import InvalidAssetError
from domain.models.asset import Asset
from domain.models.asset_type import AssetType


def make_asset(
    *,
    id: UUID | None = None,
    name: str = "Apple Inc.",
    currency: str = "USD",
) -> Asset:
    return Asset(
        id=id if id is not None else uuid4(),
        name=name,
        asset_type=AssetType.STOCK,
        currency=currency,
    )


def test_asset_normalizes_text_fields() -> None:
    asset = make_asset(
        name="  Apple Inc.  ",
        currency=" usd ",
    )

    assert asset.name == "Apple Inc."
    assert asset.currency == "USD"


def test_asset_rejects_non_v4_uuid() -> None:
    invalid_id = uuid5(NAMESPACE_DNS, "apple.com")

    with pytest.raises(InvalidAssetError):
        make_asset(id=invalid_id)


def test_asset_rejects_empty_name() -> None:
    with pytest.raises(InvalidAssetError):
        make_asset(name="   ")


@pytest.mark.parametrize(
    "invalid_currency",
    ["EURO", "12A", "", "€"],
)
def test_asset_rejects_invalid_currency(
    invalid_currency: str,
) -> None:
    with pytest.raises(InvalidAssetError):
        make_asset(currency=invalid_currency)
