# Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard described in
`prd/ecommerce-analytics.md`. Milestones move from To Do to In Progress to Done.
The implementation plan will break these deliverables into smaller steps.

## Definition of Done

- The milestone's acceptance criteria are met.
- The app runs locally with `streamlit run app.py`.
- Changes are committed with the milestone ID in the commit message.
- The completion commit is recorded below, with an honest note about decisions or corrections.

## To Do

- [ ] **TASK-2: KPI scorecards** — Show sales and transaction totals prominently (PRD M3, FR-1).
  - [ ] Total Sales equals the sum of `total_amount` and displays as currency with separators.
  - [ ] Total Orders equals the transaction count and displays with separators.
  - [ ] Pytest tests verify the calculations against known inputs.
  - Commit:
  - Notes:

- [ ] **TASK-3: Sales trend chart** — Show sales over time (PRD M4, FR-2).
  - [ ] A chronologically ordered line chart uses daily or monthly aggregation, as agreed in the design.
  - [ ] Axes are clearly labeled and interactive tooltips show exact sales values.
  - [ ] Pytest tests verify aggregation and chronological order.
  - Commit:
  - Notes:

- [ ] **TASK-4: Category and region breakdowns** — Compare sales across all categories and regions (PRD M5, FR-3–FR-4).
  - [ ] Category and region bar charts include every group in the CSV and sort from highest to lowest sales.
  - [ ] Both charts have clear labels and interactive tooltips showing exact sales values.
  - [ ] Pytest tests verify grouped totals and ordering.
  - Commit:
  - Notes:

- [ ] **TASK-5: Testing, refinement, and review** — Verify the complete dashboard and prepare it for release (PRD M6, NFR-1–NFR-4).
  - [ ] Tests pass; local inspection confirms accurate CSV totals, all required visuals, professional layout, and no errors or warnings; record performance checks against the 5-second load and 2-second chart targets.
  - [ ] Project `AGENTS.md` includes a Lessons section; setup and run instructions are documented.
  - [ ] Review the feature branch against `main`, record findings and decisions, commit applicable fixes, and merge with a no-fast-forward merge commit before deployment.
  - Commit:
  - Notes:

- [ ] **TASK-6: Deployment** — Student deploys the reviewed main branch to Streamlit Community Cloud (PRD M7, NFR-5).
  - [ ] Student deploys `app.py` from the pushed `main` branch and verifies the public dashboard.
  - [ ] Record the live URL here and near the top of `README.md`.
  - [ ] Commit and push the completed task board and README to `main`.
  - Live URL:
  - Commit:
  - Notes:

## In Progress

- [ ] **TASK-1: Project setup and data loading** — Deliver the basic app and CSV loading (PRD M1–M2, FR-5).
  - [ ] A plain `venv/` and `requirements.txt` support running `streamlit run app.py`, which shows a dashboard title.
  - [ ] Load `data/sales-data.csv` with appropriate date, numeric, and categorical types; show a clear message for missing or invalid data.
  - [ ] Keep data processing in its own module with pytest coverage for loading and validation.
  - Commit:
  - Notes:

## Done
