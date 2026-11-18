
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "output" / "cleaned_sales.csv"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    if not INPUT_FILE.exists():
        print("Cleaned CSV not found. Run clean_sales.py first.")
        return

    df = pd.read_csv(INPUT_FILE)

    # Revenue by product
    product_summary = (
        df.groupby(["product_id", "product_name", "category"], as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("net_revenue", "sum"),
            total_profit=("profit", "sum")
        )
        .sort_values("total_revenue", ascending=False)
    )

    # Revenue by store
    store_summary = (
        df.groupby(["store_id", "store_name", "region"], as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("net_revenue", "sum"),
            total_profit=("profit", "sum")
        )
        .sort_values("total_revenue", ascending=False)
    )

    product_summary.to_csv(
        OUTPUT_DIR / "product_sales_summary.csv", index=False
    )
    store_summary.to_csv(
        OUTPUT_DIR / "store_sales_summary.csv", index=False
    )

    print("\nREVENUE BY PRODUCT")
    print(product_summary.to_string(index=False))

    print("\nREVENUE BY STORE")
    print(store_summary.to_string(index=False))

    print("\nOverall net revenue:", round(df["net_revenue"].sum(), 2))
    print("Overall profit:", round(df["profit"].sum(), 2))
    print("\nSummary CSV files saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()