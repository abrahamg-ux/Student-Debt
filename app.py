import streamlit as st
import pandas as pd
import plotly.express as px
import glob
st.set_page_config(
    page_title="College Cost, Debt, and Earnings Dashboard",
    layout="wide"
)

st.title("College Cost, Debt, and Earnings Dashboard")
st.write(
    "This dashboard explores college cost, student debt, and post-graduation earnings "
    "across institutions in Connecticut, Florida, and Georgia."
)

# Load data

csv_files = glob.glob("*.csv")
st.write("CSV files found:", csv_files)

data_file = [file for file in csv_files if "Master" in file][0]

df = pd.read_csv(data_file)

# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

states = st.sidebar.multiselect(
    "Select State",
    options=sorted(df["State"].dropna().unique()),
    default=sorted(df["State"].dropna().unique())
)

institution_types = st.sidebar.multiselect(
    "Select Institution Type",
    options=sorted(df["Institution Type"].dropna().unique()),
    default=sorted(df["Institution Type"].dropna().unique())
)

years = st.sidebar.multiselect(
    "Select Academic Year",
    options=sorted(df["Academic Year"].dropna().unique()),
    default=sorted(df["Academic Year"].dropna().unique())
)

filtered_df = df[
    (df["State"].isin(states)) &
    (df["Institution Type"].isin(institution_types)) &
    (df["Academic Year"].isin(years))
]

# Key metrics
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Cost", f"${filtered_df['Average Cost'].mean():,.0f}")
col2.metric("Median Debt", f"${filtered_df['Median Debt'].mean():,.0f}")
col3.metric("Earnings 6 Years Out", f"${filtered_df['Earnings (6 Years Out)'].mean():,.0f}")
col4.metric("Earnings 10 Years Out", f"${filtered_df['Earnings (10 Years Out)'].mean():,.0f}")

st.divider()

# Chart 1: Average Cost Over Time
st.subheader("Average Cost Over Time by Institution Type")

cost_time = (
    filtered_df
    .groupby(["Academic Year", "Institution Type"], as_index=False)["Average Cost"]
    .mean()
)

fig1 = px.line(
    cost_time,
    x="Academic Year",
    y="Average Cost",
    color="Institution Type",
    markers=True,
    title="Average College Cost Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Earnings Over Time
st.subheader("Earnings 10 Years Out Over Time by Institution Type")

earnings_time = (
    filtered_df
    .groupby(["Academic Year", "Institution Type"], as_index=False)["Earnings (10 Years Out)"]
    .mean()
)

fig2 = px.line(
    earnings_time,
    x="Academic Year",
    y="Earnings (10 Years Out)",
    color="Institution Type",
    markers=True,
    title="Average Earnings 10 Years Out Over Time"
)

st.plotly_chart(fig2, use_container_width=True)

# Two-column layout
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Average Earnings by Institution Type")

    earnings_type = (
        filtered_df
        .groupby("Institution Type", as_index=False)["Earnings (10 Years Out)"]
        .mean()
    )

    fig3 = px.bar(
        earnings_type,
        x="Institution Type",
        y="Earnings (10 Years Out)",
        color="Institution Type",
        title="Average Earnings 10 Years Out by Institution Type"
    )

    st.plotly_chart(fig3, use_container_width=True)

with right_col:
    st.subheader("Median Debt by State")

    debt_state = (
        filtered_df
        .groupby("State", as_index=False)["Median Debt"]
        .mean()
    )

    fig4 = px.bar(
        debt_state,
        x="State",
        y="Median Debt",
        color="State",
        title="Average Median Debt by State"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Scatter plot
st.subheader("Average Cost vs Earnings 10 Years Out")

fig5 = px.scatter(
    filtered_df,
    x="Average Cost",
    y="Earnings (10 Years Out)",
    color="Institution Type",
    hover_name="University Name",
    size="Median Debt",
    title="Does Higher College Cost Lead to Higher Earnings?"
)

st.plotly_chart(fig5, use_container_width=True)

# Top 10 schools
st.subheader("Top 10 Institutions by Earnings 10 Years Out")

top_10 = (
    filtered_df
    .sort_values("Earnings (10 Years Out)", ascending=False)
    .head(10)
)

fig6 = px.bar(
    top_10,
    x="Earnings (10 Years Out)",
    y="University Name",
    color="Institution Type",
    orientation="h",
    title="Top 10 Institutions by Earnings 10 Years Out"
)

fig6.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig6, use_container_width=True)

# Data preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(25))
