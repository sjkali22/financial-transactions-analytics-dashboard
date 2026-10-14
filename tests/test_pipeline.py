"""Regression tests for synthetic generation, cleaning, and KPI definitions."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts import clean_transactions as cleaner  # noqa: E402
from scripts.generate_transactions import generate_dataset  # noqa: E402
from scripts.validate_data import calculate_kpis  # noqa: E402


def raw_row(
    transaction_id: str,
    amount: object,
    transaction_type: str = "Expense",
    category: str = "Shopping",
    is_recurring: object = False,
) -> dict[str, object]:
    return {
        "transaction_id": transaction_id,
        "transaction_date": "2025-01-15",
        "account_id": "ACC00001",
        "customer_id": "CUST0001",
        "transaction_type": transaction_type,
        "category": category,
        "merchant": "Test Merchant",
        "amount": amount,
        "payment_method": "Debit Card",
        "location": "London",
        "is_recurring": is_recurring,
        "is_unusual": False,
        "balance_after_transaction": 1000,
    }


def test_generation_is_reproducible_and_has_expected_schema() -> None:
    first = generate_dataset(seed=42, target_row_count=9000)
    second = generate_dataset(seed=42, target_row_count=9000)

    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 9000
    assert first["transaction_id"].is_unique
    assert first["transaction_date"].min() == "2025-01-01"
    assert first["transaction_date"].max() == "2025-12-31"
    assert set(first["transaction_type"]) == {"Income", "Expense", "Transfer", "Refund"}
    assert set(first["category"]) == {
        "Dining",
        "Entertainment",
        "Groceries",
        "Healthcare",
        "Insurance",
        "Rent",
        "Refunds",
        "Salary",
        "Savings",
        "Shopping",
        "Subscriptions",
        "Transfers",
        "Transport",
        "Travel",
        "Utilities",
    }


def test_cleaning_rejects_duplicates_missing_values_and_zero_amounts() -> None:
    rows = [
        raw_row("TXN0000001", -50),
        raw_row("TXN0000001", -50),
        raw_row("TXN0000001", -60),
        raw_row("TXN0000002", None),
        raw_row("TXN0000003", "not-a-number"),
        raw_row("TXN0000004", 0),
        raw_row("TXN0000005", -10, "Other"),
        raw_row("TXN0000006", -20),
    ]

    cleaned, counts = cleaner.clean_transactions(pd.DataFrame(rows))

    assert list(cleaned["transaction_id"]) == ["TXN0000001", "TXN0000006"]
    assert counts == {
        "starting_rows": 8,
        "exact_duplicates": 1,
        "duplicate_transaction_ids": 1,
        "missing_required_values": 1,
        "invalid_dates_or_numbers": 1,
        "zero_amounts": 1,
        "invalid_transaction_types": 1,
        "output_rows": 2,
        "total_removed": 6,
    }
    assert not cleaned.isna().any().any()


def test_cleaning_requires_the_documented_raw_schema() -> None:
    incomplete = pd.DataFrame([{"transaction_id": "TXN0000001"}])

    with pytest.raises(ValueError, match="Missing required columns"):
        cleaner.clean_transactions(incomplete)


def test_transaction_classification_and_kpi_reconciliation() -> None:
    rows = [
        raw_row("TXN0000001", 1000, "Income", "Salary", True),
        raw_row("TXN0000002", -200, "Expense", "Shopping", True),
        raw_row("TXN0000003", -100, "Transfer", "Savings", True),
        raw_row("TXN0000004", 25, "Refund", "Refunds", False),
    ]

    cleaned, _ = cleaner.clean_transactions(pd.DataFrame(rows))
    kpis = calculate_kpis(cleaned)

    assert kpis["total_income"] == 1000
    assert kpis["total_expenses"] == 200
    assert kpis["operating_surplus"] == 800
    assert kpis["net_cash_flow"] == 725
    assert kpis["recurring_expenses"] == 200


def test_budget_classification_and_monthly_grain(monkeypatch) -> None:
    monkeypatch.setitem(cleaner.CATEGORY_MONTHLY_BUDGETS, "Shopping", 100)

    near_rows = [raw_row("TXN0000001", -45), raw_row("TXN0000002", -50)]
    near_limit, _ = cleaner.clean_transactions(pd.DataFrame(near_rows))
    assert set(near_limit["budget_status"]) == {"Near Limit"}
    assert set(near_limit["category_month_expense"]) == {95}
    assert set(near_limit["budget_utilisation_pct"]) == {0.95}

    exceeded_rows = [raw_row("TXN0000003", -60), raw_row("TXN0000004", -50)]
    exceeded, _ = cleaner.clean_transactions(pd.DataFrame(exceeded_rows))
    assert set(exceeded["budget_status"]) == {"Exceeded Budget"}
    assert set(exceeded["category_month_expense"]) == {110}
    unique_budget = exceeded.drop_duplicates(["transaction_month", "category"])
    assert unique_budget["category_budget"].sum() == 100
