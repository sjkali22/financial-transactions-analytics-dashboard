# Financial Transactions Analytics — Insights Report

## Analysis Objectives

This report evaluates 9,000 synthetic transactions across 120 fictional customers and 149 fictional accounts from 1 January to 31 December 2025. The objectives are to reconcile financial KPIs, explain expense concentration, quantify recurring commitments, assess budget performance, and identify transactions that merit review.

The data is synthetic. Findings demonstrate analytical methods and must not be interpreted as real customer behaviour, fraud detection, cost savings, or commercial impact.

## Validated KPI Summary

| Metric | Exact result | Definition |
| --- | ---: | --- |
| Total income | £4,710,640.23 | Income transactions only |
| Total expenses | £1,995,612.11 | Expense transactions only, expressed positively |
| Operating surplus | £2,715,028.12 | Income − expenses |
| Refund inflows | £4,517.54 | Signed refund movements |
| Net transfers | −£479,014.83 | Incoming less outgoing transfers |
| Net cash flow | £2,240,530.83 | All signed movements |
| Average transaction value | £800.74 | Mean absolute value across all 9,000 rows |
| Recurring expenses | £1,704,954.66 | Recurring expense rows only |
| Budget utilisation | 100.73% | Month/category actuals ÷ budgets |
| Budget variance | −£14,412.11 | Budget − actual at month/category grain |

Python/pandas results were reconciled to an independent calculation using Python's standard-library `csv` and `Decimal` modules. Each comparable value had a difference of £0.00. A PostgreSQL parser accepted the two schema statements and all 19 analysis statements, but PostgreSQL was not available in the verification environment, so these figures are not described as database-executed SQL results.

## Income, Expenses, and Cash Movement

Operating surplus was £2,715,028.12, while net cash flow was £2,240,530.83. The £474,497.29 difference is fully reconciled:

```text
Operating surplus                  £2,715,028.12
+ refund inflows                       £4,517.54
+ net transfers                     −£479,014.83
= net cash flow                     £2,240,530.83
```

This distinction matters: income less expenses describes operating performance, whereas net cash flow also captures money moved into or out of savings and other accounts.

Monthly expenses were relatively stable, ranging from £160,855.50 in January to £171,381.70 in July. Monthly net cash flow remained positive in the synthetic dataset, from £183,049.05 in December to £193,093.18 in January.

## Expense Concentration

| Expense category | Annual expense |
| --- | ---: |
| Rent | £1,347,716.36 |
| Utilities | £208,573.33 |
| Shopping | £90,598.91 |
| Insurance | £77,871.09 |
| Healthcare | £76,939.52 |
| Travel | £62,875.03 |
| Subscriptions | £55,639.72 |

Rent and utilities dominate the expense profile, reflecting the simulation's large recurring fixed-cost component. Shopping, travel, dining, and entertainment are smaller but more discretionary, so they are more suitable for behavioural budget controls than rent.

## Recurring Expenses

Recurring expenses totalled £1,704,954.66. This metric deliberately excludes recurring salary and savings transfers; including all recurring `amount_abs` values would mix income, expense, and internal movement into one misleading total.

The high recurring share is primarily driven by rent, utilities, insurance, subscriptions, and gym payments. In a real setting, these commitments would be monitored separately because they constrain short-term spending flexibility.

## Budget Performance

The portfolio has £1,981,200.00 of annualised month/category budget and £1,995,612.11 of actual budgeted expense, giving a variance of −£14,412.11 and utilisation of 100.73%.

Across 132 month/category periods:

| Status | Periods | Rule |
| --- | ---: | --- |
| Below Budget | 33 | <90% utilised |
| Near Limit | 33 | 90%–100% utilised |
| Exceeded Budget | 66 | >100% utilised |

Budgets are repeated on transaction rows for dashboard convenience. Every portfolio calculation therefore deduplicates to month/category grain before aggregation.

## Review Indicators

The generated rules flagged 129 unusual transactions with an absolute value of £113,484.26. Matching account, date, merchant, category, and amount identified 31 duplicate-looking groups.

These records are investigation prompts only. A duplicate-looking pair can be legitimate, and an unusual high-value transaction is not evidence of fraud. A real review process would require authorisation data, customer context, merchant verification, and an audit trail.

## Recommendations

1. Present operating surplus and net cash flow together, with transfers and refunds shown as the reconciliation bridge.
2. Monitor recurring expenses separately from income and transfers so committed costs remain visible.
3. Review the rent and utilities base for concentration, then focus adjustable budget controls on discretionary categories.
4. Use the 90% near-limit threshold as an early warning and investigate the 66 exceeded month/category periods.
5. Review unusual and duplicate-looking transactions with contextual evidence before classifying or escalating them.
6. Retain month/category grain in SQL and Power BI budget measures to prevent duplicated budgets.

## Limitations

- All records, identifiers, merchants, balances, and behaviours are simulated.
- Budget amounts are modelling assumptions and have not been approved by a real organisation.
- The unusual flag is generated rather than statistically learned or independently labelled.
- The dataset covers one calendar year, limiting seasonality and long-term trend analysis.
- PostgreSQL execution remains pending even though the SQL logic matches the reconciled schema and definitions.
- The PBIX binary was preserved and identified as a Power BI package, but visual, relationship, DAX, and interaction checks remain pending in Power BI Desktop.
