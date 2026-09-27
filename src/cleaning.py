import pandas as pd
import logging

logger = logging.getLogger(__name__)

RETURNED_TRUE_VALUES = {"true", "yes", "1", "ja"}

def _warn_if_missing(series: pd.Series, column: str, replacement: str) -> None:
    """Varnar om kolumnen har saknade eller ogiltiga värden som ersätts."""
    missing = series.isna().sum()
    if missing:
        logger.warning(
            "%d rows have no valud value in %s, replaced with %s",
            missing, column, replacement
        )

def clean_text(series: pd.Series) -> pd.Series:
    """Fyller saknade värden och standardiserar text, t.ex. ' north ' -> 'North'."""
    return series.fillna("Unknown").astype(str).str.strip().str.title()

def clean_returned(series: pd.Series) -> pd.Series:
    """Gör om returkolumnen till true/false"""
    return (
        series.fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(RETURNED_TRUE_VALUES)
    )

def clean_orders(data: pd.DataFrame) -> pd.DataFrame:
    """Städar orderdata och returnerar en ny DataFrame."""
    data = data.copy()

    data["region"] = clean_text(data["region"])
    data["product_category"] = clean_text(data["product_category"])
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    _warn_if_missing(data["quantity"], "quantity", "1")
    data["quantity"] = data["quantity"].fillna(1)

    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    _warn_if_missing(data["unit_price"], "unit_price", "median_price")
    data["unit_price"] = data["unit_price"].fillna(data["unit_price"].median())

    data["discount"] = pd.to_numeric(data["discount"], errors="coerce")
    _warn_if_missing(data["discount"], "discount", "0")
    data["discount"] = data["discount"].fillna(0)
    
    data["returned"] = clean_returned(data["returned"])

    logger.info("Data cleaning completed")
    return data