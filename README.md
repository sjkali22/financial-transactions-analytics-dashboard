# Financial Transactions Analytics Dashboard — Two-Page Interview Summary

## Project Overview

For this project, I created a **Financial Transactions Analytics Dashboard** as part of my Data Analyst portfolio. The aim was to demonstrate a complete data analysis workflow using realistic transaction-style data. The project analyses income, expenses, transfers, refunds, recurring payments, unusual transactions, category spending, merchant spending and budget performance.

The project uses a synthetic dataset of **9,000 financial transactions**. I chose synthetic data because real financial transaction data is sensitive, so creating realistic artificial data allowed me to practise the full data analysis process without using private customer information.

The project was designed to be relevant to data analyst apprenticeship, junior data analyst, reporting analyst, BI analyst and finance data analyst roles. It shows that I can take raw data, clean and prepare it, analyse it using Python and SQL, build dashboard-ready KPIs, create a Power BI report and communicate useful business insights.

Repository:

https://github.com/sjkali22/financial-transactions-analytics-dashboard

---

## Business Problem

Finance and reporting teams often work with large transaction datasets. These datasets contain useful information, but the raw data is too detailed to support decision-making on its own. It needs to be cleaned, transformed and summarised into key metrics, trends and dashboard views.

This project answers the question:

**How can financial transaction data be transformed into business-ready insight for reporting, monitoring and decision-making?**

The same type of analysis could be applied in a real organisation to monitor financial activity, operational costs, supplier payments, customer billing, recurring costs, unusual transactions or budget performance.

For Anglian Water, the same workflow could be transferred to areas such as billing data, customer service data, operational cost reporting, supplier spend, asset data or performance dashboards.

---

## Tools and Skills Used

The main tools used in this project were:

| Tool             | Purpose                                   |
| ---------------- | ----------------------------------------- |
| Python           | Data generation and data cleaning         |
| pandas           | Data transformation and analysis          |
| Jupyter Notebook | Exploratory analysis and documentation    |
| SQL/PostgreSQL   | Querying and reporting logic              |
| Power BI         | Dashboard creation and KPI reporting      |
| GitHub           | Version control and project documentation |

The project demonstrates skills in:

* Data cleaning
* Transaction data analysis
* SQL querying
* Power BI dashboarding
* DAX measure creation
* KPI reporting
* Financial reporting
* Trend analysis
* Anomaly detection
* Business recommendations
* Project documentation

---

## Dataset Summary

The dataset contains **9,000 synthetic transaction records** across **120 customers** and **149 accounts**. The data covers the full year from **1 January 2025 to 31 December 2025**.

The dataset includes fields such as:

* Transaction ID
* Transaction date
* Account ID
* Customer ID
* Transaction type
* Category
* Merchant
* Amount
* Payment method
* Location
* Recurring transaction flag
* Unusual transaction flag
* Balance after transaction

The transaction types include income, expenses, transfers and refunds. The categories include salary, rent, groceries, utilities, transport, dining, entertainment, shopping, insurance, healthcare, travel and subscriptions.

I also created derived fields to make reporting easier, including:

* Transaction month
* Income amount
* Expense amount
* Net amount
* Absolute transaction amount
* Category budget
* Budget variance
* Budget status

These fields helped make the dataset easier to use in Power BI and SQL analysis.

---

## Project Process

The project followed a full data analyst workflow.

First, I planned the project by deciding the business problem, analysis questions, dataset structure, key metrics and final dashboard pages. The main questions included:

* What are total income, total expenses and net cash flow?
* Which categories and merchants drive the highest spend?
* How do income and expenses change month by month?
* Which transactions are recurring?
* Which transactions are unusual or worth reviewing?
* Which areas are over budget?

Next, I created the raw synthetic dataset using Python. The script generated transaction records with realistic patterns, including income, expenses, recurring payments, different merchants, different categories and unusual transactions.

After that, I cleaned and prepared the dataset using Python and pandas. This included formatting dates, validating numeric fields, checking duplicates, standardising fields and creating derived columns for reporting.

I then created a Jupyter Notebook to explore the cleaned dataset. The notebook includes data quality checks, KPI calculations, monthly trend analysis, category analysis, merchant analysis, recurring payment analysis, unusual transaction analysis and budget performance analysis.

