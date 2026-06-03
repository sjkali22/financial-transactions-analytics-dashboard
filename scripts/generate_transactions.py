"""Generate a synthetic financial transactions dataset for analysis."""

from __future__ import annotations

from calendar import monthrange
from pathlib import Path
import random

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_raw.csv"

SEED = 42
TARGET_ROW_COUNT = 9000
START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2025-12-31")

rng = np.random.default_rng(SEED)
random.seed(SEED)

MONTHS = pd.date_range(START_DATE, END_DATE, freq="MS")
ALL_DATES = pd.date_range(START_DATE, END_DATE, freq="D")

LOCATIONS = [
    "London",
    "Manchester",
    "Birmingham",
    "Leeds",
    "Glasgow",
    "Cardiff",
    "Bristol",
    "Liverpool",
    "Edinburgh",
    "Online",
]

PAYMENT_METHODS = [
    "Debit Card",
    "Credit Card",
    "Bank Transfer",
    "Direct Debit",
    "Standing Order",
    "Mobile Wallet",
    "Cash Withdrawal",
]

CATEGORY_MERCHANTS = {
    "Salary": ["Employer Payroll"],
    "Rent": ["CityRent", "UrbanNest Lettings"],
    "Groceries": ["FreshMart", "DailyBasket", "GreenGrocer"],
    "Utilities": ["PowerGrid", "WaterWorks", "MobileConnect"],
    "Transport": ["QuickFuel", "MetroTravel", "RideLoop"],
    "Dining": ["CafeSquare", "BistroBox", "LunchLane"],
    "Entertainment": ["StreamPlus", "CinemaPoint", "GameHub"],
    "Shopping": ["ShopHub", "StyleMarket", "TechCorner"],
    "Subscriptions": ["StreamPlus", "CloudBox", "NewsDesk", "MusicWave"],
    "Insurance": ["AutoProtect", "HomeShield", "CoverWise"],
    "Healthcare": ["HealthFirst", "PharmaCare", "GymCore"],
    "Travel": ["MetroTravel", "SkyBridge", "StayEasy Hotels"],
    "Savings": ["FutureFund", "HighYield Savings"],
    "Transfers": ["Internal Transfer", "Family Transfer"],
    "Refunds": ["ShopHub Refund", "Travel Refund", "Service Refund"],
}

EXPENSE_AMOUNT_RANGES = {
    "Groceries": (8, 45, 140),
    "Utilities": (35, 120, 320),
    "Transport": (4, 28, 170),
    "Dining": (7, 35, 180),
    "Entertainment": (8, 35, 160),
    "Shopping": (12, 70, 520),
    "Insurance": (35, 95, 260),
    "Healthcare": (12, 60, 350),
    "Travel": (30, 180, 1200),
    "Subscriptions": (6, 18, 65),
}


def money(value: float) -> float:
    return round(float(value), 2)


def month_date(month_start: pd.Timestamp, preferred_day: int) -> pd.Timestamp:
    last_day = monthrange(month_start.year, month_start.month)[1]
    return pd.Timestamp(month_start.year, month_start.month, min(preferred_day, last_day))


def random_date() -> pd.Timestamp:
    return pd.Timestamp(rng.choice(ALL_DATES))


def weighted_choice(options: list[str], probabilities: list[float]) -> str:
    return str(rng.choice(options, p=probabilities))


def build_accounts() -> list[dict[str, object]]:
    accounts: list[dict[str, object]] = []
    account_number = 1

    for customer_number in range(1, 121):
        customer_id = f"CUST{customer_number:04d}"
        location = str(rng.choice(LOCATIONS[:-1]))
        account_count = 2 if rng.random() < 0.2 else 1

        for _ in range(account_count):
            accounts.append(
                {
                    "customer_id": customer_id,
                    "account_id": f"ACC{account_number:05d}",
                    "location": location,
                    "opening_balance": money(rng.uniform(700, 9000)),
                }
            )
            account_number += 1

    return accounts


def expense_amount(category: str) -> float:
    low, mode, high = EXPENSE_AMOUNT_RANGES[category]
    return -money(rng.triangular(low, mode, high))


