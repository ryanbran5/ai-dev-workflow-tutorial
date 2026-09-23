# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task inline. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify the PRD's sales dashboard, then guide the student through deploying the reviewed main branch.

**Architecture:** `sales_data.py` validates the CSV and computes aggregates. `app.py` presents those results with Streamlit and Plotly. Pytest exercises the data functions independently of the UI.

**Tech Stack:** Python 3.11+, plain venv, pandas, Streamlit, Plotly, pytest.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md` (student approved in conversation).

## Global Constraints

- Stay on `feature/sales-dashboard` in the existing clone. Do not create a worktree, use uv or conda, or add another application framework.
- Missing or invalid CSV data must produce a clear error and stop the dashboard; no records are silently skipped.
- Monthly sales: group by calendar year and month, sum `total_amount`, and sort chronologically.
- Total Orders: count transaction rows, not quantities or distinct order IDs.
- Keep numeric totals unrounded during aggregation; format at presentation.
- Use standard Streamlit components and a restrained, consistent chart color.
- No custom CSS, extra controls, or decorative features are needed.
- Deployment is the final plan step and is executed by the student in Streamlit Community Cloud using `main` and `app.py`.
- No product code before written-plan review. Execute inline after the student reviews this plan.

## Review Focus

1. Text identifiers such as `001` and `NA` must remain strings, not turn into numbers or nulls (Task 1 tests).
2. Nonfinite numbers, whitespace-only labels, impossible dates, and fractional quantities must stop loading (Task 1 tests).
3. January records from different years must not merge; input order must not affect chronological output (Task 3 test).
4. Equal-sales groups must have deterministic ordering, and unfamiliar groups must remain visible (Task 4 test).
5. The UI must stop before showing partial metrics/charts when loading fails, and paths must work outside the repository's working directory (Task 5 tests).

## File map

| File | Responsibility |
| --- | --- |
| `sales_data.py` | CSV loading, validation, totals, monthly and group aggregates |
| `app.py` | Streamlit layout, error state, Plotly rendering |
| `tests/test_sales_data.py` | Loader and calculation tests |
| `tests/test_app.py` | UI error and integration smoke checks |
| `requirements.txt` | Only streamlit, pandas, plotly, pytest; pin tested versions during setup |
| `TASKS.md` | Milestone state, completion commits, honest Notes |
| `AGENTS.md` | Project memory and Lessons after implementation |
| `README.md` | Run instructions and final live URL; preserve tutorial content |

## Execution and bookkeeping

Plan task numbers below are separate from milestone IDs. Tasks 1–6 each own one milestone.
Before each task, move that milestone into In Progress. For data functions, write tests,
run them and observe failure, implement, then rerun. Let the student read a short test
and explain what it checks at the tutorial's learning checkpoint. UI rendering is
verified with smoke/browser checks, not redundant tests mirroring chart implementation.

After each implementation milestone's checks pass, commit with its TASK ID. Record
that hash in TASKS.md, check criteria that were actually verified, move it to Done,
and make a second board commit with the same TASK ID. This avoids a self-referencing
commit hash. Push after TASK-1 and subsequent milestones as the tutorial requires.
Do not mark TASK-5 Done until review and merge are complete. Keep TASK-6 pending until
the student deploys and the public page is verified. Record plan progress in checkboxes
and the executing-plans ledger; never fabricate Notes or review findings.

### Task 1: Validated loading and basic application [TASK-1]

**Files:** Create `requirements.txt`, `sales_data.py`, `app.py`, `tests/test_sales_data.py`; update `TASKS.md`.

**Interfaces:**
- Consumes: the eight-column CSV at `data/sales-data.csv`.
- Produces: `load_sales(path: str | Path) -> pd.DataFrame`; `ValueError` describes expected loading/validation failures. Parsed date/numeric columns, string identifiers/categories.
- Produces: `app.py` with module-relative `DATA_PATH` and a titled, runnable app.

- [ ] Create environment and install four dependencies:

```bash
python3 -m venv venv
venv/bin/python -m pip install streamlit pandas plotly pytest
```

Expected: successful installation into `venv/`. Record installed versions of these four
packages in requirements.txt, one `name==version` per line; do not freeze unrelated packages.
The existing `.gitignore` already excludes venv and pytest caches.

- [ ] Write loader tests before `sales_data.py` exists:

```python
from pathlib import Path
import pandas as pd
import pytest
from sales_data import load_sales