I also wrote SQL queries in a PostgreSQL-compatible SQL file. The SQL includes queries for total income, total expenses, net cash flow, monthly trends, category spend, top merchants, recurring payments, unusual transactions, payment method breakdown and budget performance.

Finally, I built Power BI dashboard pages to present the key findings visually.

---

## Power BI Dashboard

The dashboard is called:

**Financial Transactions Analytics Dashboard**

The completed dashboard pages are:

1. **Executive Overview**
2. **Spending Analysis**

The Executive Overview page gives a high-level summary of financial performance. It includes:

* Total Income KPI
* Total Expenses KPI
* Net Cash Flow KPI
* Transaction Count KPI
* Monthly Income vs Expenses chart
* Expenses by Category chart
* Transactions by Payment Method chart
* Slicers for category, payment method, transaction date and transaction type

The Spending Analysis page focuses more closely on expenses. It includes:

* Total Expenses KPI
* Transaction Count KPI
* Average Transaction Amount KPI
* Recurring Payment Total KPI
* Expenses by Category chart
* Top Merchants by Spend chart
* Monthly Spending Trend chart
* Expense Transaction Details table
* Slicers for transaction date, merchant, payment method and category

The dashboard helps users move from a summary view to a more detailed spending view. The first page answers “what is happening overall?”, while the second page answers “where is spending going?”

---

## Key Metrics

The main results from the analysis were:

| Metric                               |  Value |
| ------------------------------------ | -----: |
| Transactions analysed                |  9,000 |
| Customers                            |    120 |
| Accounts                             |    149 |
| Total income                         |  4.71M |
| Total expenses                       |  2.00M |
| Net cash flow                        |  2.24M |
| Average transaction value            | 800.74 |
| Expense ratio                        | 42.36% |
| Recurring transactions               |  7,344 |
| Unusual transactions                 |    129 |
| Duplicate-looking transaction groups |     31 |

---

## Key Insights

The analysis showed that income was higher than expenses overall, with positive net cash flow across the year.

Rent was the largest expense category at approximately **1.35M**, making it the main cost driver. Utilities were the second largest expense group at around **208,573.33**, driven by merchants such as PowerGrid, WaterWorks and MobileConnect.

The project also flagged **129 unusual transactions**, with a combined value of **113,484.26**. These transactions would be useful for further review because they may represent unusually high spending, rare transaction behaviour or possible data quality issues.

The analysis also identified **31 duplicate-looking transaction groups**, using matching logic based on account, date, merchant, category and amount.

The dashboard shows that recurring payments make up a large part of overall expense activity. This is useful because recurring payments represent committed costs that are important for budgeting and financial planning.

---

## Recommendations

Based on the analysis, the main recommendations are:

* Review high recurring payment categories to understand committed monthly costs.
* Monitor categories that regularly exceed budget.
* Investigate unusual high-value transactions.
* Review top merchants by spend to identify cost concentration.
* Use monthly cash flow reporting to support better financial planning.
* Separate essential and discretionary spending for clearer decision-making.

The main purpose of the project was not just to build charts, but to show how data can be cleaned, analysed and turned into business recommendations.

---

## What I Learned

This project helped me practise a full data analyst workflow from start to finish. I improved my ability to structure a project, clean data using Python, create reporting fields, write SQL queries, build Power BI visuals and explain insights clearly.

I also learned that dashboard design is not just about adding visuals. It is about choosing the right KPIs, making the layout readable, using filters effectively and helping the user understand what action to take from the data.

---

## Future Improvements

If I had more time, I would improve the project by completing the additional dashboard pages for recurring and unusual transactions and budget performance. I would also add more advanced anomaly detection, create a proper date table in Power BI, connect the dashboard directly to PostgreSQL and add more drill-through functionality.

---

## One-Minute Explanation

I built a Financial Transactions Analytics Dashboard to practise a complete data analyst workflow. I generated a synthetic dataset of 9,000 transactions, cleaned it using Python and pandas, created analysis-ready fields, wrote SQL queries and built Power BI dashboard pages to report on income, expenses, net cash flow, category spending, merchant spending, recurring payments and unusual activity. I also documented the project on GitHub with a README, data dictionary, SQL file, notebook and insights report. The project shows that I can take raw data, prepare it, analyse it and communicate useful business insights through dashboards and written recommendations.
