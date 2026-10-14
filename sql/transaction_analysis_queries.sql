/*
Financial Transactions Analytics Dashboard
PostgreSQL analysis queries

Recommended workflow:
1. Run scripts/generate_transactions.py
2. Run scripts/clean_transactions.py
3. Run sql/create_transactions_table.sql in a dedicated database
4. Load data/cleaned/transactions_cleaned.csv into the transactions table
5. Run the analysis queries below
*/

-- 1. Row count check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT account_id) AS unique_accounts
FROM transactions;

-- 2. Date range check
SELECT
    MIN(transaction_date) AS first_transaction_date,
    MAX(transaction_date) AS last_transaction_date,
    COUNT(DISTINCT transaction_month) AS months_covered
FROM transactions;

-- 3. Total income
SELECT
    ROUND(SUM(income_amount), 2) AS total_income
FROM transactions;

-- 4. Total expenses
SELECT
    ROUND(SUM(expense_amount), 2) AS total_expenses
FROM transactions;

-- 5. Operating surplus and net cash movement
SELECT
    ROUND(SUM(income_amount) - SUM(expense_amount), 2) AS operating_surplus,
    ROUND(SUM(net_amount), 2) AS net_cash_flow
FROM transactions;

-- 6. Monthly cash flow trend
SELECT
    transaction_month,
    TO_CHAR(transaction_month, 'Mon YYYY') AS month_label,
    ROUND(SUM(income_amount), 2) AS total_income,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    ROUND(SUM(income_amount) - SUM(expense_amount), 2) AS operating_surplus,
    ROUND(SUM(net_amount), 2) AS net_cash_flow,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY transaction_month
ORDER BY transaction_month;

-- 7. Spending by category
SELECT
    category,
    ROUND(SUM(expense_amount), 2) AS total_spend,
    COUNT(*) FILTER (WHERE transaction_type = 'Expense') AS expense_transactions,
    ROUND(AVG(expense_amount) FILTER (WHERE transaction_type = 'Expense'), 2) AS average_expense
FROM transactions
WHERE transaction_type = 'Expense'
GROUP BY category
ORDER BY total_spend DESC;

-- 8. Top merchants by spend
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

-- 9. Recurring expenses (excludes recurring income and transfers)
SELECT
    merchant,
    category,
    payment_method,
    COUNT(*) AS recurring_transaction_count,
    ROUND(SUM(expense_amount), 2) AS recurring_expense_total,
    ROUND(AVG(expense_amount), 2) AS average_recurring_expense,
    MIN(transaction_date) AS first_seen,
    MAX(transaction_date) AS last_seen
FROM transactions
WHERE is_recurring = true
  AND transaction_type = 'Expense'
GROUP BY merchant, category, payment_method
ORDER BY recurring_expense_total DESC;

-- 10. Unusual transactions
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

-- 11. Payment method breakdown
SELECT
    payment_method,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_abs), 2) AS total_transaction_value,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS transaction_share_pct
FROM transactions
GROUP BY payment_method
ORDER BY transaction_count DESC;

-- 12. Budget performance by category
SELECT
    transaction_month,
    TO_CHAR(transaction_month, 'Mon YYYY') AS month_label,
    category,
    MAX(category_budget) AS monthly_budget,
    MAX(category_month_expense) AS actual_expense,
    MAX(budget_variance) AS budget_variance,
    MAX(budget_variance_pct) AS budget_variance_pct,
    MAX(budget_utilisation_pct) AS budget_utilisation_pct,
    MAX(budget_status) AS budget_status
FROM transactions
WHERE category_budget > 0
GROUP BY transaction_month, category
ORDER BY transaction_month, actual_expense DESC;

-- 13. High-spend categories
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

-- 14. Customers/accounts with highest expenses
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

-- 15. Month-over-month spending change
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

-- 16. Duplicate-looking transactions
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

-- 17. Large transactions above threshold
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

-- 18. Final summary query suitable for dashboard KPIs
SELECT
    ROUND(SUM(income_amount), 2) AS total_income,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    ROUND(SUM(income_amount) - SUM(expense_amount), 2) AS operating_surplus,
    ROUND(SUM(net_amount), 2) AS net_cash_flow,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT account_id) AS account_count,
    ROUND(AVG(amount_abs), 2) AS average_transaction_amount,
    ROUND(
        SUM(expense_amount) FILTER (
            WHERE is_recurring = true AND transaction_type = 'Expense'
        ),
        2
    ) AS recurring_expense_total,
    COUNT(*) FILTER (WHERE is_unusual = true) AS unusual_transaction_count,
    ROUND(SUM(amount_abs) FILTER (WHERE is_unusual = true), 2) AS unusual_transaction_value,
    ROUND(100.0 * SUM(expense_amount) / NULLIF(SUM(income_amount), 0), 2) AS expense_ratio_pct
FROM transactions;

-- 19. Portfolio-level budget KPI summary at month/category grain
WITH monthly_category_budget AS (
    SELECT
        transaction_month,
        category,
        MAX(category_budget) AS monthly_budget,
        MAX(category_month_expense) AS actual_expense
    FROM transactions
    WHERE category_budget > 0
    GROUP BY transaction_month, category
)
SELECT
    ROUND(SUM(monthly_budget), 2) AS total_budget,
    ROUND(SUM(actual_expense), 2) AS total_actual_expense,
    ROUND(SUM(monthly_budget) - SUM(actual_expense), 2) AS budget_variance,
    ROUND(100.0 * SUM(actual_expense) / NULLIF(SUM(monthly_budget), 0), 2)
        AS budget_utilisation_pct
FROM monthly_category_budget;