BASE = dict(date='2024-01-03', order_id='001', product='NA',
            category='Audio', region='North', quantity='2',
            unit_price='5.25', total_amount='10.50')


def csv_file(tmp_path, rows):
    path = tmp_path / 'sales.csv'
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_load_preserves_text_and_parses_types(tmp_path):
    df = load_sales(csv_file(tmp_path, [BASE]))
    assert df.loc[0, 'order_id'] == '001'
    assert df.loc[0, 'product'] == 'NA'
    assert df.loc[0, 'date'] == pd.Timestamp('2024-01-03')
    assert df.loc[0, 'total_amount'] == 10.5
    assert df.loc[0, 'quantity'] == 2


def test_missing_file(tmp_path):
    with pytest.raises(ValueError, match='read'):
        load_sales(tmp_path / 'missing.csv')


def test_missing_column(tmp_path):
    row = {k: v for k, v in BASE.items() if k != 'region'}
    with pytest.raises(ValueError, match='region'):
        load_sales(csv_file(tmp_path, [row]))


@pytest.mark.parametrize('text', ['', ','.join(BASE) + '\n'])
def test_empty_file(tmp_path, text):
    path = tmp_path / 'empty.csv'
    path.write_text(text)
    with pytest.raises(ValueError):
        load_sales(path)


@pytest.mark.parametrize('column,value', [
    ('date', '2024-02-30'), ('date', '01/03/2024'),
    ('quantity', '1.5'), ('quantity', ''),
    ('unit_price', 'bad'), ('unit_price', '-inf'),
    ('total_amount', 'NaN'), ('total_amount', 'inf'),
    ('category', '  '), ('region', ''), ('order_id', ''), ('product', ''),
])
def test_invalid_record_rejects_entire_file(tmp_path, column, value):
    bad = dict(BASE, **{column: value})
    with pytest.raises(ValueError, match=column):
        load_sales(csv_file(tmp_path, [BASE, bad]))


def test_malformed_csv(tmp_path):
    path = tmp_path / 'bad.csv'
    path.write_text(','.join(BASE) + '\n"unterminated')
    with pytest.raises(ValueError):
        load_sales(path)


def test_extra_columns_and_negative_amounts_allowed(tmp_path):
    row = dict(BASE, total_amount='-10.50', extra='ignored')
    df = load_sales(csv_file(tmp_path, [row]))
    assert df.loc[0, 'total_amount'] == -10.5
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -q`.
Expected: collection failure because `sales_data` does not yet exist. Read and explain
the invalid-record test: one bad record must reject the entire input, preventing partial totals.

- [ ] Implement the loader:

```python
from pathlib import Path
import math
import pandas as pd

COLUMNS = ['date', 'order_id', 'product', 'category', 'region',
           'quantity', 'unit_price', 'total_amount']


def load_sales(path: str | Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError('Could not read the sales CSV. Check the file and its format.') from exc
    missing = sorted(set(COLUMNS) - set(df.columns))
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(missing))
    if df.empty:
        raise ValueError('The sales CSV contains no transactions.')
    df = df[COLUMNS].copy()
    for column in ['order_id', 'product', 'category', 'region']:
        df[column] = df[column].str.strip()
        if df[column].isna().any() or df[column].eq('').any():
            raise ValueError(f'Invalid {column}: blank values are not allowed.')
    if not df['date'].str.fullmatch(r'\d{4}-\d{2}-\d{2}', na=False).all():
        raise ValueError('Invalid date: use YYYY-MM-DD.')
    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='raise')
    except (ValueError, OverflowError) as exc:
        raise ValueError('Invalid date: expected real calendar dates.') from exc
    for column in ['quantity', 'unit_price', 'total_amount']:
        values = pd.to_numeric(df[column], errors='coerce')
        if not values.map(math.isfinite).all():
            raise ValueError(f'Invalid {column}: finite numbers are required.')
        if column == 'quantity' and (values % 1 != 0).any():
            raise ValueError('Invalid quantity: whole numbers are required.')
        df[column] = values
    return df
```

- [ ] Create the basic app:

```python
from pathlib import Path
import streamlit as st
from sales_data import load_sales

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'sales-data.csv'
st.set_page_config(page_title='ShopSmart Sales Dashboard', layout='wide')
st.title('ShopSmart Sales Dashboard')
try:
    data = load_sales(DATA_PATH)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
