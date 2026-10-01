"""Streamlit presentation for the historical sales dashboard."""

from pathlib import Path
import streamlit as st
from sales_data import load_sales, sales_totals

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

sales, orders = sales_totals(data)
sales_column, orders_column = st.columns(2)
sales_column.metric('Total Sales', f'${sales:,.2f}')
orders_column.metric('Total Orders', f'{orders:,}')
