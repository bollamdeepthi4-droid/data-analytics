import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales & Revenue Dashboard",
                   page_icon="📊",
                   layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data Loaded Successfully")

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    regions = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    products = st.sidebar.multiselect(
        "Select Product",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    start_date = st.sidebar.date_input(
        "Start Date",
        value=df["Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=df["Date"].max()
    )

    filtered = df[
        (df["Region"].isin(regions)) &
        (df["Product"].isin(products)) &
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date))
    ]

    # KPIs
    total_sales = filtered["Quantity"].sum()
    total_revenue = filtered["Revenue"].sum()
    total_orders = filtered["Order ID"].nunique()
    avg_order = total_revenue / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"{total_sales:,}")
    col2.metric("Revenue", f"${total_revenue:,.2f}")
    col3.metric("Orders", total_orders)
    col4.metric("Avg Order", f"${avg_order:,.2f}")

    st.divider()

    # Revenue Trend
    revenue_trend = filtered.groupby("Date")["Revenue"].sum().reset_index()

    fig1 = px.line(
        revenue_trend,
        x="Date",
        y="Revenue",
        title="Revenue Trend",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    # Top Products
    top_products = filtered.groupby("Product")["Revenue"].sum().reset_index()
    top_products = top_products.sort_values(
        by="Revenue",
        ascending=False
    )

    fig2 = px.bar(
        top_products,
        x="Revenue",
        y="Product",
        orientation="h",
        title="Top Performing Products"
    )

    col1.plotly_chart(fig2, use_container_width=True)

    # Sales by Region
    region_sales = filtered.groupby("Region")["Revenue"].sum().reset_index()

    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Revenue",
        title="Revenue by Region"
    )

    col2.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Monthly Revenue
    filtered["Month"] = filtered["Date"].dt.to_period("M").astype(str)

    monthly = filtered.groupby("Month")["Revenue"].sum().reset_index()

    fig4 = px.bar(
        monthly,
        x="Month",
        y="Revenue",
        color="Revenue",
        title="Monthly Revenue"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    st.subheader("Filtered Data")

    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Data",
        csv,
        "filtered_sales.csv",
        "text/csv"
    )

else:
    st.info("Please upload a CSV or Excel file.")