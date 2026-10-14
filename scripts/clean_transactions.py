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
    "Savings": 0,
    "Transfers": 0,
    "Refunds": 0,
    "Salary": 0,
}

BUDGET_NEAR_LIMIT_THRESHOLD = 0.90


def normalise_boolean(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def clean_transactions(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Validate and transform raw transactions without reading or writing files."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    rejection_counts: dict[str, int] = {"starting_rows": len(df)}

    before = len(df)
    df = df.drop_duplicates()
    rejection_counts["exact_duplicates"] = before - len(df)

    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")
    rejection_counts["duplicate_transaction_ids"] = before - len(df)

    missing_required_values = df[REQUIRED_COLUMNS].isna().any(axis=1)
    rejection_counts["missing_required_values"] = int(missing_required_values.sum())
    df = df.loc[~missing_required_values].copy()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["balance_after_transaction"] = pd.to_numeric(
        df["balance_after_transaction"],
        errors="coerce",
    )

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype(str).str.strip().str.title()

    for column in ["transaction_id", "account_id", "customer_id"]:
        df[column] = df[column].astype(str).str.strip().str.upper()

    df["merchant"] = df["merchant"].astype(str).str.strip()
    df["is_recurring"] = df["is_recurring"].apply(normalise_boolean)
    df["is_unusual"] = df["is_unusual"].apply(normalise_boolean)

    invalid_required_values = df[
        ["transaction_date", "amount", "balance_after_transaction"]
    ].isna().any(axis=1)
    rejection_counts["invalid_dates_or_numbers"] = int(invalid_required_values.sum())
    df = df.loc[~invalid_required_values].copy()

    rejection_counts["zero_amounts"] = int(df["amount"].eq(0).sum())
    df = df[df["amount"] != 0].copy()

    valid_transaction_types = ["Income", "Expense", "Transfer", "Refund"]
    invalid_transaction_types = ~df["transaction_type"].isin(valid_transaction_types)
    rejection_counts["invalid_transaction_types"] = int(invalid_transaction_types.sum())
    df = df.loc[~invalid_transaction_types].copy()

    df["transaction_month"] = df["transaction_date"].dt.to_period("M").dt.to_timestamp()
    df["transaction_year"] = df["transaction_date"].dt.year.astype(int)
    df["month_name"] = df["transaction_date"].dt.strftime("%B")

    df["amount"] = df["amount"].round(2)
    df["balance_after_transaction"] = df["balance_after_transaction"].round(2)
    df["amount_abs"] = df["amount"].abs().round(2)
    df["income_amount"] = np.where(
        df["transaction_type"].eq("Income"),
        df["amount"].clip(lower=0),
        0,
    ).round(2)
    df["expense_amount"] = np.where(
        df["transaction_type"].eq("Expense"),
        df["amount_abs"],
        0,
    ).round(2)
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
    df["budget_utilisation_pct"] = np.where(
        df["category_budget"] > 0,
        (df["category_month_expense"] / df["category_budget"]).round(4),
        0,
    )

    df["budget_status"] = np.select(
        [
            df["category_budget"].eq(0),
            df["category_month_expense"].lt(
                df["category_budget"] * BUDGET_NEAR_LIMIT_THRESHOLD
            ),
            df["category_month_expense"].le(df["category_budget"]),
        ],
        ["Not Budgeted", "Below Budget", "Near Limit"],
        default="Exceeded Budget",
    )

    df = df.sort_values(
        ["transaction_date", "account_id", "transaction_id"]
    ).reset_index(drop=True)
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
        "budget_utilisation_pct",
        "budget_status",
    ]

    cleaned_df = df[output_columns]
    rejection_counts["output_rows"] = len(cleaned_df)
    rejection_counts["total_removed"] = rejection_counts["starting_rows"] - len(cleaned_df)
    return cleaned_df, rejection_counts


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {RAW_PATH}. Run scripts/generate_transactions.py first."
        )

    raw_df = pd.read_csv(RAW_PATH)
    cleaned_df, rejection_counts = clean_transactions(raw_df)

    CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(CLEANED_PATH, index=False)

    print(f"Cleaned {len(cleaned_df):,} rows and saved analysis-ready data to {CLEANED_PATH}")
    print(
        "Rejected rows: "
        f"exact duplicates={rejection_counts['exact_duplicates']:,}, "
        f"duplicate IDs={rejection_counts['duplicate_transaction_ids']:,}, "
        f"missing required values={rejection_counts['missing_required_values']:,}, "
        f"invalid dates/numbers={rejection_counts['invalid_dates_or_numbers']:,}, "
        f"zero amounts={rejection_counts['zero_amounts']:,}, "
        f"invalid transaction types={rejection_counts['invalid_transaction_types']:,} "
        f"(total removed={rejection_counts['total_removed']:,})"
    )


if __name__ == "__main__":
    main()
