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
- A Done checkbox is not evidence: verify the corresponding code, tests, commit, and deployed page before updating TASKS.md.
- Restart Streamlit after adding imports; a long-running process can retain an older sales_data module.
- The 2026-10-01 repair restored missing KPIs/charts after a board-only completion commit.

AGENTS.md is the Codex companion filename. CLAUDE.md is kept identical for the course review.
