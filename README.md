# Financial Transactions Analytics Dashboard

## Overview

This portfolio project turns 9,000 synthetic financial transactions into a reproducible analytics workflow and a two-page Power BI report. It demonstrates data generation, data quality controls, Python transformation, PostgreSQL-compatible analysis, KPI reconciliation, dashboard design, and business communication without using real personal financial data.

The analysis separates operating performance from cash movement: **operating surplus** is income less expenses, while **net cash flow** also includes signed refunds and transfers. That distinction prevents materially different measures from being presented as though they were interchangeable.

## Business Problem

Transaction-level data is too detailed for quick financial oversight. A useful reporting solution must answer:

- How much income and expense activity occurred?
- How do signed transfers and refunds affect cash movement?
- Which categories drive spending?
- How much expense is recurring?
- Where is actual spend below, near, or above budget?
- Which transactions merit review because they are unusually large or duplicated-looking?

## Project Objectives

1. Generate a realistic, deterministic synthetic dataset with no personal data.
2. Validate and transform raw transactions into an analysis-ready model.
3. Define financial KPIs consistently across Python, SQL, and Power BI.
4. Analyse trends, categories, recurring expenses, budgets, and review flags.
5. Present the results in a concise two-page Power BI report.
6. Make the workflow reproducible with tests and continuous integration.

## Dashboard Preview

The Power BI artifact is available at [`dashboard/financial_transactions_dashboard.pbix`](dashboard/financial_transactions_dashboard.pbix). Genuine page screenshots have not yet been exported, so no placeholder or mock dashboard images are shown here.

The intended v1.0 scope is:

- **Executive Overview** — headline KPIs, monthly income and expense trends, category mix, and filters.
- **Spending Analysis** — expense categories, recurring expenses, budget performance, and transaction detail.

See the [Power BI validation guide](dashboard/powerbi_dashboard_plan.md) for the reconciled DAX measures and the remaining desktop checks.

## Key Findings

| Metric | Verified result |
| --- | ---: |
| Transactions | 9,000 |
| Total income | £4,710,640.23 |
| Total expenses | £1,995,612.11 |
| Operating surplus | £2,715,028.12 |
| Net cash flow | £2,240,530.83 |
| Average transaction value | £800.74 |
| Recurring expenses | £1,704,954.66 |
| Budget utilisation | 100.73% |

- Net cash flow is £474,497.29 below operating surplus. Refunds contributed £4,517.54, while transfers had a net cash effect of −£479,014.83.
- Rent was the largest expense category at £1,347,716.36, followed by utilities at £208,573.33.
- Monthly expenses ranged from £160,855.50 in January to £171,381.70 in July.
- At month/category grain, 66 of 132 budgeted periods exceeded budget, 33 were near the limit, and 33 were below budget.
- Rule-based checks flagged 129 unusual transactions worth £113,484.26 and 31 duplicate-looking groups. These are review indicators, not confirmed fraud or data errors.

## Tools and Technologies

| Tool | Role |
| --- | --- |
| Python 3.12 | Synthetic data generation, validation, and automation |
| pandas / NumPy | Cleaning, derived fields, KPI calculation, and analysis |
| PostgreSQL-compatible SQL | Reusable analytical queries and dashboard KPI logic |
| Jupyter Notebook | Executable exploratory analysis and visual summaries |
| Power BI / DAX | Two-page interactive reporting artifact |
| pytest / GitHub Actions | Regression tests and automated data validation |

## Data Source

The dataset is entirely **synthetic**. It represents 9,000 transactions across 120 fictional customers and 149 fictional accounts from 1 January to 31 December 2025. It contains income, expenses, refunds, and incoming or outgoing transfers.

The simulation is useful for demonstrating analytical methods, but it does not represent a real organisation, actual customers, verified fraud, or commercial impact. Budget values and unusual-transaction flags are modelling assumptions.

## Data Preparation

[`scripts/generate_transactions.py`](scripts/generate_transactions.py) uses a fixed seed to create deterministic transaction patterns, including recurring salary, rent, utilities, subscriptions, insurance, savings transfers, refunds, and unusual high-value activity.

[`scripts/clean_transactions.py`](scripts/clean_transactions.py):

- validates the required raw schema;
- reports exact duplicate, duplicate-ID, invalid-value, zero-value, and invalid-type rejection counts;
- standardises identifiers, text, dates, numbers, and booleans;
- creates signed, absolute, income, expense, and monthly reporting fields;
- aggregates category spend at month/category grain; and
- classifies budget use as **Below Budget** (<90%), **Near Limit** (90%–100%), or **Exceeded Budget** (>100%).

