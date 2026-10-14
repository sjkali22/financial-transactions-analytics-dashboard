# Data Dictionary

## Dataset

`data/cleaned/transactions_cleaned.csv` is the analysis-ready version of the synthetic transaction data. It contains 9,000 rows and 26 columns covering 1 January to 31 December 2025. No field contains real customer or financial information.

## Fields

| Column | Type | Meaning and constraints |
| --- | --- | --- |
| `transaction_id` | Text | Unique, non-null ID in the form `TXN0000001`. |
| `transaction_date` | Date | Transaction date in `YYYY-MM-DD` format. |
| `transaction_month` | Date | First calendar day of the transaction month; derived from `transaction_date`. |
| `transaction_year` | Integer | Four-digit year derived from `transaction_date`. |
| `month_name` | Text | Full English month name derived from `transaction_date`. |
| `account_id` | Text | Fictional account identifier in uppercase. |
| `customer_id` | Text | Fictional customer identifier in uppercase. |
| `transaction_type` | Text | One of `Income`, `Expense`, `Transfer`, or `Refund`. |
| `category` | Text | Reporting category such as Salary, Rent, Shopping, or Savings. |
| `merchant` | Text | Fictional or generic counterparty name. |
| `amount` | Decimal | Signed value: income/refunds are positive; expenses and most outgoing transfers are negative. |
| `amount_abs` | Decimal | Absolute value of `amount`; used for transaction-size comparisons. |
| `income_amount` | Decimal | Positive `amount` for `Income` rows; zero otherwise. |
| `expense_amount` | Decimal | Positive absolute value for `Expense` rows; zero otherwise. |
| `net_amount` | Decimal | Signed `amount`; used for net cash flow including refunds and transfers. |
| `payment_method` | Text | Payment channel such as Direct Debit, Bank Transfer, or Debit Card. |
| `location` | Text | Fictional UK location or `Online`. |
| `is_recurring` | Boolean | Generated flag for a regular transaction pattern. It can apply to income, expenses, or transfers. |
| `is_unusual` | Boolean | Generated review flag for unusual value, merchant, or duplicate-like activity; not a fraud outcome. |
| `balance_after_transaction` | Decimal | Simulated account balance after applying the signed transaction. |
| `category_budget` | Decimal | Portfolio-level monthly benchmark for expense categories; repeated on rows for reporting convenience. |
| `category_month_expense` | Decimal | Sum of `expense_amount` for the same month and category. |
| `budget_variance` | Decimal | `category_budget - category_month_expense`; negative means actual expense exceeded budget. |
| `budget_variance_pct` | Decimal | `budget_variance / category_budget`; zero when no budget exists. |
| `budget_utilisation_pct` | Decimal | `category_month_expense / category_budget`; stored as a decimal ratio, not a 0–100 number. |
| `budget_status` | Text | `Not Budgeted`, `Below Budget`, `Near Limit`, or `Exceeded Budget`. |

## Budget Rules

Budgets exist only for expense categories. They are portfolio-level monthly benchmarks, not per-customer or per-transaction budgets.

| Status | Rule |
| --- | --- |
| `Not Budgeted` | `category_budget = 0` |
| `Below Budget` | utilisation < 90% |
| `Near Limit` | utilisation ≥ 90% and ≤ 100% |
| `Exceeded Budget` | utilisation > 100% |

Because monthly budget and actual values are repeated on transaction rows, aggregate them once per `transaction_month` and `category` using `MAX` or a deduplicated month/category table. Never sum these fields directly across all rows.

## KPI Calculations

| KPI | Calculation |
| --- | --- |
| Total Income | `SUM(income_amount)` |
| Total Expenses | `SUM(expense_amount)` |
| Operating Surplus | Total Income − Total Expenses |
| Net Cash Flow | `SUM(net_amount)`; includes signed refunds and transfers |
| Average Transaction Value | `AVERAGE(amount_abs)` across every transaction |
| Recurring Expenses | `SUM(expense_amount)` where `is_recurring = True` and `transaction_type = 'Expense'` |
| Budget Utilisation | Sum of month/category actuals ÷ sum of month/category budgets |
| Budget Variance | Sum of month/category budgets − sum of month/category actuals |

## Data Quality Contract

- Required columns must be present before transformation.
- Transaction IDs must be unique after cleaning.
- Dates, signed amounts, and balances must parse successfully.
- Zero-value rows and unsupported transaction types are rejected.
- Cleaned data must contain no missing values.
- Income rows must be positive and expense rows negative in the signed `amount` field.
- The cleaning command reports every rejection category rather than silently dropping rows.
