"""Load and calculate sales data without depending on the dashboard UI."""

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
