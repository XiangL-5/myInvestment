import re

from domain.exceptions import InvalidAssetError


def normalize_ticker(value: object) -> str:
    if not isinstance(value, str):
        raise InvalidAssetError("Ticker must be a string.")

    ticker = value.strip()

    if not ticker:
        raise InvalidAssetError("Ticker cannot be empty.")

    return ticker.upper()


def normalize_isin(value: object) -> str:
    if not isinstance(value, str):
        raise InvalidAssetError("ISIN must be a string.")

    isin = value.strip()

    if not re.fullmatch(r"[A-Za-z]{2}[A-Za-z0-9]{9}[0-9]", isin):
        raise InvalidAssetError("ISIN must have a valid 12-character format.")

    return isin.upper()


def normalize_optional_ticker(value: object | None) -> str | None:
    if value is None:
        return None

    return normalize_ticker(value)


def normalize_optional_isin(value: object | None) -> str | None:
    if value is None:
        return None

    return normalize_isin(value)
