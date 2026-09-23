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
