# Power BI Dashboard — v1.0 Validation Guide

## Scope and Verification Status

The v1.0 report scope is exactly two pages:

1. **Executive Overview**
2. **Spending Analysis**

`financial_transactions_dashboard.pbix` has been preserved unchanged. Archive integrity passed, and read-only layout inspection confirmed exactly two pages: **Executive Overview** (12 visual containers) and **Spending Analysis** (13 visual containers). The package also contains a data model, metadata, settings, and theme resources.

The layout queries reference transaction fields and the measures `Total Income`, `Total Expenses`, `Net Cash Flow`, `Transaction Count`, `Average Transaction Amount`, and `Recurring Payment Total`. They contain no references to retail or sales fields. This confirms the report belongs to the financial-transactions project, but it also identifies one required correction: replace the ambiguous `Recurring Payment Total` visual measure with `Recurring Expenses` below. Add `Operating Surplus` so the report distinguishes income less expenses from total signed cash movement.

Power BI Desktop and `pbi-tools` were not available during automated verification. Consequently, the rendered visuals, DAX definitions, relationships, formatting, data freshness, and interactions are **not verified**. Use this guide to complete the required desktop check; do not interpret package-level layout inspection as visual validation.

The unrelated local file `Retail Sales Dashboard.pbix` is explicitly excluded by `.gitignore` and is not part of this project.

## Data Source and Model

Use `data/cleaned/transactions_cleaned.csv` as the source table named `transactions`. After refreshing, confirm:

- 9,000 rows and 26 columns;
- `transaction_date` and `transaction_month` are Date fields;
- monetary and ratio fields are Decimal Number;
- `transaction_year` is Whole Number;
- `is_recurring` and `is_unusual` are True/False; and
- transaction IDs contain 9,000 distinct values.

Create a calendar table:

```DAX
Calendar =
ADDCOLUMNS(
    CALENDAR(
        MIN(transactions[transaction_date]),
        MAX(transactions[transaction_date])
    ),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "MMM"),
    "Month Year", FORMAT([Date], "MMM YYYY"),
    "Month Sort", YEAR([Date]) * 100 + MONTH([Date])
)
```

Sort `Calendar[Month Year]` by `Calendar[Month Sort]`. Create one active, single-direction, one-to-many relationship from `Calendar[Date]` to `transactions[transaction_date]`, and mark `Calendar` as the date table.

## Reconciled DAX Measures

Replace ambiguous or conflicting measures with these definitions.

```DAX
Total Income =
SUM(transactions[income_amount])
```

```DAX
Total Expenses =
SUM(transactions[expense_amount])
```

```DAX
Operating Surplus =
[Total Income] - [Total Expenses]
```

```DAX
Refund Inflows =
CALCULATE(
    SUM(transactions[net_amount]),
    transactions[transaction_type] = "Refund"
)
```

```DAX
Net Transfers =
CALCULATE(
    SUM(transactions[net_amount]),
    transactions[transaction_type] = "Transfer"
)
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
Average Transaction Value =
AVERAGE(transactions[amount_abs])
```

```DAX
Recurring Expenses =
CALCULATE(
    SUM(transactions[expense_amount]),
    transactions[is_recurring] = TRUE(),
    transactions[transaction_type] = "Expense"
)
```

The budget fields repeat on transaction rows. These measures aggregate once per visible month/category and must replace direct sums:

```DAX
Budget Amount =
SUMX(
    SUMMARIZE(
        FILTER(transactions, transactions[category_budget] > 0),
        transactions[transaction_month],
        transactions[category],
        "Monthly Budget", MAX(transactions[category_budget])
    ),
    [Monthly Budget]
)
```

```DAX
Actual Budgeted Expense =
SUMX(
    SUMMARIZE(
        FILTER(transactions, transactions[category_budget] > 0),
        transactions[transaction_month],
        transactions[category],
        "Monthly Actual", MAX(transactions[category_month_expense])
    ),
    [Monthly Actual]
)
```

```DAX
Budget Variance =
[Budget Amount] - [Actual Budgeted Expense]
```