st.caption(f"Historical sales • {data['date'].min():%b %d, %Y} – "
           f"{data['date'].max():%b %d, %Y} • Source: data/sales-data.csv")
```

- [ ] Rerun `venv/bin/python -m pytest tests/test_sales_data.py -q`.
Expected: all loader tests pass. Start `venv/bin/streamlit run app.py --server.headless true`,
open the shown local URL, and verify the title and date caption without an error.
Expected: title and Jan 3–Dec 31, 2024 caption. Keep the server available for later UI checks.

- [ ] Commit `TASK-1: Add validated CSV loading and dashboard shell`, record its hash
and actual observations in TASKS.md, commit the board update, then run
`git push -u origin feature/sales-dashboard`.
Expected: branch pushed. If Git authentication is required, guide the student through
normal authentication without putting credentials into files or chat.

### Task 2: Sales and order KPIs [TASK-2]

**Files:** Modify `sales_data.py`, `app.py`, `tests/test_sales_data.py`, `TASKS.md`.

**Interfaces:** Consumes validated DataFrame; produces `sales_totals(data: pd.DataFrame) -> tuple[float, int]`.

- [ ] Append the test, importing `sales_totals`:

```python
def test_totals_count_transactions_not_quantity_or_unique_ids():
    data = pd.DataFrame({'total_amount': [10.25, 20.50, -5.00],
                         'quantity': [2, 4, 1], 'order_id': ['A', 'A', 'B']})
    sales, orders = sales_totals(data)
    assert sales == pytest.approx(25.75)
    assert orders == 3
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -q`.
Expected: missing `sales_totals` import failure.

- [ ] Implement and import into `app.py`:

```python
def sales_totals(data: pd.DataFrame) -> tuple[float, int]:
    return float(data['total_amount'].sum()), len(data)
```

Append to the app after successful loading:

```python
sales, orders = sales_totals(data)
sales_column, orders_column = st.columns(2)
sales_column.metric('Total Sales', f'${sales:,.2f}')
orders_column.metric('Total Orders', f'{orders:,}')
```

- [ ] Run the full data suite. Expected: all tests pass. Inspect the local dashboard:
Expected: `$116,500.21` and `482` in two cards.
- [ ] Commit `TASK-2: Add tested sales and order scorecards`; record hash/Notes,
complete the milestone board update, and push the feature branch.

### Task 3: Monthly sales trend [TASK-3]

**Files:** Modify `sales_data.py`, `app.py`, `tests/test_sales_data.py`, `TASKS.md`.

**Interfaces:** Consumes validated DataFrame; produces `monthly_sales(data: pd.DataFrame) -> pd.DataFrame` with date-valued `month` and numeric `total_amount` columns.

- [ ] Append this test and import `monthly_sales`:

```python
def test_monthly_sales_preserves_year_and_sorts():
    data = pd.DataFrame({
        'date': pd.to_datetime(['2025-01-05', '2024-02-01', '2024-01-20', '2024-01-02']),
        'total_amount': [40.0, 30.0, 20.0, 10.0],
    })
    result = monthly_sales(data)
    assert result['month'].tolist() == list(pd.to_datetime(['2024-01-01', '2024-02-01', '2025-01-01']))
    assert result['total_amount'].tolist() == [30.0, 30.0, 40.0]
```

- [ ] Run the data suite. Expected: import fails for missing `monthly_sales`.
- [ ] Implement:

```python
def monthly_sales(data: pd.DataFrame) -> pd.DataFrame:
    months = data['date'].dt.to_period('M').dt.to_timestamp()
    return (data.assign(month=months).groupby('month', as_index=False)['total_amount']
            .sum().sort_values('month').reset_index(drop=True))
```

Import `plotly.express as px` and `monthly_sales` in the app. Append:

```python
trend = px.line(monthly_sales(data), x='month', y='total_amount',
                title='Monthly Sales Trend', markers=True,
                labels={'month': 'Month', 'total_amount': 'Sales ($)'},
                color_discrete_sequence=['#2563EB'])
