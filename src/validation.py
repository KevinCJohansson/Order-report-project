import pandas as pd
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned"
}

@dataclass
class ValidationResult:
    """Samlar valideringsfel så att alla kan rapporteras på en gång."""
    errors: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def raise_if_invalid(self) -> None:
        if not self.is_valid:
            raise ValueError("Invalid values found. " + "; ".join(self.errors))

def validate_columns(data: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing columns: {missing}")

    logger.info("All required columns are present")

def validate_values(data: pd.DataFrame) -> ValidationResult:
    """Kontrollerar att numeriska värden är rimliga. Körs efter städningen."""
    result = ValidationResult()

    invalid_quantity = data.loc[data["quantity"] <= 0, "order_id"].tolist()
    if invalid_quantity:
        result.add_error(f"quantity must be greater than 0: {invalid_quantity}")

    invalid_price = data.loc[data["unit_price"] < 0, "order_id"].tolist()
    if invalid_price:
        result.add_error(f"unit_price cannot be negative: {invalid_price}")

    invalid_discount = data.loc[~data["discount"].between(0, 1), "order_id"].tolist()
    if invalid_discount:
        result.add_error(f"discount must be between 0 and 1: {invalid_discount}")

    if result.is_valid:
        logger.info("All values are within valid ranges")

    return result