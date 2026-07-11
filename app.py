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
vg_df = pd.read_csv("vgsales_processed.csv")

sales_df["Order Date"] = pd.to_datetime(
    sales_df["Order Date"],
    dayfirst= True
)

# Sidebar

st.sidebar.image(
    "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
    width=120
)

st.sidebar.title("Sales Forecasting Dashboard")

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Forecasting",
        "Anomaly Detection",
        "Clustering"
    ]
)

# Sidebar Filters

st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options = sorted(sales_df["Region"].unique()),
    default = sorted(sales_df["Region"].unique())
)

selected_category = st.sidebar.multiselect(
    "Selecte Category",
    options = sorted(sales_df["Category"].unique()),
    default = sorted(sales_df["Category"].unique())
)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options = sorted(sales_df["Segment"].unique()),
    default = sorted(sales_df["Segment"].unique()),
    
)

# applyling filters

filtered_df = sales_df[
    (sales_df["Region"].isin(selected_region)) &
    (sales_df["Category"].isin(selected_category)) &
    (sales_df["Segment"].isin(selected_segment))
]


# Dashboard Page

if page == "Dashboard":
    st.header("Business Overview")
    total_sales = filtered_df["Sales"].sum()
    
    average_sales = filtered_df["Sales"].mean()
    highest_sale = filtered_df["Sales"].max()
    
    total_orders = filtered_df.shape[0]
    
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
        filtered_df
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
            filtered_df
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
            filtered_df
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
        filtered_df
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
    
    st.markdown("---")

    st.subheader("📋 Filtered Dataset Preview")

    st.dataframe(filtered_df.head(20))
    
    
    # download filtered data
    
    st.markdown("---")
    
    st.subheader("📥 Download Filtered Data")
    
    csv = filtered_df.to_csv(index= False).encode("utf-8")
    
    st.download_button(
        label = "Download CSV",
        data = csv,
        file_name = "filtered_sales_data.csv",
        mime = "text/csv"
    )
    
# forecastin page

elif page == "Forecasting":
    
    st.header("🔮 Sales Forecasting")
    
    model = st.selectbox(
        "Select Forecasting Model",
        ["SARIMA", "Prophet", "XGBoost"]
    )
    
    st.write(f"### Selected Model: {model}")
    
    st.info(
        "Forecasts were generated during the notebook analysis phase."
        "This dashboard presents the selected forecasting approach."
        
    )
    
# anomaly Detection page

elif page == "Anomaly Detection":

    st.header("⚠️ Anomaly Detection")

    st.write(
        "Isolation Forest was used to identify unusual sales records "
        "in the Video Game Sales dataset."
    )

    anomaly_count = (vg_df["Anomaly"] == -1).sum()

    st.metric("Detected Anomalies", anomaly_count)

    fig = px.scatter(
        vg_df,
        x="Global_Sales",
        y="NA_Sales",
        color="Anomaly",
        title="Isolation Forest Results"
    )

    st.plotly_chart(fig, use_container_width=True)
    
# Clusterin Page

elif page == "Clustering":
    st.header("🎯 Customer / Sales Clustering")
    
    st.write(
        "K-Means clustering grouped similar sales pattern "
        "using regional and global sales."
    )
    
    cluster_counts = vg_df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]
    
    fig = px.bar(
        cluster_counts,
        x = "Cluster",
        y = "Count",
        color = "Cluster"
    )
    
    st.plotly_chart(fig, use_container_width= True)
    
    
# Footer

st.markdown("---")

st.caption(
    "Developed by Omprakash Meena | Xylofi Internship Project | Sales Forecasting using Machine Learning"
)