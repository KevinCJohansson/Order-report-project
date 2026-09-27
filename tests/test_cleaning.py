import pandas as pd
from src.cleaning import clean_orders, clean_returned

def test_returned_values():
    data = pd.Series(["yes", "ja", "no", "false"])
    result = clean_returned(data)

    assert result.tolist() == [True, True, False, False]

def test_invalid_discount_becomes_zero():
    data = pd.DataFrame({
        "region": ["North"],
        "product_category": ["Books"],
        "quantity": [1],
        "unit_price": [100.0],
        "discount": ["unknown"],
        "returned": ["false"],
    })

    result = clean_orders(data)
    assert result["discount"].tolist() == [0]