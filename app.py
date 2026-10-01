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
total_sales = data["total_amount"].sum() / 100
total_orders = data["order_id"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Orders", f"{total_orders:,}")
st.subheader("Sales Trend")

daily_sales = (
    data.groupby("date", as_index=False)["total_amount"]
    .sum()
)

daily_sales["sales"] = daily_sales["total_amount"] / 100

st.line_chart(
    daily_sales,
    x="date",
    y="sales"
    )
st.subheader("Sales by Category")

category_sales = (
    data.groupby("category", as_index=False)["total_amount"]
    .sum()
)

category_sales["sales"] = category_sales["total_amount"] / 100

st.bar_chart(
    category_sales,
    x="category",
    y="sales"
)

st.subheader("Sales by Region")

region_sales = (
    data.groupby("region", as_index=False)["total_amount"]
    .sum()
)

region_sales["sales"] = region_sales["total_amount"] / 100

st.bar_chart(
    region_sales,
    x="region",
    y="sales"
)