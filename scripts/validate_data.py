"""Validate the cleaned dataset and reconcile portfolio KPIs independently."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_PATH = PROJECT_ROOT / "data" / "cleaned" / "transactions_cleaned.csv"
MONEY = Decimal("0.01")

EXPECTED_COLUMNS = [
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


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Calculate the documented portfolio KPIs with pandas."""
    recurring_expenses = df["is_recurring"] & df["transaction_type"].eq("Expense")
    budget_grain = (
        df.loc[df["category_budget"].gt(0)]
        .drop_duplicates(["transaction_month", "category"])
    )

    total_income = round(float(df["income_amount"].sum()), 2)
    total_expenses = round(float(df["expense_amount"].sum()), 2)
    total_budget = round(float(budget_grain["category_budget"].sum()), 2)
    actual_budgeted_expense = round(float(budget_grain["category_month_expense"].sum()), 2)

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "operating_surplus": round(total_income - total_expenses, 2),
        "net_cash_flow": round(float(df["net_amount"].sum()), 2),
        "average_transaction_value": round(float(df["amount_abs"].mean()), 2),
        "recurring_expenses": round(float(df.loc[recurring_expenses, "expense_amount"].sum()), 2),
        "total_budget": total_budget,
        "actual_budgeted_expense": actual_budgeted_expense,
        "budget_variance": round(total_budget - actual_budgeted_expense, 2),
        "budget_utilisation_pct": round(100 * actual_budgeted_expense / total_budget, 2),
        "transaction_count": len(df),
    }


def calculate_kpis_with_decimal(path: Path) -> dict[str, Decimal | int]:
    """Recalculate core KPIs using csv and Decimal, independently of pandas sums."""
    total_income = Decimal("0")
    total_expenses = Decimal("0")
    net_cash_flow = Decimal("0")
    total_absolute_value = Decimal("0")
    recurring_expenses = Decimal("0")
    row_count = 0

    with path.open(newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row_count += 1
            income = Decimal(row["income_amount"])
            expense = Decimal(row["expense_amount"])
            total_income += income
            total_expenses += expense
            net_cash_flow += Decimal(row["net_amount"])
            total_absolute_value += Decimal(row["amount_abs"])
            if row["is_recurring"].lower() == "true" and row["transaction_type"] == "Expense":
                recurring_expenses += expense

    return {
        "total_income": total_income.quantize(MONEY),
        "total_expenses": total_expenses.quantize(MONEY),
        "operating_surplus": (total_income - total_expenses).quantize(MONEY),
        "net_cash_flow": net_cash_flow.quantize(MONEY),
        "average_transaction_value": (total_absolute_value / row_count).quantize(MONEY),
        "recurring_expenses": recurring_expenses.quantize(MONEY),
        "transaction_count": row_count,
    }


def validate_dataset(df: pd.DataFrame) -> None:
    """Raise an assertion with a clear message when a data contract fails."""
    assert list(df.columns) == EXPECTED_COLUMNS, "Cleaned schema does not match EXPECTED_COLUMNS"
    assert len(df) == 9000, f"Expected 9,000 rows, found {len(df):,}"
    assert not df["transaction_id"].duplicated().any(), "Duplicate transaction IDs found"
    assert not df.isna().any().any(), "Missing values found"
    assert set(df["transaction_type"]) == {"Income", "Expense", "Transfer", "Refund"}
    assert df["transaction_date"].min() == pd.Timestamp("2025-01-01")
    assert df["transaction_date"].max() == pd.Timestamp("2025-12-31")
    assert (df.loc[df["transaction_type"].eq("Income"), "amount"] > 0).all()
    assert (df.loc[df["transaction_type"].eq("Expense"), "amount"] < 0).all()
    assert (
        df.loc[df["category_budget"].gt(0), "budget_status"]
        .isin(["Below Budget", "Near Limit", "Exceeded Budget"])
        .all()
    )


def main() -> None:
    df = pd.read_csv(
        CLEANED_PATH,
        parse_dates=["transaction_date", "transaction_month"],
    )
    validate_dataset(df)
    pandas_kpis = calculate_kpis(df)
    decimal_kpis = calculate_kpis_with_decimal(CLEANED_PATH)

    print("Data contract: PASS")
    print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
    print(
        f"Date range: {df['transaction_date'].min().date()} "
        f"to {df['transaction_date'].max().date()}"
    )
    print(f"Customers: {df['customer_id'].nunique():,} | Accounts: {df['account_id'].nunique():,}")
    print("\nKPI reconciliation (pandas vs csv/Decimal):")
    print("metric | pandas | independent | difference | status")

    for metric in decimal_kpis:
        pandas_value = Decimal(str(pandas_kpis[metric]))
        independent_value = Decimal(str(decimal_kpis[metric]))
        difference = pandas_value - independent_value
        status = "PASS" if difference == 0 else "FAIL"
        print(f"{metric} | {pandas_value} | {independent_value} | {difference} | {status}")

    print("\nBudget KPIs (month/category grain):")
    for metric in [
        "total_budget",
        "actual_budgeted_expense",
        "budget_variance",
        "budget_utilisation_pct",
    ]:
        print(f"{metric}: {pandas_kpis[metric]}")

    budget_grain = df.loc[df["category_budget"].gt(0)].drop_duplicates(
        ["transaction_month", "category"]
    )
    print("\nBudget status counts (month/category grain):")
    print(budget_grain["budget_status"].value_counts().sort_index().to_string())

    print("\nTransaction types:")
    print(df["transaction_type"].value_counts().sort_index().to_string())
    refund_inflows = df.loc[df["transaction_type"].eq("Refund"), "net_amount"].sum()
    net_transfers = df.loc[df["transaction_type"].eq("Transfer"), "net_amount"].sum()
    print(f"refund_inflows: {refund_inflows:.2f}")
    print(f"net_transfers: {net_transfers:.2f}")
    print(f"transfer_and_refund_adjustment: {refund_inflows + net_transfers:.2f}")

    category_spend = (
        df.loc[df["transaction_type"].eq("Expense")]
        .groupby("category")["expense_amount"]
        .sum()
        .sort_values(ascending=False)
    )
    print("\nExpense categories:")
    print(category_spend.round(2).to_string())

    monthly = df.groupby("transaction_month").agg(
        income=("income_amount", "sum"),
        expenses=("expense_amount", "sum"),
        net_cash_flow=("net_amount", "sum"),
    )
    print("\nMonthly KPI range:")
    for column in monthly.columns:
        minimum_month = monthly[column].idxmin().strftime("%Y-%m")
        maximum_month = monthly[column].idxmax().strftime("%Y-%m")
        print(
            f"{column}: min={monthly.loc[monthly[column].idxmin(), column]:.2f} "
            f"({minimum_month}), max={monthly.loc[monthly[column].idxmax(), column]:.2f} "
            f"({maximum_month})"
        )

    duplicate_groups = (
        df.groupby(["account_id", "transaction_date", "merchant", "category", "amount_abs"])
        .size()
        .gt(1)
        .sum()
    )
    print("\nReview indicators:")
    print(f"unusual_transactions: {int(df['is_unusual'].sum())}")
    print(f"unusual_transaction_value: {df.loc[df['is_unusual'], 'amount_abs'].sum():.2f}")
    print(f"duplicate_looking_groups: {duplicate_groups}")


if __name__ == "__main__":
    main()
