import pandas as pd
import pytest
from src.validation import validate_columns, validate_values

def test_missing_column_raises_error():
    data = pd.DataFrame({"order_id": ["O1"]})

    with pytest.raises(ValueError):
        validate_columns(data)

def test_discount_above_one_raises_error():
    data = pd.DataFrame({
        "order_id": ["O1"],
        "quantity": [1],
        "unit_price": [100.0],
        "discount": [1.5]
    })

    result = validate_values(data)

    assert not result.is_valid
    assert len(result.errors) == 1
    assert "discount" in result.errors[0]