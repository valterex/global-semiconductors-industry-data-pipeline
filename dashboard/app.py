import os

import pandas as pd
import streamlit as st
from google.cloud import bigquery

DATASET = "global_semiconductor_industry"

st.set_page_config(page_title="Semiconductor Dashboard", layout="wide")


@st.cache_resource
def get_client() -> bigquery.Client:
    return bigquery.Client(project=os.environ["GCP_PROJECT_ID"])


@st.cache_data(ttl=3600)
def load_ai_chip_revenue() -> pd.DataFrame:
    project = os.environ["GCP_PROJECT_ID"]
    sql = f"""
        select vendor, year, revenue_usd_m
        from `{project}.{DATASET}.fct_ai_chip_revenue_yearly`
    """
    return get_client().query(sql).to_dataframe()


@st.cache_data(ttl=3600)
def load_export_controls() -> pd.DataFrame:
    project = os.environ["GCP_PROJECT_ID"]
    sql = f"""
        select year, administration, actions
        from `{project}.{DATASET}.fct_export_controls_yearly`
    """
    return get_client().query(sql).to_dataframe()


st.title("Global Semiconductor Industry")
st.caption("AI chip revenue and export controls, sourced from the BigQuery marts.")

if "GCP_PROJECT_ID" not in os.environ:
    st.error("Set the `GCP_PROJECT_ID` environment variable, then restart the app.")
    st.stop()

revenue = load_ai_chip_revenue()
controls = load_export_controls()

min_year = int(min(revenue["year"].min(), controls["year"].min()))
max_year = int(max(revenue["year"].max(), controls["year"].max()))

with st.sidebar:
    st.header("Filters")
    year_range = st.slider("Year", min_year, max_year, (min_year, max_year))
    vendors = st.multiselect("Vendor", sorted(revenue["vendor"].unique()))

revenue = revenue[revenue["year"].between(*year_range)]
controls = controls[controls["year"].between(*year_range)]

if vendors:
    revenue = revenue[revenue["vendor"].isin(vendors)]

st.subheader("AI chip estimated revenue by vendor (USD m)")
revenue_pivot = revenue.pivot(index="year", columns="vendor", values="revenue_usd_m")

st.area_chart(revenue_pivot)

st.subheader("Export-control actions by administration")
controls_pivot = controls.pivot(
    index="year", columns="administration", values="actions"
)

st.bar_chart(controls_pivot)
