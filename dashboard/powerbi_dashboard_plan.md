# Financial Transactions Analytics Dashboard - Power BI Plan

## Dashboard Goal

Build a four-page Power BI report that helps users understand income, expenses, net cash flow, recurring payments, unusual transactions and budget performance across synthetic financial transaction data.

Recommended data source:

`data/cleaned/transactions_cleaned.csv`

## Data Model Setup

1. Open Power BI Desktop.
2. Select **Get Data > Text/CSV**.
3. Load `data/cleaned/transactions_cleaned.csv`.
4. Confirm these data types:
   - `transaction_date`: Date
   - `transaction_month`: Date
   - `transaction_year`: Whole number
   - `amount`, `amount_abs`, `income_amount`, `expense_amount`, `net_amount`: Decimal number
   - `is_recurring`, `is_unusual`: True/False
5. Create a calendar table for time intelligence:

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

## Suggested DAX Measures

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
Budget Variance =
SUM(transactions[budget_variance])
```

```DAX
Budget Variance % =
DIVIDE([Budget Variance], SUM(transactions[category_budget]))
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

## Suggested Colour Scheme

Use a clean finance/reporting palette:

- Deep navy: `#18324A`
- Teal: `#1F8A8A`
- Green for income/positive cash flow: `#2E7D32`
- Red for expenses/negative variance: `#C62828`
- Amber for warnings: `#F9A825`
- Light grey background: `#F5F7FA`
- Dark text: `#1F2933`

Keep backgrounds light, use navy for headings, green for income, red for expenses, and amber for warning or unusual transaction indicators.

## Page 1: Executive Overview

Purpose: Give a fast executive summary of overall financial performance.

Recommended visuals:

- KPI card: Total Income
  - Field: `[Total Income]`
  - Format: Currency
- KPI card: Total Expenses
  - Field: `[Total Expenses]`
  - Format: Currency
- KPI card: Net Cash Flow
  - Field: `[Net Cash Flow]`
  - Format: Currency
- KPI card: Number of Transactions
  - Field: `[Transaction Count]`
- Line and clustered column chart: Monthly income vs expenses
  - X-axis: `Calendar[Month Year]`
  - Column values: `[Total Expenses]`
  - Line values: `[Total Income]`
  - Sort by: `Calendar[Month Number]`
- Donut chart: Category spending breakdown
  - Legend: `transactions[category]`
  - Values: `[Total Expenses]`
- Bar chart: Payment method breakdown
  - Axis: `transactions[payment_method]`
  - Values: `[Transaction Count]`

Layout guidance:

- Place KPI cards across the top row.
- Use the monthly trend chart as the largest visual in the centre.
- Place category and payment method charts below or to the right depending on screen width.

## Page 2: Spending Analysis

Purpose: Explain where money is going and which categories or merchants drive the most spend.

Recommended visuals:

- Bar chart: Spending by category
  - Axis: `transactions[category]`
  - Values: `[Total Expenses]`
  - Sort descending by `[Total Expenses]`
- Bar chart: Top merchants
  - Axis: `transactions[merchant]`
  - Values: `[Total Expenses]`
  - Visual filter: Top 10 by `[Total Expenses]`
- Line chart: Monthly spending trend
  - X-axis: `Calendar[Month Year]`
  - Values: `[Total Expenses]`
- Matrix: High-spend categories
  - Rows: `transactions[category]`
  - Values: `[Total Expenses]`, `[Average Transaction Amount]`, `[Transaction Count]`

Recommended slicers:

- `Calendar[Date]`
- `transactions[category]`
- `transactions[customer_id]`
- `transactions[transaction_type]`
- `transactions[payment_method]`

Layout guidance:

- Put slicers in a slim panel on the left.
- Use category and merchant bar charts as the main comparison visuals.
- Keep table/matrix visuals below charts for detailed review.

## Page 3: Recurring and Unusual Transactions

Purpose: Highlight fixed costs, unusual activity and possible investigation areas.

Recommended visuals:

- KPI card: Unusual Transaction Count
  - Field: `[Unusual Transaction Count]`
- KPI card: Unusual Transaction Value
  - Field: `[Unusual Transaction Value]`
- Table: Recurring payments
  - Fields: `merchant`, `category`, `payment_method`, `amount_abs`, `transaction_date`
  - Visual filter: `is_recurring = True`
- Table: Unusual transactions
  - Fields: `transaction_id`, `transaction_date`, `customer_id`, `category`, `merchant`, `amount`, `payment_method`
  - Visual filter: `is_unusual = True`
- Heatmap-style matrix: Spend spikes by month/category
  - Rows: `transactions[category]`
  - Columns: `Calendar[Month Year]`
  - Values: `[Total Expenses]`
  - Conditional formatting: background colour by value
- Bar chart: Large transactions
  - Axis: `transactions[merchant]`
  - Values: `transactions[amount_abs]`
  - Visual filter: amount_abs greater than or equal to 1000

Layout guidance:

- Put unusual KPI cards at the top.
- Use the recurring and unusual tables side by side.
- Use conditional formatting to make spikes easy to see.

## Page 4: Budget Performance

Purpose: Compare actual monthly spend with budget and identify categories needing action.

Recommended visuals:

- Clustered bar chart: Budget vs actual by category
  - Axis: `transactions[category]`
  - Values: `transactions[category_budget]`, `transactions[category_month_expense]`
  - Filter: `category_budget > 0`
- Table: Over-budget categories
  - Fields: `transaction_month`, `category`, `category_budget`, `category_month_expense`, `budget_variance`, `budget_status`
  - Visual filter: `budget_status = Over Budget`
- Donut chart or stacked bar: Budget status
  - Legend: `transactions[budget_status]`
  - Values: `[Transaction Count]`
- Text box: Recommendations
  - Review recurring costs in high-spend categories.
  - Set alerts for unusual high-value transactions.
  - Investigate repeated over-budget categories.
  - Separate essential and discretionary spend.

Layout guidance:

- Put the budget vs actual visual at the top.
- Place over-budget details below.
- Keep recommendations short and business-focused.

## Screenshots to Save

After building the Power BI report, export or screenshot each page and save them here:

- `dashboard/screenshots/executive_overview.png`
- `dashboard/screenshots/spending_analysis.png`
- `dashboard/screenshots/recurring_unusual_transactions.png`
- `dashboard/screenshots/budget_performance.png`

## What to Add to GitHub After Screenshots

Once screenshots are saved:

1. Add the four images to the README dashboard section.
2. Include one sentence under each screenshot explaining what the page shows.
3. Commit the screenshots:

```bash
git add dashboard/screenshots README.md
git commit -m "Add Power BI dashboard screenshots"
```

