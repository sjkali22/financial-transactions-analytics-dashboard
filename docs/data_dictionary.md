# Data Dictionary

## Dataset

This data dictionary documents the cleaned synthetic financial transactions dataset used for analysis, SQL queries and Power BI dashboarding.

Dataset path:

```text
data/cleaned/transactions_cleaned.csv
```

## Fields

| Field Name | Data Type | Description | Example |
| --- | --- | --- | --- |
| `transaction_id` | Text | Unique transaction identifier created for each row in the dataset. | `TXN0000001` |
| `transaction_date` | Date | Date when the transaction occurred. | `2025-01-01` |
| `transaction_month` | Date | First day of the transaction month, used for monthly grouping and dashboard trends. | `2025-01-01` |
| `transaction_year` | Integer | Calendar year of the transaction. | `2025` |
| `month_name` | Text | Month name derived from the transaction date. | `January` |
| `account_id` | Text | Synthetic account identifier linked to the transaction. | `ACC00010` |
| `customer_id` | Text | Synthetic customer identifier linked to the account. | `CUST0008` |
| `transaction_type` | Text | Transaction classification such as income, expense, transfer or refund. | `Expense` |
| `category` | Text | Reporting category assigned to the transaction. | `Rent` |
| `merchant` | Text | Fictional or generic merchant name. | `CityRent` |
| `amount` | Decimal | Signed transaction value. Income and refunds are generally positive, while expenses and outgoing transfers are generally negative. | `-1322.26` |
| `amount_abs` | Decimal | Absolute transaction value used for spend analysis and transaction size comparisons. | `1322.26` |
| `income_amount` | Decimal | Positive value populated for income transactions and zero for non-income rows. | `0.00` |
| `expense_amount` | Decimal | Positive expense value populated for expense transactions and zero for non-expense rows. | `1322.26` |
| `net_amount` | Decimal | Signed value used for net cash flow calculations. | `-1322.26` |
| `payment_method` | Text | Payment channel or method used for the transaction. | `Direct Debit` |
| `location` | Text | Synthetic transaction location or online channel. | `Glasgow` |
| `is_recurring` | Boolean | Indicates whether the transaction is part of a regular payment pattern. | `True` |
| `is_unusual` | Boolean | Indicates whether the transaction has been flagged for review as unusual. | `False` |
| `balance_after_transaction` | Decimal | Running account balance after the transaction is applied. | `2320.31` |
| `category_budget` | Decimal | Monthly benchmark budget assigned to the transaction category. | `112000.00` |
| `category_month_expense` | Decimal | Total expense value for the same category and month. | `112523.47` |
| `budget_variance` | Decimal | Difference between the category budget and actual monthly category expense. Positive values are under budget and negative values are over budget. | `-523.47` |
| `budget_variance_pct` | Decimal | Budget variance as a percentage of the category budget. | `-0.0047` |
| `budget_status` | Text | Budget performance label based on actual monthly spend compared with the benchmark budget. | `Near Budget` |

## Notes

- The dataset is synthetic and created for portfolio use.
- Negative and positive amount handling depends on the project logic: expenses and most outgoing transfers are negative, while income, refunds and some incoming transfers are positive.
- Derived fields were created to support reporting, dashboard KPIs, SQL aggregation and business analysis.
- `is_unusual` is used to flag potential anomalies or transactions worth reviewing.
- `is_recurring` is used to identify regular payment patterns such as salary, rent, utilities, subscriptions, insurance and savings transfers.