The current source data produces 9,000 cleaned rows with no removals, missing values, or duplicate transaction IDs.

## Exploratory and SQL Analysis

The [analysis notebook](notebooks/transaction_analysis.ipynb) covers data quality, headline KPIs, monthly trends, category and merchant spend, recurring expenses, unusual transactions, payment methods, and budget performance.

[`sql/transaction_analysis_queries.sql`](sql/transaction_analysis_queries.sql) provides PostgreSQL-compatible queries for the same subjects. SQL definitions follow the cleaned schema and deduplicate repeated budgets at month/category grain. A PostgreSQL parser accepted both schema statements and all 19 analysis statements. No PostgreSQL service was available during the v1.0 verification run, so SQL results were not represented as database-executed; core KPI logic was independently reconciled with Python's `csv` and `Decimal` modules instead.

## KPI Definitions

| KPI | Definition |
| --- | --- |
| Total Income | Sum of positive `income_amount` for `Income` transactions |
| Total Expenses | Sum of positive `expense_amount` for `Expense` transactions |
| Operating Surplus | Total Income − Total Expenses |
| Net Cash Flow | Sum of signed `net_amount`, including refunds and transfers |
| Average Transaction Value | Average `amount_abs` across all transactions |
| Recurring Expenses | Expense amount where `is_recurring = True` and type is `Expense` |
| Budget Utilisation | Actual expense ÷ budget, aggregated once per month/category |
| Budget Variance | Budget − actual expense, aggregated once per month/category |

## Project Structure

```text
.
├── .github/workflows/ci.yml
├── dashboard/
│   ├── financial_transactions_dashboard.pbix
│   ├── powerbi_dashboard_plan.md
│   └── screenshots/.gitkeep
├── data/
│   ├── raw/transactions_raw.csv
│   └── cleaned/transactions_cleaned.csv
├── docs/data_dictionary.md
├── notebooks/transaction_analysis.ipynb
├── reports/insights.md
├── scripts/
│   ├── clean_transactions.py
│   ├── generate_transactions.py
│   └── validate_data.py
├── sql/
│   ├── create_transactions_table.sql
│   └── transaction_analysis_queries.sql
├── tests/test_pipeline.py
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run

From the repository root on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\generate_transactions.py
python scripts\clean_transactions.py
python scripts\validate_data.py
python -m pytest -q
jupyter nbconvert --execute --to notebook --inplace notebooks\transaction_analysis.ipynb
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` and use forward slashes in paths.

To run the SQL in a dedicated PostgreSQL database:

```text
psql -d financial_transactions -f sql/create_transactions_table.sql
```

Then, from an interactive `psql` session started at the repository root, load the CSV:

```sql
\copy transactions FROM 'data/cleaned/transactions_cleaned.csv' WITH (FORMAT csv, HEADER true)
```

Run the analytical queries:

```text
psql -d financial_transactions -f sql/transaction_analysis_queries.sql
```

Use a dedicated database because the setup script replaces a table named `transactions`.

Open `dashboard/financial_transactions_dashboard.pbix` in Power BI Desktop and refresh it from `data/cleaned/transactions_cleaned.csv`. Complete the checklist in `dashboard/powerbi_dashboard_plan.md` before relying on the dashboard totals.

## Results and Recommendations

- Separate operating surplus from net cash flow in every report so transfer activity cannot obscure expense performance.
- Track recurring expenses independently; they account for £1,704,954.66 of the annual expense base and represent committed cost.
- Review rent and utilities first because together they dominate expense value, while more discretionary categories are better candidates for behavioural budget controls.
- Investigate the 129 unusual rows and 31 duplicate-looking groups with supporting context before taking action.
- Use month/category budget grain for reporting; summing row-level repeated budget fields would overstate the available budget.

## Limitations

- The data is synthetic and cannot support claims about real customers, fraud, savings, or business outcomes.
- Budget thresholds are portfolio assumptions rather than approved organisational targets.
- Unusual flags are generated rules, not a trained anomaly or fraud model.
- SQL logic still requires execution against PostgreSQL for database-engine verification.
- The PBIX layout still references an ambiguous `Recurring Payment Total` measure; it must be replaced with the documented `Recurring Expenses` measure, and the rendered report, relationships, formats, interactions, and screenshots require Power BI Desktop validation.

## Future Enhancements

- Add genuine screenshots after the desktop report is validated.
- Execute and snapshot SQL reconciliation results in a dedicated PostgreSQL environment.
- Introduce an explicit essential/discretionary category mapping.
- Replace rule-generated anomaly labels with explainable statistical thresholds for demonstration.
