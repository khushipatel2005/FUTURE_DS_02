import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Load Data
df = pd.read_csv(r"sales_data002.csv")
df['JoinDate'] = pd.to_datetime(df['JoinDate'])
df['LastActiveDate'] = pd.to_datetime(df['LastActiveDate'])

# KPIs
total_customers = df['CustomerID'].nunique()
active_customers = df[df['Churn']=="No"]['CustomerID'].nunique()
churned_customers = df[df['Churn']=="Yes"]['CustomerID'].nunique()
retention_rate = round((active_customers/total_customers)*100,2)
mrr = df['MonthlyCharges'].sum()
revenue_at_risk = df[df['Churn']=="Yes"]['MonthlyCharges'].sum()

st.title("Customer Retention & Churn Analysis Dashboard")

# KPI Row
col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric("Total Customers", total_customers)
col2.metric("Active Customers", active_customers)
col3.metric("Churned Customers", churned_customers)
col4.metric("Retention Rate %", retention_rate)
col5.metric("MRR", mrr)
col6.metric("Revenue at Risk", revenue_at_risk)

st.markdown("---")

# Charts Row 1
col1,col2,col3 = st.columns(3)

# Customer Distribution
fig1 = px.treemap(df, path=['SubscriptionType'])
col1.plotly_chart(fig1, use_container_width=True)

# Contract Impact
fig2 = px.histogram(df, x='ContractType', color='Churn', barmode='group')
col2.plotly_chart(fig2, use_container_width=True)

# Revenue Mix by Region
fig3 = px.bar(df, x='Region', y='MonthlyCharges', color='SubscriptionType')
col3.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Matrix Table
pivot = pd.pivot_table(df,
                       values='MonthlyCharges',
                       index='Region',
                       columns='SubscriptionType',
                       aggfunc='mean')

st.subheader("Region - Plan Matrix")
st.dataframe(pivot)

# Customer Lifetime
df['TenureMonths'] = (df['LastActiveDate'] - df['JoinDate']).dt.days/30
fig4 = px.box(df, x='SubscriptionType', y='TenureMonths', color='Churn')
st.plotly_chart(fig4, use_container_width=True)