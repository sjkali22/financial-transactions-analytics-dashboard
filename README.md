# Financial Transactions Analytics Dashboard

## Short Project Summary

This Data Analyst portfolio project analyses 9,000 synthetic financial transactions across income, expenses, transfers, refunds, recurring payments and unusual activity. It demonstrates a complete analysis workflow using Python and pandas for data cleaning, PostgreSQL-compatible SQL for querying, Jupyter Notebook for exploratory analysis and Power BI planning for dashboard reporting.

Repository:

```text
https://github.com/sjkali22/financial-transactions-analytics-dashboard
```

The project is designed to be clear, realistic and easy to explain in interviews for junior data analyst, reporting analyst, BI analyst and finance data analyst roles.

## Business Problem

Finance and reporting teams need reliable transaction reporting to understand cash flow, spending patterns, recurring costs, budget performance and transactions that may require review. Raw transaction data is too detailed for decision-making on its own, so it needs to be cleaned, transformed and summarised into meaningful KPIs, analysis outputs and dashboard views.

This project answers the question:

> How can financial transaction data be transformed into business-ready insight for reporting, monitoring and decision-making?

## Project Objectives

- Generate a realistic synthetic financial transactions dataset.
- Clean and prepare transaction data using Python and pandas.
- Create analysis-ready fields for monthly trends, net cash flow, budget variance and anomaly review.
- Use SQL to answer common financial reporting questions.
- Build a Jupyter Notebook for exploratory analysis and simple visualisation.
- Prepare a Power BI dashboard plan with recommended visuals, slicers and DAX measures.
- Write a professional insights report with business recommendations.

## Tools and Skills Used

- Python
- pandas
- numpy
- matplotlib
- Jupyter Notebook
- PostgreSQL-compatible SQL
- Power BI dashboard planning
- DAX measure design
- Financial reporting
- KPI reporting
- Anomaly detection
- Business recommendations
- Git and GitHub documentation

## Dataset Overview

The dataset is synthetic and included in the repository for portfolio review.

- Raw dataset: `data/raw/transactions_raw.csv`
- Cleaned dataset: `data/cleaned/transactions_cleaned.csv`
- Rows in cleaned dataset: 9,000
- Customers: 120
- Accounts: 149
- Date range: `2025-01-01` to `2025-12-31`

The cleaned dataset includes original transaction fields and derived reporting fields such as `transaction_month`, `income_amount`, `expense_amount`, `net_amount`, `amount_abs`, `category_budget`, `budget_variance` and `budget_status`.

## Repository Structure

```text
financial-transactions-analytics-dashboard/
├── README.md
├── data/
│   ├── raw/
│   │   └── transactions_raw.csv
│   └── cleaned/
│       └── transactions_cleaned.csv
├── docs/
│   └── data_dictionary.md
├── sql/
│   └── transaction_analysis_queries.sql
├── notebooks/
│   └── transaction_analysis.ipynb
├── dashboard/
│   ├── screenshots/
│   │   └── .gitkeep
│   └── powerbi_dashboard_plan.md
├── reports/
│   └── insights.md
├── scripts/
│   ├── generate_transactions.py
│   └── clean_transactions.py
├── requirements.txt
└── .gitignore
```

## Key Analysis Questions

- What are total income, total expenses and net cash flow?
- How do income and expenses change month by month?
- Which categories and merchants drive the highest spend?
- Which transactions are recurring?
- Which transactions are unusual or worth reviewing?
- Which categories are over budget or near budget?
- Which payment methods are used most often?
- Which customers or accounts have the highest expenses?

## Key Metrics

| Metric | Value |
| --- | ---: |
| Transactions analysed | 9,000 |
| Customers | 120 |
| Accounts | 149 |
| Total income | 4.71M |
| Total expenses | 2.00M |
| Net cash flow | 2.24M |
| Average transaction value | 800.74 |
| Expense ratio | 42.36% |
| Recurring transactions | 7,344 |
| Unusual transactions | 129 |
| Duplicate-looking transaction groups | 31 |

