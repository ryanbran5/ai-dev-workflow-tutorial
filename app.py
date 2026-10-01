"""Streamlit presentation for the historical sales dashboard."""

from pathlib import Path
import streamlit as st
import plotly.express as px
from sales_data import load_sales, sales_totals, monthly_sales, group_sales

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

trend = px.line(monthly_sales(data), x='month', y='total_amount',
                title='Monthly Sales Trend', markers=True,
                labels={'month': 'Month', 'total_amount': 'Sales ($)'},
                color_discrete_sequence=['#2563EB'])
trend.update_traces(hovertemplate='%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>')
trend.update_yaxes(tickprefix='$', tickformat=',.0f')
st.plotly_chart(trend, width='stretch')

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
