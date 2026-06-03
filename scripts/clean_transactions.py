"""Clean the raw financial transactions dataset for analysis."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_raw.csv"
CLEANED_PATH = PROJECT_ROOT / "data" / "cleaned" / "transactions_cleaned.csv"

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "account_id",
    "customer_id",
    "transaction_type",
    "category",
    "merchant",
    "amount",
    "payment_method",
    "location",
    "is_recurring",
    "is_unusual",
    "balance_after_transaction",
]

TEXT_COLUMNS = ["transaction_type", "category", "payment_method", "location"]

CATEGORY_MONTHLY_BUDGETS = {
    "Rent": 112000,
    "Groceries": 2100,
    "Utilities": 17000,
    "Transport": 1600,
    "Dining": 1800,
    "Entertainment": 900,
    "Shopping": 7000,
    "Subscriptions": 4700,
    "Insurance": 6500,
    "Healthcare": 6000,
    "Travel": 5500,
    "Savings": 52000,
    "Transfers": 12000,
    "Refunds": 0,
    "Salary": 0,
}


def normalise_boolean(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {RAW_PATH}. Run scripts/generate_transactions.py first."
        )

    df = pd.read_csv(RAW_PATH)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    starting_rows = len(df)
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["balance_after_transaction"] = pd.to_numeric(df["balance_after_transaction"], errors="coerce")

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype(str).str.strip().str.title()

    for column in ["transaction_id", "account_id", "customer_id"]:
        df[column] = df[column].astype(str).str.strip().str.upper()

    df["merchant"] = df["merchant"].astype(str).str.strip()
    df["is_recurring"] = df["is_recurring"].apply(normalise_boolean)
    df["is_unusual"] = df["is_unusual"].apply(normalise_boolean)

    df = df.dropna(subset=["transaction_date", "amount", "balance_after_transaction"])
    df = df[df["amount"] != 0].copy()
    df = df[df["transaction_type"].isin(["Income", "Expense", "Transfer", "Refund"])].copy()

    df["transaction_month"] = df["transaction_date"].dt.to_period("M").dt.to_timestamp()
    df["transaction_year"] = df["transaction_date"].dt.year.astype(int)
    df["month_name"] = df["transaction_date"].dt.strftime("%B")

    df["amount"] = df["amount"].round(2)
    df["balance_after_transaction"] = df["balance_after_transaction"].round(2)
    df["amount_abs"] = df["amount"].abs().round(2)
    df["income_amount"] = np.where(df["transaction_type"].eq("Income"), df["amount"].clip(lower=0), 0).round(2)
    df["expense_amount"] = np.where(df["transaction_type"].eq("Expense"), df["amount_abs"], 0).round(2)
    df["net_amount"] = df["amount"].round(2)

    df["category_budget"] = df["category"].map(CATEGORY_MONTHLY_BUDGETS).fillna(0).astype(float)

    monthly_category_spend = (
        df.groupby(["transaction_month", "category"], as_index=False)["expense_amount"]
        .sum()
        .rename(columns={"expense_amount": "category_month_expense"})
    )
    df = df.merge(monthly_category_spend, on=["transaction_month", "category"], how="left")
    df["category_month_expense"] = df["category_month_expense"].fillna(0).round(2)
    df["budget_variance"] = (df["category_budget"] - df["category_month_expense"]).round(2)
    df["budget_variance_pct"] = np.where(
        df["category_budget"] > 0,
        (df["budget_variance"] / df["category_budget"]).round(4),
        0,
    )

    df["budget_status"] = np.select(
        [
            df["category_budget"].eq(0),
            df["category_month_expense"].le(df["category_budget"]),
            df["category_month_expense"].le(df["category_budget"] * 1.1),
        ],
        ["Not Budgeted", "Within Budget", "Near Budget"],
        default="Over Budget",
    )

    df = df.sort_values(["transaction_date", "account_id", "transaction_id"]).reset_index(drop=True)
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
    df["transaction_month"] = df["transaction_month"].dt.strftime("%Y-%m-%d")

    output_columns = [
        "transaction_id",
        "transaction_date",
        "transaction_month",
        "transaction_year",
        "month_name",
        "account_id",
        "customer_id",
        "transaction_type",
        "category",
        "merchant",
        "amount",
        "amount_abs",
        "income_amount",
        "expense_amount",
        "net_amount",
        "payment_method",
        "location",
        "is_recurring",
        "is_unusual",
        "balance_after_transaction",
        "category_budget",
        "category_month_expense",
        "budget_variance",
        "budget_variance_pct",
        "budget_status",
    ]

    CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df[output_columns].to_csv(CLEANED_PATH, index=False)

    removed_rows = starting_rows - len(df)
    print(f"Cleaned {len(df):,} rows and saved analysis-ready data to {CLEANED_PATH}")
    print(f"Removed {removed_rows:,} duplicate or invalid rows during cleaning")


if __name__ == "__main__":
    main()
