/*
Create the cleaned transaction table in a dedicated PostgreSQL database.
This script replaces only the table named transactions in the selected database.
*/

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_month DATE NOT NULL,
    transaction_year INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    account_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    merchant VARCHAR(100) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    amount_abs NUMERIC(12, 2) NOT NULL,
    income_amount NUMERIC(12, 2) NOT NULL,
    expense_amount NUMERIC(12, 2) NOT NULL,
    net_amount NUMERIC(12, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    is_recurring BOOLEAN NOT NULL,
    is_unusual BOOLEAN NOT NULL,
    balance_after_transaction NUMERIC(12, 2) NOT NULL,
    category_budget NUMERIC(12, 2) NOT NULL,
    category_month_expense NUMERIC(12, 2) NOT NULL,
    budget_variance NUMERIC(12, 2) NOT NULL,
    budget_variance_pct NUMERIC(12, 4) NOT NULL,
    budget_utilisation_pct NUMERIC(12, 4) NOT NULL,
    budget_status VARCHAR(30) NOT NULL,
    CONSTRAINT valid_transaction_type
        CHECK (transaction_type IN ('Income', 'Expense', 'Transfer', 'Refund')),
    CONSTRAINT nonnegative_absolute_amount CHECK (amount_abs >= 0),
    CONSTRAINT nonnegative_income_amount CHECK (income_amount >= 0),
    CONSTRAINT nonnegative_expense_amount CHECK (expense_amount >= 0)
);

-- From psql opened at the repository root, load the cleaned data with:
-- \copy transactions FROM 'data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true)