trend.update_traces(hovertemplate='%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>')
trend.update_yaxes(tickprefix='$', tickformat=',.0f')
st.plotly_chart(trend, width='stretch')
```

- [ ] Run the data suite. Expected: all tests pass. Inspect the local line chart and
hover: 12 chronological months, exact two-decimal sales in tooltips.
- [ ] Commit `TASK-3: Add tested monthly sales trend`; update TASKS.md with hash/Notes,
commit the board update, and push.

### Task 4: Category and region bars [TASK-4]

**Files:** Modify `sales_data.py`, `app.py`, `tests/test_sales_data.py`, `TASKS.md`.

**Interfaces:** Consumes validated data and grouping column (`category` or `region`);
produces `group_sales(data: pd.DataFrame, column: str) -> pd.DataFrame` with group column and `total_amount`, sorted descending, alphabetically for ties.

- [ ] Append this test and import `group_sales`:

```python
@pytest.mark.parametrize('column', ['category', 'region'])
def test_group_sales_includes_all_groups_and_sorts_ties(column):
    data = pd.DataFrame({column: ['Z', 'B', 'A', 'Z', 'New'],
                         'total_amount': [20.0, 30.0, 30.0, 25.0, -2.0]})
    result = group_sales(data, column)
    assert result[column].tolist() == ['Z', 'A', 'B', 'New']
    assert result['total_amount'].tolist() == [45.0, 30.0, 30.0, -2.0]
```

- [ ] Run the data suite. Expected: missing `group_sales` import failure.
- [ ] Implement:

```python
def group_sales(data: pd.DataFrame, column: str) -> pd.DataFrame:
    return (data.groupby(column, as_index=False)['total_amount'].sum()
            .sort_values(['total_amount', column], ascending=[False, True])
            .reset_index(drop=True))
```

Import the function into the app and append:

```python
for container, column in zip(st.columns(2), ['category', 'region']):
    grouped = group_sales(data, column)
    chart = px.bar(grouped, x='total_amount', y=column, orientation='h',
                   title=f'Sales by {column.title()}',
                   labels={'total_amount': 'Sales ($)', column: column.title()},
                   category_orders={column: grouped[column].tolist()},
                   color_discrete_sequence=['#2563EB'])
    chart.update_traces(hovertemplate='%{y}<br>Sales: $%{x:,.2f}<extra></extra>')
    chart.update_xaxes(tickprefix='$', tickformat=',.0f')
    container.plotly_chart(chart, width='stretch')
```

- [ ] Run the data suite. Expected: all tests pass. Inspect bars: five categories,
four regions, largest group at top, exact-value hover, no truncated labels.
- [ ] Commit `TASK-4: Add tested category and region breakdowns`; update board/hash/Notes,
commit the board update, and push.

### Task 5: Verify, document, review, and merge [TASK-5]

**Files:** Create `tests/test_app.py`, `AGENTS.md`; modify `tests/test_sales_data.py`, `README.md`, `TASKS.md`; change application files only for evidenced defects.

**Interfaces:** Consumes all four data functions and completed `app.py`; produces a tested, reviewed main branch and project instructions.

- [ ] Add independent source-data and UI checks. These integration checks verify existing behavior;
if they reveal a defect, use the failure as the regression test before fixing it.
Append to `tests/test_sales_data.py` (import csv and Decimal):

```python
def test_supplied_csv_matches_independent_calculation():
    import csv
    from decimal import Decimal
    path = Path(__file__).resolve().parents[1] / 'data' / 'sales-data.csv'
    with path.open() as source:
        rows = list(csv.DictReader(source))
    expected = sum(Decimal(row['total_amount']) for row in rows)
    data = load_sales(path)
    sales, orders = sales_totals(data)
    assert orders == len(rows) == 482
    assert expected == Decimal('116500.21')
    assert sales == pytest.approx(float(expected))
    assert monthly_sales(data)['total_amount'].sum() == pytest.approx(sales)
    for column in ['category', 'region']:
        assert group_sales(data, column)['total_amount'].sum() == pytest.approx(sales)
```

Create `tests/test_app.py`:

```python
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / 'app.py'


def test_dashboard_runs_outside_project_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP)).run(timeout=10)
    assert not app.exception
    assert not app.error
    assert [metric.value for metric in app.metric] == ['$116,500.21', '482']
    assert len(app.get('plotly_chart')) == 3


def test_loading_error_stops_before_metrics_or_charts():
    with patch('sales_data.load_sales', side_effect=ValueError('Invalid date in sales CSV.')):
        app = AppTest.from_file(str(APP)).run(timeout=10)
    assert not app.exception
    assert app.error[0].value == 'Invalid date in sales CSV.'
    assert len(app.metric) == 0
    assert len(app.get('plotly_chart')) == 0
