
from pathlib import Path

import numpy as np
import pandas as pd

# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "sales.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "cleaned_sales.csv"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # 1. Load sales data
    if not INPUT_FILE.exists():
        print(f"ERROR: CSV file not found: {INPUT_FILE}")
        print("Place sales.csv inside the data folder.")
        return

    df = pd.read_csv(INPUT_FILE)

    print("=" * 50)
    print("RETAIL SALES DATA CLEANING")
    print("=" * 50)
    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())

    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # 3. Inspect missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # 4. Remove duplicate rows
    df = df.drop_duplicates()

    # 5. Convert data types
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(
            df["sale_date"], errors="coerce"
        )

    numeric_columns = [
        "sale_id", "product_id", "cost", "store_id",
        "employee_id", "quantity", "unit_price",
        "discount_percent"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

    # 6. Remove rows missing essential sales fields
    required_columns = [
        "sale_date", "product_id", "store_id",
        "quantity", "unit_price"
    ]

    missing_required = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_required:
        print("\nERROR: Required columns are missing:")
        print(missing_required)
        print("Check the CSV export and column names.")
        return

    df = df.dropna(subset=required_columns)

    # 7. Replace missing discounts with zero
    if "discount_percent" in df.columns:
        df["discount_percent"] = (
            df["discount_percent"].fillna(0)
        )

    # 8. Validate sales values
    valid_rows = (
        (df["quantity"] >= 0)
        & (df["unit_price"] >= 0)
        & (df["discount_percent"].between(0, 100))
    )

    df = df.loc[valid_rows].copy()

    # 9. Calculate revenue and discount
    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    df["discount_amount"] = (
        df["gross_revenue"] * df["discount_percent"] / 100
    )

    df["net_revenue"] = (
        df["gross_revenue"] - df["discount_amount"]
    )

    # 10. Calculate profit and profit margin
    if "cost" in df.columns:
        df["total_cost"] = df["quantity"] * df["cost"]

        df["profit"] = df["net_revenue"] - df["total_cost"]

        df["profit_margin_percent"] = np.where(
            df["net_revenue"] != 0,
            df["profit"] / df["net_revenue"] * 100,
            np.nan
        )

    # 11. Save cleaned dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nCleaned rows:", len(df))
    print("Removed rows:", "calculated below")
    print("\nFirst five cleaned records:")
    print(df.head().to_string(index=False))

    print("\nOutput saved successfully:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