```DAX
Budget Utilisation % =
DIVIDE([Actual Budgeted Expense], [Budget Amount])
```

```DAX
Exceeded Budget Periods =
COUNTROWS(
    FILTER(
        SUMMARIZE(
            FILTER(transactions, transactions[category_budget] > 0),
            transactions[transaction_month],
            transactions[category],
            "Status", MAX(transactions[budget_status])
        ),
        [Status] = "Exceeded Budget"
    )
)
```

## Expected Unfiltered Results

Use these values after refresh to verify the model and measures:

| Measure | Expected value |
| --- | ---: |
| Transaction Count | 9,000 |
| Total Income | £4,710,640.23 |
| Total Expenses | £1,995,612.11 |
| Operating Surplus | £2,715,028.12 |
| Refund Inflows | £4,517.54 |
| Net Transfers | −£479,014.83 |
| Net Cash Flow | £2,240,530.83 |
| Average Transaction Value | £800.74 |
| Recurring Expenses | £1,704,954.66 |
| Budget Amount | £1,981,200.00 |
| Actual Budgeted Expense | £1,995,612.11 |
| Budget Variance | −£14,412.11 |
| Budget Utilisation | 100.73% |
| Exceeded Budget Periods | 66 |

The reconciliation must hold:

```text
Operating Surplus + Refund Inflows + Net Transfers = Net Cash Flow
```

## Page 1 — Executive Overview

Purpose: explain overall financial position and cash movement quickly.

Required content:

- KPI cards: Total Income, Total Expenses, Operating Surplus, Net Cash Flow, Transaction Count.
- Monthly comparison: Total Income and Total Expenses by `Calendar[Month Year]`.
- Cash-flow bridge or supporting cards: Refund Inflows and Net Transfers.
- Expense category bar chart using `Total Expenses`, filtered to Expense transactions.
- Slicers: date, category, and transaction type.

Use consistent currency units on every card. Do not label Operating Surplus as Net Cash Flow.

## Page 2 — Spending Analysis

Purpose: explain expense drivers, recurring commitments, and budget performance.

Required content:

- KPI cards: Total Expenses, Recurring Expenses, Average Transaction Value, Budget Utilisation %.
- Spending by category, sorted descending.
- Monthly expense trend.
- Budget vs actual by category using the deduplicated measures.
- Merchant or transaction detail table for investigation.
- Slicers: date, category, merchant, payment method, recurring flag, and budget status as space allows.

Do not use `COUNTROWS(transactions)` to chart budget-status periods; that counts transactions rather than month/category outcomes.

## Visual Standards

- Use a light background, dark text, and one restrained accent colour.
- Reserve green/red for meaningful positive/negative states; ensure accessibility does not rely on colour alone.
- Format currency consistently as GBP with two decimals on validation cards; display units may be used on charts.
- Format ratios as percentages and keep date labels chronologically sorted.
- Align cards and visuals to a consistent grid with readable titles.
- Remove decorative visuals that do not answer an analytical question.

## Desktop Validation Checklist

- [ ] Refresh succeeds from the repository-relative CSV after reconnecting the source.
- [ ] Row count, column count, data types, and distinct transaction IDs are correct.
- [ ] Only the two release pages are visible.
- [ ] All expected unfiltered KPI values match the table above.
- [ ] Operating Surplus and Net Cash Flow are separately named and reconciled.
- [ ] Recurring Expenses excludes salary and transfers.
- [ ] Budget visuals use month/category-grain measures and show 66 exceeded periods.
- [ ] Month labels sort chronologically.
- [ ] Slicers cross-filter all intended visuals and reset cleanly.
- [ ] Cards and charts use consistent GBP/percentage formats and accessible colours.
- [ ] No absolute local path, unrelated retail dataset, or sensitive data appears.
- [ ] Save the validated report back to `dashboard/financial_transactions_dashboard.pbix`.

## Genuine Screenshots Required

After validation, export or capture the two report pages at a readable resolution:

```text
dashboard/screenshots/executive_overview.png
dashboard/screenshots/spending_analysis.png
```

Add those real images to the README only after their numbers match the expected values. Do not create mockups and label them as Power BI output.