```

- [ ] Run `venv/bin/python -m pytest -q`.
Expected: all tests pass; investigate failures before proceeding.
- [ ] Inspect the actual browser page, hover each chart, and check console/server output.
Use browser timing observations for navigation-to-visible-content and chart display;
record the measurement method and actual observations against 5s/2s targets. Report
unmeasured environments honestly. Do not substitute server health for visual verification.
- [ ] Explain one calculation test and one app diff to the student; preserve their actual
feedback in Notes when provided. Do not write a student reflection on their behalf.
- [ ] Use Codex `/init` or its project-memory equivalent to create `AGENTS.md`. Include:

```markdown
# Project guide
This project implements the LMU Phase 1 sales dashboard.
Use venv/ and requirements.txt; do not use uv or conda.
Run: source venv/bin/activate && streamlit run app.py
Test: venv/bin/python -m pytest -q
app.py owns presentation; sales_data.py owns validation and calculations.
Keep changes within prd/ecommerce-analytics.md and the approved design.
Track milestones and completion commits in TASKS.md.

## Lessons
- Total Orders counts transaction rows, not quantity or distinct IDs.
- Monthly aggregation includes the year so January values from different years stay separate.
- Invalid CSV data stops the dashboard; never silently discard rows.
```

Add any real implementation lessons, with evidence. Commit project memory separately
as `Add project memory (AGENTS.md)`, as requested by the companion.

- [ ] Prepend setup instructions to README while retaining existing tutorial content:

```markdown
## Run this dashboard

Requires Python 3.11 or later.

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    streamlit run app.py

Run tests with `python -m pytest -q` after activating venv.
The dashboard uses the supplied historical CSV, monthly sales totals, and
all categories and regions. Invalid input stops the dashboard with an error.
```

- [ ] Commit verified changes as `TASK-5: Verify dashboard and document local usage` and push the feature branch.
- [ ] Run Codex `/review` against base branch `main`, using the companion's command;
use the fresh whole-branch reviewer required by executing-plans. Present genuine
findings to the student and obtain their fix decisions. If invoking native `/review`
is unavailable in this app, explain that limitation and guide the student to it in
Codex CLI; do not claim an unrun review. Do not invent findings to manufacture a fix commit.
- [ ] For accepted defects, write failing regression tests where meaningful, fix,
run `venv/bin/python -m pytest -q`, and commit `TASK-5: Fix review findings` with a descriptive suffix.
Expected: full suite passes and selected findings are resolved. Record deferred findings honestly.
- [ ] Verify clean working tree and run `git switch main` then
`git merge --no-ff feature/sales-dashboard -m 'Merge reviewed sales dashboard (TASK-5)'`.
Expected: a merge commit with two parents; resolve unexpected conflicts before proceeding.
- [ ] Record the TASK-5 implementation/fix hash and merge hash in TASKS.md, complete
its criteria, commit `TASK-5: Record completed review and merge`, then `git push origin main`.
Expected: GitHub main contains app.py, requirements.txt, data, tests, specs, plan,
AGENTS.md, and the completed implementation milestones. Confirm the public file list.

### Task 6: Student deployment and final bookkeeping [TASK-6; HUMAN EXECUTED]

**Files:** Modify `TASKS.md`, `README.md` only after verified deployment.

**Interfaces:** Consumes pushed and reviewed main branch; produces a working public Streamlit URL recorded in both files.

- [ ] **STOP and hand off to the student:** visit https://share.streamlit.io, sign in,
and create a public app from `ryanbran5/ai-dev-workflow-tutorial`, branch `main`, entry
point `app.py`. The student completes account authorization and clicks Deploy.
- [ ] Student opens the public URL and checks KPIs, trend, both breakdowns, and hover values.
Expected: same values and behavior as local dashboard. The student supplies the live URL.
- [ ] Verify the public dashboard, record its actual URL under TASK-6 and near the top
of README, check deployment criteria, and record the delivery commit hash with a
subsequent board commit. Do not insert an invented URL or claim deployment prematurely.
- [ ] Commit/push main with `TASK-6` messages. Verify all done milestones have checked
criteria, real Commit and Notes lines, and required artifacts remain in the repository.
- [ ] Give the student the repository URL and live app URL for their course submission;
remind them to be ready to explain a diff, a test, a requirement-to-commit trace, and
one genuine correction. Submission itself stays with the student.
