# Sales dashboard design

## Purpose and scope

Build the PRD's Phase 1 Streamlit dashboard so ShopSmart's managers can read
overall sales performance, monthly trends, and category/region comparisons.
Use the supplied historical CSV; this release does not provide live updates.
Success means correct totals and charts, readable presentation, tested data
calculations, and a publicly accessible Streamlit Community Cloud deployment.

The student chose monthly totals to keep the trend readable and aligned with
the high-level KPIs. Missing or invalid CSV data must produce a clear error
and stop the dashboard; no records are silently skipped.

Out of scope: filters, date selectors, authentication, databases, exports,
alerts, drill-down, and custom mobile layouts, as specified by the PRD.

## Approach and files

Use two application modules: `app.py` for presentation and `sales_data.py`
for loading, validation, and calculations. This keeps calculations testable
without launching Streamlit and avoids the complexity of a larger package.
The alternatives considered were a single file (less separation for testing)
and a larger package (unnecessary structure for this small dashboard).

- `app.py`: page title, error display, KPI cards, and Plotly charts.
- `sales_data.py`: validated CSV loader and small aggregation functions.
- `tests/test_sales_data.py`: pytest tests using small, known datasets and temporary CSVs.
- `requirements.txt`: Streamlit, pandas, Plotly, and pytest dependencies.
- `venv/`: plain Python virtual environment, excluded from Git.
- `AGENTS.md`: project memory and genuine Lessons, created after implementation.
- `README.md`: preserve tutorial content and add project run instructions and eventually the live URL.

Stay on `feature/sales-dashboard` in the existing clone. Do not create a
worktree, use uv or conda, or add another application framework.

## Data contract and error handling

Resolve `data/sales-data.csv` relative to the application files. Read it with
pandas and validate all eight PRD columns: `date`, `order_id`, `product`,
`category`, `region`, `quantity`, `unit_price`, and `total_amount`.

- Require a readable, well-formed, nonempty CSV and all required columns.
- Require valid calendar dates in the supplied ISO date format.
- Require finite numeric quantity, unit price, and total amount values;
  quantity must be integral. Do not invent restrictions on negative values
  or recompute revenue: the PRD defines `total_amount` as the sales source.
- Require nonblank order IDs, products, categories, and regions.
- Preserve order IDs and categorical values as strings; parse dates and numbers.
- Extra columns may be ignored. Do not restrict categories/regions to a hardcoded list.

The loader raises an informative validation error naming the problem.
`app.py` catches expected file/validation errors, displays a concise message
using Streamlit, and stops before drawing KPIs or charts. It never replaces
bad data with sample data or silently drops invalid rows.

## Calculations

- Total Sales: sum `total_amount`; display dollars with grouping and two decimals.
- Total Orders: count transaction rows, not quantities or distinct order IDs.
- Monthly sales: group by calendar year and month, sum `total_amount`, and
  sort chronologically. Use a date-valued month key so years cannot be mixed.
  Display months present in the data; do not invent missing-month observations.
- Category and region sales: sum `total_amount` per group, include every group,
  and sort descending by sales. Use alphabetical order to break ties consistently.
- Keep numeric totals unrounded during aggregation; format at presentation.

Read-only inspection of the supplied CSV found 482 transactions totaling
$116,500.21, dated January 3 through December 31, 2024, with five categories
and four regions. Calculate results from the file rather than hardcoding them.

## Dashboard presentation

Use a wide Streamlit page titled **ShopSmart Sales Dashboard**. Place Total
Sales and Total Orders side by side at the top, a full-width monthly trend
line chart below, and two horizontal bar charts side by side at the bottom.
Bars run from the highest-sales group at the top to the lowest at the bottom.

Use standard Streamlit components and a restrained, consistent chart color.
Label the trend axes Month and Sales ($); label bar charts Sales by Category
and Sales by Region, with sales amounts in dollars. Tooltips show the month
or group name and its sales amount to two decimal places. Include a short
caption identifying the historical CSV and its date range. No custom CSS,
extra controls, or decorative features are needed.

## Verification

Use test-first development for the loader, validation, and aggregation
functions. Small fixtures must verify exact expected behavior, including
missing files/columns, empty or invalid records, transaction count versus
quantity, totals, cross-year monthly grouping, chronological sorting, and
descending group sorting. Use appropriate numeric tolerances for floating
point comparisons and cross-check the supplied CSV totals independently.

Inspect the running dashboard for all required visuals, correct formatting,
chart order, hover values, and absence of errors/warnings. Verify the clear
error state using a temporary test fixture without damaging the tracked CSV.
Record local load/render observations against the PRD's five-second page
load and two-second chart-render targets; do not claim unmeasured performance
or browser coverage. Cloud cold starts may differ from local timings.

## Milestone mapping and delivery order

| Milestone | Design coverage |
| --- | --- |
| TASK-1 | Virtual environment, dependencies, basic app, CSV loader and validation tests |
| TASK-2 | Tested sales/order calculations and KPI cards |
| TASK-3 | Tested monthly aggregation and trend chart |
| TASK-4 | Tested grouped totals and sorted category/region bar charts |
| TASK-5 | Full validation, documentation, project memory, branch review and merge |
| TASK-6 | Student deployment from main and final URL/bookkeeping updates |

Commit this design before the implementation plan, and commit the reviewed
plan before product code. Execute the plan inline with milestone IDs on
implementation commits. Update `TASKS.md` as each milestone progresses;
record actual completion hashes and honest Notes, never fabricated lessons.

After implementation, create project memory using the Codex `/init`
equivalent with a Lessons section. Push the feature branch, review against
`main` using Codex `/review`, let the student decide on findings, and commit
applicable fixes. Merge with `--no-ff` and push `main` before deployment.

Deployment is the final plan step and is executed by the student in Streamlit
Community Cloud using `main` and `app.py`. After the student supplies the live
URL and the app is verified, record it in TASKS.md and near the top of README.md,
complete deployment bookkeeping, and commit/push those updates to main.

## Review status

The student approved the conversational design. This written specification
is now ready for the tutorial's written-spec review before writing-plans.
