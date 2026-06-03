# Financial Transactions Analytics Dashboard - Insights Report

## Executive Summary

This project analyses 9,000 synthetic financial transactions across 120 customers and 149 accounts for the period 1 January 2025 to 31 December 2025. The dataset includes income, expenses, transfers, refunds, recurring payments and unusual transaction flags.

Total income was 4.71M, total expenses were 2.00M and net cash flow was 2.24M. The overall expense ratio was 42.36%, meaning expenses represented less than half of income across the synthetic portfolio. This suggests a positive cash flow position overall, but category-level analysis shows recurring fixed costs and several over-budget spending areas that should be monitored.

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

Monthly expenses were relatively stable, ranging from 160,855.50 in January to 171,381.70 in July. Net cash flow remained positive every month, with the strongest month in January at 193,093.18 and the lowest month in December at 183,049.05.

The trend suggests that income is consistent and predictable, while expense variation is mostly driven by shopping, travel, healthcare and other non-rent categories. A dashboard should make month-over-month expense movement visible so unusual increases can be investigated quickly.

## Category Insights

Rent was the largest expense category at 1.35M, representing the main fixed-cost driver in the portfolio. Utilities were the second largest category at 208,573.33, followed by shopping at 90,598.91, insurance at 77,871.09 and healthcare at 76,939.52.

This pattern is realistic for financial transaction reporting: fixed essential costs dominate total spend, while discretionary or variable categories create the most budget volatility. Shopping and travel should be monitored because they had repeated over-budget months and can change quickly across customer segments.

## Merchant Insights

CityRent was the highest-spend merchant at 1.35M, which aligns with rent being the top category. The next highest merchants were PowerGrid, WaterWorks and MobileConnect, showing utilities as another important recurring cost group.

Several unusual or rare merchants also appeared in the top merchant list, including FlashElectronics, RareCollective and Harbor Motors. These merchants should be reviewed in a real reporting workflow because they are linked to higher-value or less frequent spend patterns.

## Recurring Payments

The dataset contains 7,344 recurring transactions. Recurring income was driven by salary payments, while recurring expenses were concentrated in rent, utilities, insurance, healthcare/gym payments and subscriptions.

Recurring expenses totalled 1.70M, making them a major part of the cost base. This is useful for dashboarding because recurring payments are predictable and can be separated from discretionary spending. A good business action would be to review high recurring costs and identify subscriptions or services that can be reduced.

## Unusual Transactions

There were 129 unusual transactions with a combined value of 113,484.26. These included high-value transactions, rare merchants and duplicate-looking payments. The dataset also contains 31 duplicate-looking transaction groups based on matching account, date, merchant, category and amount.

In a real finance reporting process, these items would be suitable for exception reporting. Suggested actions include adding alerts for high-value payments, reviewing duplicate-looking transactions and monitoring rare merchants that suddenly appear in high-spend categories.

## Budget Performance

Budget performance was assessed using portfolio-level monthly category benchmarks. Across month/category combinations, 90 were within budget, 38 were near budget and 28 were over budget.

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

Shopping and travel are the clearest budget control opportunities because they exceeded budget most often and are more discretionary than rent or utilities.

## Recommendations

1. Review high recurring subscription and service costs to identify payments that can be cancelled, consolidated or renegotiated.
2. Set alerts for unusual high-value transactions, especially rare merchants and payments above 1,000.
3. Investigate duplicate-looking payments using account, date, merchant, category and amount matching.
4. Monitor categories with repeated over-budget months, especially shopping, travel, groceries and healthcare.
5. Separate essential and discretionary spending in the dashboard to make business recommendations clearer.
6. Use monthly cash flow reporting to support financial planning and identify changes before they become persistent trends.

## Limitations

This dataset is synthetic and designed for portfolio demonstration rather than operational finance use. The data does not include real customers, real bank accounts, fraud outcomes, credit risk scores or external economic factors. Budget values are benchmark assumptions and should be adjusted if the analysis is reframed for a different business scenario.

## Next Steps

1. Build the Power BI dashboard using the cleaned CSV and dashboard plan.
2. Add dashboard screenshots to `dashboard/screenshots/`.
3. Extend the SQL analysis with optional customer segmentation.
4. Add more detailed anomaly rules, such as rolling category averages or merchant-level spike detection.
5. Create a short project walkthrough for GitHub or interview preparation.

