# Financial Transactions Analytics Dashboard - Power BI Plan

## Dashboard Title

Financial Transactions Analytics Dashboard

## Dashboard Purpose

This Power BI dashboard is designed to turn cleaned transaction data into a clear reporting experience for finance and business stakeholders. It focuses on income, expenses, net cash flow, recurring payments, unusual transactions, category spend and budget performance.

Recommended data source:

```text
data/cleaned/transactions_cleaned.csv
```

## Data Model Setup

1. Open Power BI Desktop.
2. Select **Get Data > Text/CSV**.
3. Load `data/cleaned/transactions_cleaned.csv`.
4. Confirm these data types:
   - `transaction_date`: Date
   - `transaction_month`: Date
   - `transaction_year`: Whole number
   - `amount`, `amount_abs`, `income_amount`, `expense_amount`, `net_amount`: Decimal number
   - `category_budget`, `category_month_expense`, `budget_variance`, `budget_variance_pct`: Decimal number
   - `is_recurring`, `is_unusual`: True/False
5. Create a calendar table:

```DAX
Calendar =
ADDCOLUMNS(
    CALENDAR(MIN(transactions[transaction_date]), MAX(transactions[transaction_date])),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "MMM"),
    "Month Year", FORMAT([Date], "MMM YYYY")
)
```

6. Create a relationship:
   - `Calendar[Date]` to `transactions[transaction_date]`
   - Relationship type: One-to-many
   - Filter direction: Single

## Suggested Slicers

Use these slicers across the report pages where useful:

- `Calendar[Date]`
- `transactions[transaction_month]`
- `transactions[category]`
- `transactions[customer_id]`
- `transactions[account_id]`
- `transactions[transaction_type]`
- `transactions[payment_method]`
- `transactions[budget_status]`

## DAX Measures

```DAX
Total Income =
SUM(transactions[income_amount])
```

```DAX
Total Expenses =
SUM(transactions[expense_amount])
```

```DAX
Net Cash Flow =
SUM(transactions[net_amount])
```

```DAX
Transaction Count =
COUNTROWS(transactions)
```

```DAX
Average Transaction Amount =
AVERAGE(transactions[amount_abs])
```

```DAX
Recurring Payment Total =
CALCULATE(
    SUM(transactions[amount_abs]),
    transactions[is_recurring] = TRUE()
)
```

```DAX
Unusual Transaction Count =
CALCULATE(
    COUNTROWS(transactions),
    transactions[is_unusual] = TRUE()
)
```

```DAX
Unusual Transaction Value =
CALCULATE(
    SUM(transactions[amount_abs]),
    transactions[is_unusual] = TRUE()
)
```

```DAX
Expense Ratio =
DIVIDE([Total Expenses], [Total Income])
```

```DAX
Budget Amount =
SUMX(
    SUMMARIZE(
        transactions,
        transactions[transaction_month],
        transactions[category],
        "MonthlyBudget", MAX(transactions[category_budget])
    ),
    [MonthlyBudget]
)
```

```DAX
Actual Budgeted Category Expense =
SUMX(
    SUMMARIZE(
        transactions,
        transactions[transaction_month],
        transactions[category],
        "MonthlyExpense", MAX(transactions[category_month_expense])
    ),
    [MonthlyExpense]
)
```

```DAX
Budget Variance =
[Budget Amount] - [Actual Budgeted Category Expense]
```

```DAX
Budget Variance % =
DIVIDE([Budget Variance], [Budget Amount])
```

```DAX
Month-over-Month Expense Change =
VAR PreviousMonthExpenses =
    CALCULATE(
        [Total Expenses],
        DATEADD('Calendar'[Date], -1, MONTH)
    )
RETURN
    [Total Expenses] - PreviousMonthExpenses
```

```DAX
Month-over-Month Expense Change % =
VAR PreviousMonthExpenses =
    CALCULATE(
        [Total Expenses],
        DATEADD('Calendar'[Date], -1, MONTH)
    )
RETURN
    DIVIDE([Total Expenses] - PreviousMonthExpenses, PreviousMonthExpenses)
```

## Recommended Design Style

Use a clean finance/reporting palette:

- Deep navy: `#18324A`
- Teal: `#1F8A8A`
- Green for income and positive cash flow: `#2E7D32`
- Red for expenses and negative variance: `#C62828`
- Amber for warning or unusual transaction indicators: `#F9A825`
- Light grey background: `#F5F7FA`
- Dark text: `#1F2933`

Keep the report light, readable and business-focused. Use consistent KPI formatting and avoid unnecessary decoration.

## Page 1: Executive Overview

Purpose: Provide a fast summary of financial performance.

Recommended visuals:

- KPI card: `[Total Income]`
- KPI card: `[Total Expenses]`
- KPI card: `[Net Cash Flow]`
- KPI card: `[Transaction Count]`
- Line and clustered column chart: monthly income vs expenses
  - X-axis: `Calendar[Month Year]`
  - Column values: `[Total Expenses]`
  - Line values: `[Total Income]`
