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
