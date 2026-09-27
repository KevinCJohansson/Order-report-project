import pandas as pd
from src.reports import add_order_values, summarize_by

def test_order_value():
    data = pd.DataFrame({
        "quantity": [2, 3],
        "unit_price": [100.0, 50.0],
        "discount": [0.0, 0.0],
    })

    result = add_order_values(data)
    assert result["order_value"].tolist() == [200.0, 150.0]

def test_discounted_value():
    data = pd.DataFrame({
        "quantity": [2],
        "unit_price": [100.0],
        "discount": [0.25],
    })

    result = add_order_values(data)
    assert result["discounted_value"].tolist() == [150.0]

def test_summary_by_category():
    data = pd.DataFrame({
        "order_id": ["O1", "O2", "O3"],
        "product_category": ["Books", "Books", "Electronics"],
        "quantity": [2, 1, 1],
        "unit_price": [100.0, 100.0, 1000.0],
        "discount": [0.0, 0.0, 0.0],
        "returned": [True, False, False],
    })

    result = summarize_by(add_order_values(data), "product_category")
    assert result["product_category"].tolist() == ["Electronics", "Books"]
    assert result["order_count"].tolist() == [1, 2]
    assert result["total_sales"].tolist() == [1000.0, 300.0]
    assert result["return_rate"].tolist() == [0.0, 0.5]

def test_summary_by_region():
    data = pd.DataFrame({
        "order_id": ["O1", "O2", "O3"],
        "region": ["North", "South", "South"],
        "quantity": [1, 1, 1],
        "unit_price": [100.0, 300.0, 200.0],
        "discount": [0.0, 0.0, 0.0],
        "returned": [False, True, False],
    })

    result = summarize_by(add_order_values(data), "region")
    assert result["region"].tolist() == ["South", "North"]
    assert result["total_sales"].tolist() == [500.0, 100.0]