- Donut chart: category spending breakdown
  - Legend: `transactions[category]`
  - Values: `[Total Expenses]`
- Bar chart: payment method breakdown
  - Axis: `transactions[payment_method]`
  - Values: `[Transaction Count]`

Layout guidance:

- Place KPI cards across the top row.
- Use the monthly trend chart as the main visual.
- Place category and payment method visuals below the main trend chart.

## Page 2: Spending Analysis

Purpose: Explain where money is going and which categories or merchants drive the most spend.

Recommended visuals:

- Bar chart: spending by category
  - Axis: `transactions[category]`
  - Values: `[Total Expenses]`
  - Sort descending by `[Total Expenses]`
- Bar chart: top merchants
  - Axis: `transactions[merchant]`
  - Values: `[Total Expenses]`
  - Visual filter: Top 10 by `[Total Expenses]`
- Line chart: monthly spending trend
  - X-axis: `Calendar[Month Year]`
  - Values: `[Total Expenses]`
- Matrix: high-spend categories
  - Rows: `transactions[category]`
  - Values: `[Total Expenses]`, `[Average Transaction Amount]`, `[Transaction Count]`

Suggested slicers:

- Date
- Category
- Customer ID
- Transaction type
- Payment method

Layout guidance:

- Put slicers in a left-side panel or top filter row.
- Make the category and merchant charts the main comparison visuals.
- Use the matrix for detail rather than as the main visual.

## Page 3: Recurring and Unusual Transactions

Purpose: Highlight regular payments, possible anomalies and transactions worth review.

Recommended visuals:

- KPI card: `[Recurring Payment Total]`
- KPI card: `[Unusual Transaction Count]`
- KPI card: `[Unusual Transaction Value]`
- Table: recurring payments
  - Fields: `merchant`, `category`, `payment_method`, `amount_abs`, `transaction_date`
  - Filter: `is_recurring = True`
- Table: unusual transactions
  - Fields: `transaction_id`, `transaction_date`, `customer_id`, `account_id`, `category`, `merchant`, `amount`, `payment_method`
  - Filter: `is_unusual = True`
- Matrix with conditional formatting: spend spikes by month and category
  - Rows: `transactions[category]`
  - Columns: `Calendar[Month Year]`
  - Values: `[Total Expenses]`
- Bar chart: large transactions
  - Axis: `transactions[merchant]`
  - Values: `transactions[amount_abs]`
  - Filter: `amount_abs >= 1000`

Suggested slicers:

- Date
- Category
- Merchant
- Payment method
- Customer ID

Layout guidance:

- Put unusual transaction KPIs at the top.
- Use tables for investigation detail.
- Use conditional formatting to make spikes easy to identify.

## Page 4: Budget Performance

Purpose: Compare actual spending with benchmark budgets and identify categories needing action.

Recommended visuals:

- Clustered bar chart: budget vs actual by category
  - Axis: `transactions[category]`
  - Values: `[Budget Amount]`, `[Actual Budgeted Category Expense]`
  - Filter: `category_budget > 0`
- Table: over-budget categories
  - Fields: `transaction_month`, `category`, `category_budget`, `category_month_expense`, `budget_variance`, `budget_status`
  - Filter: `budget_status = Over Budget`
- Donut or stacked bar chart: budget status
  - Legend: `transactions[budget_status]`
  - Values: `[Transaction Count]`
- Text box: recommendations
  - Review recurring costs in high-spend categories.
  - Set alerts for unusual high-value transactions.
  - Investigate repeated over-budget categories.
  - Separate essential and discretionary spend.

Suggested slicers:

- Date
- Category
- Budget status
- Transaction type

Layout guidance:

- Place budget vs actual at the top.
- Put over-budget details below the main visual.
- Keep recommendations short and action-focused.

## Screenshot Checklist

After building the Power BI report, export or screenshot each page and save it in `dashboard/screenshots/`.

Expected files:

```text
dashboard/screenshots/executive_overview.png
dashboard/screenshots/spending_analysis.png
dashboard/screenshots/recurring_unusual_transactions.png
dashboard/screenshots/budget_performance.png
```

## Final Screenshot Checklist

After building the Power BI dashboard, save these screenshots:

* dashboard/screenshots/executive_overview.png
* dashboard/screenshots/spending_analysis.png
* dashboard/screenshots/recurring_unusual_transactions.png
* dashboard/screenshots/budget_performance.png

## Final GitHub Update Checklist

After screenshots are added:

1. Add the four screenshot files to `dashboard/screenshots/`.
2. Update the README dashboard screenshots section with image links and a short explanation for each page.
3. Check that the screenshots display correctly on GitHub.
4. Commit and push the dashboard updates:

```bash
git add README.md dashboard/screenshots
git commit -m "Add Power BI dashboard screenshots"
git push
```