## Dashboard Overview

The Power BI dashboard is planned as a four-page reporting pack titled **Financial Transactions Analytics Dashboard**.

> Dashboard screenshots will be added after the Power BI report has been built.

Planned pages:

1. Executive Overview
2. Spending Analysis
3. Recurring and Unusual Transactions
4. Budget Performance

The dashboard is designed to show executive KPIs, monthly cash flow, category spend, merchant spend, recurring payments, unusual transactions and budget performance. Full dashboard build guidance is available in `dashboard/powerbi_dashboard_plan.md`.

## Dashboard Screenshots

Screenshots will be added after the Power BI dashboard is built.

Expected screenshot files:

```text
dashboard/screenshots/executive_overview.png
dashboard/screenshots/spending_analysis.png
dashboard/screenshots/recurring_unusual_transactions.png
dashboard/screenshots/budget_performance.png
```

No broken image links are included yet because the screenshots have not been exported.

## Example Insights

- Rent was the largest expense category at 1.35M, making fixed housing costs the main cost driver.
- Utilities were the second largest expense group at 208,573.33, driven by PowerGrid, WaterWorks and MobileConnect.
- Shopping and travel had the most frequent over-budget months, making them strong candidates for monitoring.
- 129 unusual transactions were flagged, with a combined value of 113,484.26.
- 31 duplicate-looking transaction groups were identified using account, date, merchant, category and amount matching.
- Net cash flow stayed positive in every month of 2025.

More detail is available in `reports/insights.md`.

## How to Run the Project Locally

Clone the existing GitHub repository and run the project locally:

```bash
git clone https://github.com/sjkali22/financial-transactions-analytics-dashboard.git
cd financial-transactions-analytics-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_transactions.py
python scripts/clean_transactions.py
jupyter notebook
```

Then open:

```text
notebooks/transaction_analysis.ipynb
```

The notebook loads the cleaned CSV and includes data quality checks, KPI calculations, monthly cash flow analysis, category analysis, merchant analysis, recurring payment analysis, unusual transaction analysis, payment method analysis and budget performance analysis.

## SQL Analysis

The SQL file is:

```text
sql/transaction_analysis_queries.sql
```

It includes PostgreSQL-compatible queries for:

- Table creation
- Data load notes
- Row count and date range checks
- Total income, expenses and net cash flow
- Monthly cash flow trends
- Category and merchant spending
- Recurring payment analysis
- Unusual transaction analysis
- Payment method breakdown
- Budget performance
- Duplicate-looking transactions
- Large transactions above a threshold
- Dashboard KPI summary

Example PostgreSQL load command:

```sql
\copy transactions FROM 'data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true);
```

If PostgreSQL is running from another directory, use the full local path to the cleaned CSV.

## Data Dictionary

[View the data dictionary](docs/data_dictionary.md)

## Skills Demonstrated

- Python data cleaning
- Transaction data analysis
- SQL querying
- Financial reporting
- Power BI dashboard planning
- KPI reporting
- Budget variance analysis
- Anomaly detection
- Business insight writing
- Clear project documentation

## CV Bullet Points

- Built a financial transactions analytics dashboard using Python, SQL and Power BI to analyse 9,000 synthetic banking transactions across income, expenses, recurring payments and unusual activity.
- Cleaned and transformed transaction data with Python/Pandas, creating analysis-ready fields for monthly trends, category spend, net cash flow, budget variance and anomaly detection.
- Developed SQL queries and dashboard-ready KPIs to support financial reporting, spending analysis and business recommendations.

## GitHub Topics

Suggested repository topics:

```text
data-analysis
python
pandas
sql
postgresql
power-bi
financial-analysis
dashboard
business-intelligence
portfolio-project
```

## Future Improvements

- Add completed Power BI dashboard screenshots to the README.
- Add customer segmentation by spending behaviour.
- Add rolling-average anomaly detection.
- Add a short project walkthrough for interview preparation.
- Add optional PostgreSQL setup instructions for users who want to run the SQL locally.
- Add simple tests for the Python cleaning workflow.