def payment_method_for(category: str, transaction_type: str) -> str:
    if transaction_type == "Income":
        return "Bank Transfer"
    if category in {"Rent", "Utilities", "Subscriptions", "Insurance"}:
        return weighted_choice(["Direct Debit", "Bank Transfer", "Standing Order"], [0.7, 0.2, 0.1])
    if category in {"Savings", "Transfers"}:
        return weighted_choice(["Bank Transfer", "Standing Order"], [0.75, 0.25])
    if category == "Transport" and rng.random() < 0.15:
        return "Cash Withdrawal"
    return weighted_choice(["Debit Card", "Credit Card", "Mobile Wallet"], [0.55, 0.3, 0.15])


def add_transaction(
    rows: list[dict[str, object]],
    account: dict[str, object],
    transaction_date: pd.Timestamp,
    transaction_type: str,
    category: str,
    merchant: str,
    amount: float,
    payment_method: str,
    is_recurring: bool = False,
    is_unusual: bool = False,
    location: str | None = None,
) -> None:
    rows.append(
        {
            "transaction_date": pd.Timestamp(transaction_date).date().isoformat(),
            "account_id": account["account_id"],
            "customer_id": account["customer_id"],
            "transaction_type": transaction_type,
            "category": category,
            "merchant": merchant,
            "amount": money(amount),
            "payment_method": payment_method,
            "location": location or account["location"],
            "is_recurring": bool(is_recurring),
            "is_unusual": bool(is_unusual),
            "_sequence": len(rows) + 1,
        }
    )


def add_recurring_transactions(rows: list[dict[str, object]], accounts: list[dict[str, object]]) -> None:
    for account in accounts:
        has_salary = rng.random() < 0.78
        has_rent = rng.random() < 0.48
        has_utilities = rng.random() < 0.65
        has_insurance = rng.random() < 0.38
        has_gym = rng.random() < 0.35
        has_savings_transfer = rng.random() < 0.42
        subscription_count = int(rng.choice([0, 1, 2, 3], p=[0.38, 0.34, 0.2, 0.08]))

        salary_amount = rng.uniform(2200, 4800)
        rent_amount = rng.uniform(850, 2100)
        utilities_amount = rng.uniform(85, 280)
        insurance_amount = rng.uniform(45, 190)
        gym_amount = rng.uniform(25, 75)
        savings_amount = rng.uniform(150, 900)
        subscription_merchants = random.sample(CATEGORY_MERCHANTS["Subscriptions"], k=subscription_count)

        for month_start in MONTHS:
            if has_salary:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(24, 29))),
                    "Income",
                    "Salary",
                    "Employer Payroll",
                    money(rng.normal(salary_amount, salary_amount * 0.025)),
                    "Bank Transfer",
                    is_recurring=True,
                    location="Online",
                )

            if has_rent:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(1, 5))),
                    "Expense",
                    "Rent",
                    "CityRent",
                    -money(rng.normal(rent_amount, rent_amount * 0.015)),
                    "Direct Debit",
                    is_recurring=True,
                )

            if has_utilities:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(7, 16))),
                    "Expense",
                    "Utilities",
                    str(rng.choice(CATEGORY_MERCHANTS["Utilities"])),
                    -money(rng.normal(utilities_amount, utilities_amount * 0.08)),
                    "Direct Debit",
                    is_recurring=True,
                )

            if has_insurance:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(10, 20))),
                    "Expense",
                    "Insurance",
                    str(rng.choice(CATEGORY_MERCHANTS["Insurance"])),
                    -money(rng.normal(insurance_amount, insurance_amount * 0.04)),
                    "Direct Debit",
                    is_recurring=True,
                )

            if has_gym:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(3, 8))),
                    "Expense",
                    "Healthcare",
                    "GymCore",
                    -money(rng.normal(gym_amount, gym_amount * 0.03)),
                    "Direct Debit",
                    is_recurring=True,
                )

            if has_savings_transfer:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(26, 29))),
                    "Transfer",
                    "Savings",
                    "FutureFund",
                    -money(rng.normal(savings_amount, savings_amount * 0.05)),
                    "Standing Order",
                    is_recurring=True,
                    location="Online",
                )

            for merchant in subscription_merchants:
                add_transaction(
                    rows,
                    account,
                    month_date(month_start, int(rng.integers(5, 24))),
                    "Expense",
                    "Subscriptions",
                    merchant,
                    -money(rng.uniform(7, 55)),
                    "Direct Debit",
                    is_recurring=True,
                    location="Online",
                )


