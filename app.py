"""Streamlit presentation for the historical sales dashboard."""

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
