# Financial Transactions Analytics Dashboard - Insights Report

## Executive Summary

This report analyses 9,000 synthetic financial transactions across 120 customers and 149 accounts between 1 January 2025 and 31 December 2025. The dataset includes income, expenses, transfers, refunds, recurring payments and unusual transaction flags.

Total income was 4.71M, total expenses were 2.00M and net cash flow was 2.24M. The overall expense ratio was 42.36%, meaning the synthetic portfolio maintained positive cash flow across the year. The main reporting opportunity is not overall cash flow risk, but the ability to monitor recurring fixed costs, identify unusual activity and manage categories that repeatedly move close to or above budget.

## Key Metrics

| Metric | Value |
| --- | ---: |
| Transactions analysed | 9,000 |
| Customers | 120 |
| Accounts | 149 |
| Date range | 2025-01-01 to 2025-12-31 |
| Total income | 4.71M |
| Total expenses | 2.00M |
| Net cash flow | 2.24M |
| Average transaction value | 800.74 |
| Expense ratio | 42.36% |
| Recurring transactions | 7,344 |
| Unusual transactions | 129 |
| Unusual transaction value | 113,484.26 |
| Duplicate-looking transaction groups | 31 |

## Monthly Spending Trends

Monthly expenses were stable across the year, ranging from 160,855.50 in January to 171,381.70 in July. Net cash flow was positive in every month, with the strongest month in January at 193,093.18 and the lowest month in December at 183,049.05.

This pattern suggests that income is predictable and that month-to-month movement is mainly driven by variable spend categories rather than core income volatility. A dashboard should therefore focus on highlighting changes in category spend and identifying months where discretionary spend increases.

## Category Insights

Rent was the largest expense category at 1.35M, making it the main fixed-cost driver. Utilities were the second largest category at 208,573.33, followed by shopping at 90,598.91, insurance at 77,871.09 and healthcare at 76,939.52.

The category mix is useful for reporting because it separates essential recurring spend from more controllable variable spend. Rent and utilities explain a large share of total expense value, while shopping, travel, dining and entertainment are better candidates for budget monitoring and behavioural insight.

## Merchant Insights

CityRent was the highest-spend merchant at 1.35M, which aligns with rent being the largest category. PowerGrid, WaterWorks and MobileConnect were also high-value merchants, reflecting the importance of utilities in recurring monthly spend.

Rare or less frequent merchants such as FlashElectronics, RareCollective and Harbor Motors also appeared in high-spend analysis. In a real reporting process, these merchants would be useful to review because high-value, low-frequency transactions can indicate one-off purchases, unusual behaviour or transactions that need further context.

## Recurring Payments

The dataset contains 7,344 recurring transactions. Recurring income is mainly salary-related, while recurring expenses are concentrated in rent, utilities, insurance, healthcare/gym payments and subscriptions.

Recurring expenses totalled 1.70M. This makes recurring payment analysis important because fixed costs reduce flexibility in future months. A practical dashboard should allow users to separate recurring spend from non-recurring spend and identify merchants with high regular payment totals.

## Unusual Transactions

There were 129 unusual transactions with a combined value of 113,484.26. These include high-value payments, rare merchant activity and duplicate-looking payments. The dataset also contains 31 duplicate-looking transaction groups based on matching account, transaction date, merchant, category and amount.

These transactions are not automatically fraudulent because the dataset is synthetic and review flags are rule-based. However, they are suitable for exception reporting. In a finance reporting context, these records would be prioritised for review, especially where high transaction values and rare merchants appear together.

## Budget Performance

Budget performance was measured using portfolio-level monthly category benchmarks. Across month/category combinations, 90 were within budget, 38 were near budget and 28 were over budget.

The most frequent over-budget categories were:

| Category | Over-budget months |
| --- | ---: |
| Shopping | 6 |
| Travel | 5 |
| Groceries | 4 |
| Healthcare | 4 |
| Dining | 3 |
| Entertainment | 3 |
| Transport | 3 |

Shopping and travel are the clearest budget control opportunities because they exceeded budget most often and are more variable than rent or utilities. Groceries and healthcare should also be monitored because repeated over-budget months may indicate sustained cost pressure rather than isolated spikes.

## Recommendations

1. Track recurring payments separately from non-recurring spend so fixed monthly commitments are visible.
2. Review high recurring merchants and subscription-style payments for possible cancellation, consolidation or renegotiation.
3. Add dashboard alerts or review rules for transactions above 1,000 and transactions linked to rare merchants.
4. Investigate duplicate-looking transaction groups using account, date, merchant, category and amount matching.
5. Monitor shopping, travel, groceries and healthcare because they show repeated over-budget behaviour.
6. Use monthly cash flow reporting to identify changes early and support financial planning.
7. Separate essential and discretionary categories in future reporting to make recommendations easier to act on.

## Limitations

This dataset is synthetic and created for portfolio demonstration. It does not contain real customer data, real bank accounts, confirmed fraud outcomes, credit risk data or external economic factors. Budget values are benchmark assumptions and should be adjusted if the project is adapted to a different business scenario.

The unusual transaction flag is designed for analytical review, not as a production fraud model. It should be interpreted as a prompt for investigation rather than a confirmed risk label.

## Next Steps

1. Build the Power BI dashboard using `data/cleaned/transactions_cleaned.csv`.
2. Save dashboard screenshots in `dashboard/screenshots/`.
3. Add the completed screenshots to the README.
4. Extend the SQL analysis with optional customer or account segmentation.
5. Add rolling-average anomaly logic for category and merchant-level spike detection.
6. Prepare a short project walkthrough for interview use.

