# Financial Transactions Analytics Dashboard

## Project Summary

This is a complete Data Analyst portfolio project that analyses 9,000 synthetic financial transactions across income, expenses, transfers, refunds, recurring payments and unusual activity. The project uses Python for data generation and cleaning, SQL for analysis queries, Jupyter Notebook for exploratory analysis and a Power BI plan for dashboard development.

The project is designed to be clear, realistic and easy to explain in interviews for Data Analyst Apprentice, Junior Data Analyst, Finance Data Analyst, Reporting Analyst, Business Intelligence Analyst and Data Technician roles.

## Business Problem

Finance teams need reliable reporting to understand cash flow, category spend, recurring costs, unusual transactions and budget performance. Raw transaction data is often too detailed for decision-making, so it must be cleaned, transformed and summarised into KPIs, SQL outputs and dashboards.

This project answers a practical reporting question:

> How can transaction data be transformed into business-ready insight for financial monitoring and decision-making?

## Project Objectives

- Generate a realistic synthetic financial transactions dataset.
- Clean and prepare transaction data using Python and pandas.
- Create analysis-ready fields for cash flow, monthly trends, budget status and anomaly review.
- Analyse the data with PostgreSQL-compatible SQL queries.
- Build a Jupyter Notebook for exploratory analysis and simple visualisation.
- Prepare a Power BI dashboard plan with recommended visuals and DAX measures.
- Write a business-style insights report with recommendations.

## Tools Used

- Python
- pandas
- numpy
- matplotlib
- Jupyter Notebook
- PostgreSQL SQL
- Power BI
- VS Code
- Git and GitHub

## Dataset Description

The dataset is synthetic and saved in two versions:

- Raw dataset: `data/raw/transactions_raw.csv`
- Cleaned dataset: `data/cleaned/transactions_cleaned.csv`

The cleaned dataset contains 9,000 transactions across 120 customers and 149 accounts from 2025-01-01 to 2025-12-31.

Main fields include:

- `transaction_id`
- `transaction_date`
- `account_id`
- `customer_id`
- `transaction_type`
- `category`
- `merchant`
- `amount`
- `payment_method`
- `location`
- `is_recurring`
- `is_unusual`
- `balance_after_transaction`

Derived analysis fields include:

- `transaction_month`
- `transaction_year`
- `month_name`
- `income_amount`
- `expense_amount`
- `net_amount`
- `amount_abs`
- `category_budget`
- `category_month_expense`
- `budget_variance`
- `budget_variance_pct`
- `budget_status`

## Folder Structure

```text
financial-transactions-analytics-dashboard/
├── README.md
├── data/
│   ├── raw/
│   │   └── transactions_raw.csv
│   └── cleaned/
│       └── transactions_cleaned.csv
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

- What are the total income, total expenses and net cash flow?
- How do income and expenses change month by month?
- Which spending categories and merchants drive the most cost?
- Which transactions are recurring?
- Which transactions look unusual or require review?
- Which categories are over budget?
- Which payment methods are used most often?
- Which customers or accounts have the highest expenses?

## Key Metrics

| Metric | Value |
| --- | ---: |
| Transactions | 9,000 |
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

The Power BI dashboard is planned as four report pages:

1. **Executive Overview**
   - Total Income KPI
   - Total Expenses KPI
   - Net Cash Flow KPI
   - Transaction Count KPI
   - Monthly income vs expenses visual
   - Category and payment method breakdowns

2. **Spending Analysis**
   - Spending by category
   - Top merchants
   - Monthly spending trend
   - High-spend categories
   - Slicers for date, category, customer, transaction type and payment method

3. **Recurring and Unusual Transactions**
   - Recurring payments table
   - Unusual transactions table
   - Unusual transaction KPIs
   - Spend spike analysis
   - Large transaction visual

4. **Budget Performance**
   - Budget vs actual by category
   - Over-budget categories
   - Budget status breakdown
   - Recommendations section

Full build instructions are in `dashboard/powerbi_dashboard_plan.md`.

## Example Insights

- Rent was the largest expense category at 1.35M, making fixed housing costs the biggest cost driver.
- Utilities were the second largest expense group at 208,573.33, driven by PowerGrid, WaterWorks and MobileConnect.
- Shopping and travel were the most frequent over-budget categories, suggesting they should be monitored closely.
- 129 unusual transactions were flagged, with a combined value of 113,484.26.
- 31 duplicate-looking transaction groups were found using account, date, merchant, category and amount matching.
- Net cash flow stayed positive in every month of 2025.

More detail is available in `reports/insights.md`.

## How to Run the Project Locally

From VS Code, open a terminal in the project folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate the Dataset

```bash
python scripts/generate_transactions.py
```

This creates:

```text
data/raw/transactions_raw.csv
```

## Clean the Dataset

```bash
python scripts/clean_transactions.py
```

This creates:

```text
data/cleaned/transactions_cleaned.csv
```

## Run the Notebook

```bash
jupyter notebook
```

Then open:

```text
notebooks/transaction_analysis.ipynb
```

The notebook loads the cleaned CSV and includes data quality checks, summary statistics, monthly cash flow analysis, category spend, merchant spend, recurring payments, unusual transactions, payment method analysis and budget performance.

## Use the SQL File

The SQL file is:

```text
sql/transaction_analysis_queries.sql
```

It includes:

- A PostgreSQL `CREATE TABLE` statement
- Data load notes
- Row count and date range checks
- Income, expense and net cash flow queries
- Monthly trend queries
- Category and merchant spend queries
- Recurring and unusual transaction queries
- Budget performance queries
- Duplicate-looking transaction checks
- Dashboard KPI summary query

Example PostgreSQL load command:

```sql
\copy transactions FROM 'data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true);
```

If PostgreSQL is running from another directory, use the full file path to the cleaned CSV.

## Power BI Dashboard Screenshots

After building the dashboard in Power BI, save screenshots to:

```text
dashboard/screenshots/executive_overview.png
dashboard/screenshots/spending_analysis.png
dashboard/screenshots/recurring_unusual_transactions.png
dashboard/screenshots/budget_performance.png
```

Once screenshots are added, update this README with the dashboard images and one short explanation under each image.

## Skills Demonstrated

- Synthetic data generation
- Data cleaning with Python and pandas
- Feature engineering for analysis
- Financial transaction analysis
- SQL querying and KPI preparation
- Exploratory data analysis
- Dashboard planning
- DAX measure design
- Business insight writing
- GitHub project documentation

## CV Bullet Points

- Built a financial transactions analytics dashboard using Python, SQL and Power BI to analyse 9,000 synthetic banking transactions across income, expenses, recurring payments and unusual activity.
- Cleaned and transformed transaction data with Python and pandas, creating analysis-ready fields for monthly trends, category spend, net cash flow, budget variance and anomaly detection.
- Developed SQL queries and dashboard-ready KPIs to support financial reporting, spending analysis, budget monitoring and business recommendations.

## Git Setup

Run these commands when you are ready to create your first commit:

```bash
git init
git add .
git commit -m "Initial financial transactions analytics project"
```

## Future Improvements

- Add customer segmentation by spending behaviour.
- Add rolling-average anomaly detection.
- Add a formal data dictionary.
- Create Power BI dashboard screenshots and add them to the README.
- Add optional PostgreSQL setup instructions using Docker.
- Add unit tests for the Python cleaning script.
- Build a short project walkthrough for interview preparation.

