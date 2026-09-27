import pandas as pd

def add_order_values(data: pd.DataFrame) -> pd.DataFrame:
    """Lägger till ordervärde före och efter rabatt."""
    data = data.copy()
    data["order_value"] = data["quantity"] * data["unit_price"]
    data["discounted_value"] = data["order_value"] * (1 - data["discount"])

    return data

def build_overview(data: pd.DataFrame) -> pd.DataFrame:
    """Skapar en översikt med total försäljning, antal ordrar och returer."""
    return pd.DataFrame(
        {
            "metric": ["total_sales", "order_count", "return_count"],
            "value": [
                round(data["discounted_value"].sum(), 2),
                data["order_id"].nunique(),
                int(data["returned"].sum()),
            ],
        }
    )

def summarize_by(data: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Summerar försäljning och returer per vald kolumn."""
    summary = data.groupby(group_column, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )
    summary["total_sales"] = summary["total_sales"].round(2)
    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)

    return summary.sort_values("total_sales", ascending=False).reset_index(drop=True)

def build_returns_by_category(sales_by_category: pd.DataFrame) -> pd.DataFrame:
    """Skapar returrapporten utifrån den befintliga kategorisammanställningen."""
    columns = ["product_category", "order_count", "returns", "return_rate"]
    return (
        sales_by_category[columns]
        .sort_values("return_rate", ascending=False)
        .reset_index(drop=True)
    )

def build_reports(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Bygger alla rapporter och returnerar dem med sina filnamn."""
    data = add_order_values(data)
    sales_by_category = summarize_by(data, "product_category")

    return {
        "overview.csv": build_overview(data),
        "sales_by_category.csv": sales_by_category,
        "sales_by_region.csv": summarize_by(data, "region"),
        "returns_by_category.csv": build_returns_by_category(sales_by_category)
    }