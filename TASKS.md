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

## In Progress

## Done

- [x] **TASK-1: Project setup and data loading** — Deliver the basic app and CSV loading.
  - [x] App runs with `streamlit run app.py`.
  - [x] `data/sales-data.csv` loads correctly.
  - [x] Data processing is kept in `sales_data.py`.
  - Commit: `a72dc36`
  - Notes: Completed validated CSV loading and dashboard shell.

- [x] **TASK-2: KPI scorecards**
  - [x] Total Sales KPI implemented.
  - [x] Total Orders KPI implemented.
  - Notes: KPI cards are displayed in the dashboard.

- [x] **TASK-3: Sales trend chart**
  - [x] Monthly sales trend chart implemented.
  - [x] Sales are shown in chronological order.
  - Notes: Monthly aggregation was used for readability.

- [x] **TASK-4: Category and region breakdowns**
  - [x] Sales by Category chart implemented.
  - [x] Sales by Region chart implemented.
  - Notes: Both breakdown charts are included in the dashboard.

- [x] **TASK-5: Testing, refinement, and review**
  - [x] App was run locally and reviewed.
  - [x] Feature branch was merged into `main`.
  - Notes: Dashboard was verified locally before deployment.

- [x] **TASK-6: Deployment**
  - [x] App deployed from `main` to Streamlit Community Cloud.
  - [x] Public dashboard verified.
  - Live URL: https://ryanbran5-ai-dev-workflow-tutorial-app-ohgk2n.streamlit.app
  - Notes: Deployment completed successfully.
