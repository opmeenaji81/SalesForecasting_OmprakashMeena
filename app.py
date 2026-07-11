# Task 5 – Interactive Streamlit Dashboard

# pip install streamlit requirement

# sales forcasting Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px

# page configuration

st.set_page_config(
    page_title = "Sales Forecasting Dashboard",
    page_icon="📈",
    layout = "wide"
)

st.title("📈 Sales Forecasting Dashboard")
st.markdown("---")

# Dataset loading

sales_df = pd.read_csv("train.csv")
vg_df = pd.read_csv("vgsales.csv")

sales_df["Order Date"] = pd.to_datetime(
    sales_df["Order Date"],
    dayfirst= True
)

# Sidebar

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Forecasting",
        "Anomaly Detection",
        "Clustering"
    ]
)

# Dashboard Page

if page == "Dashboard":
    st.header("Business Overview")
    total_sales = sales_df["Sales"].sum()
    
    average_sales = sales_df["Sales"].mean()
    highest_sale = sales_df["Sales"].max()
    
    total_orders = sales_df.shape[0]
    
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )
    
    c2.metric(
        "Average Sale",
        f"${average_sales:,.2f}"
    )
    
    c3.metric(
        "Higest Sale",
        f"${highest_sale:,.2f}"
    )
    
    c4.metric(
        "Orders",
        total_orders
    )
    
    st.markdown("---")
    st.subheader("📈 Monthly Sales Trend ")
    
    monthly_sales = (
        sales_df
        .groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
        
    )
    
    fig = px.line(
        monthly_sales,
        x = "Order Date",
        y = "Sales",
        title = "Monthly Sales Trend",
        markers = True
    )
    
    fig.update_layout(
        xaxis_title = "Date",
        yaxis_title = "Sales"
    )
    
    st.plotly_chart(
        fig,
        use_container_width= True
    )
    
    # two charts side by side
    
    st.markdown("---")
    left, right = st.columns(2)
    
    #Left Column - Category Revenue
    
    with left:
        st.subheader("📈 Sales by Category")
        
        category_sales = (
            sales_df
            .groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )
        
        fig = px.bar(
            category_sales,
            x = "Category",
            y = "Sales",
            color = "Category"
        )
        
        st.plotly_chart(
            fig,
            use_container_width= True
        )
        
    #right column - region revenue
    
    with right:
        
        st.subheader("🗺️ Sales by Region")
        
        region_sales = (
            sales_df
            .groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )
        
        fig = px.pie(
            region_sales,
            names = "Region",
            values = "Sales"
        )
        
        st.plotly_chart(
            fig,
            use_container_width= True
        )
        
        
    # TOP  10 STATES
    
    st.markdown("---")
    st.subheader("🔝 Top 10 States by Revenue")
    
    top_states = (
        sales_df
        .groupby("State")["Sales"]
        .sum()
        .sort_values(ascending= False)
        .head(10)
        .reset_index()
    )
    
    fig = px.bar(
        top_states,
        x = "Sales",
        y = "State",
        orientation = "h",
        color = "Sales"
    )
    
    st.plotly_chart(
        fig,
        use_container_width= True
    )