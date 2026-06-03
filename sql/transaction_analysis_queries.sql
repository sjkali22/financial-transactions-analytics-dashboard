/*
Financial Transactions Analytics Dashboard
PostgreSQL analysis queries

Recommended workflow:
1. Run scripts/generate_transactions.py
2. Run scripts/clean_transactions.py
3. Create this table in PostgreSQL
4. Load data/cleaned/transactions_cleaned.csv into the transactions table
5. Run the analysis queries below
*/

-- 1. Create table statement for cleaned transactions
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
    budget_status VARCHAR(30) NOT NULL
);

-- 2. Load/check data instructions or notes
-- In psql, update the absolute file path if needed:
-- \copy transactions FROM 'data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true);
--
-- If running from another directory, use the full local path, for example:
-- \copy transactions FROM '/Users/yourname/path/to/financial-transactions-analytics-dashboard/data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true);

-- 3. Row count check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT account_id) AS unique_accounts
FROM transactions;

-- 4. Date range check
SELECT
    MIN(transaction_date) AS first_transaction_date,
    MAX(transaction_date) AS last_transaction_date,
    COUNT(DISTINCT transaction_month) AS months_covered
FROM transactions;

-- 5. Total income
SELECT
    ROUND(SUM(income_amount), 2) AS total_income
FROM transactions;

-- 6. Total expenses
SELECT
    ROUND(SUM(expense_amount), 2) AS total_expenses
FROM transactions;

-- 7. Net cash flow
SELECT
    ROUND(SUM(net_amount), 2) AS net_cash_flow
FROM transactions;

-- 8. Monthly cash flow trend
SELECT
    transaction_month,
    TO_CHAR(transaction_month, 'Mon YYYY') AS month_label,
    ROUND(SUM(income_amount), 2) AS total_income,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    ROUND(SUM(net_amount), 2) AS net_cash_flow,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY transaction_month
ORDER BY transaction_month;

-- 9. Spending by category
SELECT
    category,
    ROUND(SUM(expense_amount), 2) AS total_spend,
    COUNT(*) FILTER (WHERE transaction_type = 'Expense') AS expense_transactions,
    ROUND(AVG(expense_amount) FILTER (WHERE transaction_type = 'Expense'), 2) AS average_expense
FROM transactions
WHERE transaction_type = 'Expense'
GROUP BY category
ORDER BY total_spend DESC;

-- 10. Top merchants by spend
SELECT
    merchant,
    category,
    ROUND(SUM(expense_amount), 2) AS total_spend,
    COUNT(*) AS transaction_count,
    ROUND(AVG(expense_amount), 2) AS average_transaction_value
FROM transactions
WHERE transaction_type = 'Expense'
GROUP BY merchant, category
ORDER BY total_spend DESC
LIMIT 15;

-- 11. Recurring payments
SELECT
    merchant,
    category,
    payment_method,
    COUNT(*) AS recurring_transaction_count,
    ROUND(SUM(amount_abs), 2) AS recurring_total_value,
    ROUND(AVG(amount_abs), 2) AS average_recurring_value,
    MIN(transaction_date) AS first_seen,
    MAX(transaction_date) AS last_seen
FROM transactions
WHERE is_recurring = true
GROUP BY merchant, category, payment_method
ORDER BY recurring_total_value DESC;

-- 12. Unusual transactions
SELECT
    transaction_id,
    transaction_date,
    customer_id,
    account_id,
    transaction_type,
    category,
    merchant,
    amount,
    payment_method,
    location
FROM transactions
WHERE is_unusual = true
ORDER BY amount_abs DESC, transaction_date;

-- 13. Payment method breakdown
SELECT
    payment_method,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_abs), 2) AS total_transaction_value,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS transaction_share_pct
FROM transactions
GROUP BY payment_method
ORDER BY transaction_count DESC;

-- 14. Budget performance by category
SELECT
    transaction_month,
    TO_CHAR(transaction_month, 'Mon YYYY') AS month_label,
    category,
    MAX(category_budget) AS monthly_budget,
    MAX(category_month_expense) AS actual_expense,
    MAX(budget_variance) AS budget_variance,
    MAX(budget_variance_pct) AS budget_variance_pct,
    MAX(budget_status) AS budget_status
FROM transactions
WHERE category_budget > 0
GROUP BY transaction_month, category
ORDER BY transaction_month, actual_expense DESC;

-- 15. High-spend categories
SELECT
    category,
    ROUND(SUM(expense_amount), 2) AS total_expense,
    ROUND(AVG(expense_amount), 2) AS average_expense,
    MAX(expense_amount) AS largest_single_expense,
    COUNT(*) AS transaction_count
FROM transactions
WHERE transaction_type = 'Expense'
GROUP BY category
HAVING SUM(expense_amount) >= 10000
ORDER BY total_expense DESC;

-- 16. Customers/accounts with highest expenses
SELECT
    customer_id,
    account_id,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    ROUND(SUM(income_amount), 2) AS total_income,
    ROUND(SUM(net_amount), 2) AS net_cash_flow,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY customer_id, account_id
ORDER BY total_expenses DESC
LIMIT 20;

-- 17. Month-over-month spending change
WITH monthly_expenses AS (
    SELECT
        transaction_month,
        ROUND(SUM(expense_amount), 2) AS total_expenses
    FROM transactions
    GROUP BY transaction_month
),
monthly_change AS (
    SELECT
        transaction_month,
        total_expenses,
        LAG(total_expenses) OVER (ORDER BY transaction_month) AS previous_month_expenses
    FROM monthly_expenses
)
SELECT
    transaction_month,
    total_expenses,
    previous_month_expenses,
    ROUND(total_expenses - previous_month_expenses, 2) AS expense_change,
    ROUND(
        100.0 * (total_expenses - previous_month_expenses)
        / NULLIF(previous_month_expenses, 0),
        2
    ) AS expense_change_pct
FROM monthly_change
ORDER BY transaction_month;

-- 18. Duplicate-looking transactions
SELECT
    account_id,
    transaction_date,
    merchant,
    category,
    amount_abs,
    COUNT(*) AS similar_transaction_count,
    STRING_AGG(transaction_id, ', ' ORDER BY transaction_id) AS transaction_ids
FROM transactions
GROUP BY account_id, transaction_date, merchant, category, amount_abs
HAVING COUNT(*) > 1
ORDER BY similar_transaction_count DESC, transaction_date DESC;

-- 19. Large transactions above threshold
SELECT
    transaction_id,
    transaction_date,
    customer_id,
    account_id,
    transaction_type,
    category,
    merchant,
    amount,
    amount_abs,
    is_unusual
FROM transactions
WHERE amount_abs >= 1000
ORDER BY amount_abs DESC;

-- 20. Final summary query suitable for dashboard KPIs
SELECT
    ROUND(SUM(income_amount), 2) AS total_income,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    ROUND(SUM(net_amount), 2) AS net_cash_flow,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT account_id) AS account_count,
    ROUND(AVG(amount_abs), 2) AS average_transaction_amount,
    ROUND(SUM(amount_abs) FILTER (WHERE is_recurring = true), 2) AS recurring_payment_total,
    COUNT(*) FILTER (WHERE is_unusual = true) AS unusual_transaction_count,
    ROUND(SUM(amount_abs) FILTER (WHERE is_unusual = true), 2) AS unusual_transaction_value,
    ROUND(100.0 * SUM(expense_amount) / NULLIF(SUM(income_amount), 0), 2) AS expense_ratio_pct
FROM transactions;