def add_random_transaction(rows: list[dict[str, object]], accounts: list[dict[str, object]]) -> None:
    account = accounts[int(rng.integers(0, len(accounts)))]
    transaction_date = random_date()

    roll = rng.random()
    if roll < 0.018:
        category = str(rng.choice(["Shopping", "Travel", "Healthcare"]))
        add_transaction(
            rows,
            account,
            transaction_date,
            "Expense",
            category,
            str(rng.choice(["RareCollective", "Harbor Motors", "FlashElectronics"])),
            -money(rng.uniform(900, 4200)),
            payment_method_for(category, "Expense"),
            is_unusual=True,
            location=str(rng.choice(LOCATIONS)),
        )
        return

    if roll < 0.035 and len(rows) + 2 <= TARGET_ROW_COUNT:
        category = str(rng.choice(["Dining", "Shopping", "Transport", "Groceries"]))
        merchant = str(rng.choice(CATEGORY_MERCHANTS[category]))
        amount = expense_amount(category)
        payment_method = payment_method_for(category, "Expense")
        for _ in range(2):
            add_transaction(
                rows,
                account,
                transaction_date,
                "Expense",
                category,
                merchant,
                amount,
                payment_method,
                is_unusual=True,
                location=str(rng.choice(LOCATIONS)),
            )
        return

    category = weighted_choice(
        [
            "Groceries",
            "Transport",
            "Dining",
            "Entertainment",
            "Shopping",
            "Healthcare",
            "Travel",
            "Utilities",
            "Transfers",
            "Refunds",
        ],
        [0.21, 0.14, 0.15, 0.09, 0.16, 0.07, 0.05, 0.05, 0.05, 0.03],
    )

    if category == "Refunds":
        transaction_type = "Refund"
        merchant = str(rng.choice(CATEGORY_MERCHANTS["Refunds"]))
        amount = money(rng.uniform(8, 240))
    elif category == "Transfers":
        transaction_type = "Transfer"
        merchant = str(rng.choice(CATEGORY_MERCHANTS["Transfers"]))
        amount = money(rng.uniform(50, 650)) if rng.random() < 0.2 else -money(rng.uniform(50, 900))
    else:
        transaction_type = "Expense"
        merchant = str(rng.choice(CATEGORY_MERCHANTS[category]))
        amount = expense_amount(category)

    is_unusual = False
    if transaction_type == "Expense" and rng.random() < 0.02:
        amount = money(amount * rng.uniform(3.5, 7.5))
        is_unusual = True

    add_transaction(
        rows,
        account,
        transaction_date,
        transaction_type,
        category,
        merchant,
        amount,
        payment_method_for(category, transaction_type),
        is_recurring=False,
        is_unusual=is_unusual,
        location=str(rng.choice(LOCATIONS)),
    )


def add_running_balances(rows: list[dict[str, object]], accounts: list[dict[str, object]]) -> pd.DataFrame:
    opening_balances = {str(account["account_id"]): float(account["opening_balance"]) for account in accounts}
    df = pd.DataFrame(rows)

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df = df.sort_values(["account_id", "transaction_date", "_sequence"]).reset_index(drop=True)
    df["balance_after_transaction"] = (
        df.groupby("account_id")["amount"].cumsum() + df["account_id"].map(opening_balances)
    ).round(2)

    df = df.sort_values(["transaction_date", "account_id", "_sequence"]).reset_index(drop=True)
    df.insert(0, "transaction_id", [f"TXN{i:07d}" for i in range(1, len(df) + 1)])
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")

    columns = [
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
    return df[columns]


def main() -> None:
    accounts = build_accounts()
    rows: list[dict[str, object]] = []

    add_recurring_transactions(rows, accounts)
    while len(rows) < TARGET_ROW_COUNT:
        add_random_transaction(rows, accounts)

    df = add_running_balances(rows, accounts)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(df):,} rows and saved raw transactions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
