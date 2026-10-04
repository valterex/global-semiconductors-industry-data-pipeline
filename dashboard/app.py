import pandas as pd
import streamlit as st
from google.cloud import bigquery

from dashboard.config import gcp_config
from dashboard.queries import get_client, load_ai_chip_revenue, load_export_controls
from dashboard.transforms import (
    filter_by_vendors,
    filter_by_year,
    pivot_controls,
    pivot_revenue,
    year_range,
)

st.set_page_config(page_title="Semiconductor Dashboard", layout="wide")

PROJECT, DATASET = gcp_config()

if not PROJECT or not DATASET:
    st.error(
        "Set the `GCP_PROJECT_ID` and `GCP_DATASET` environment variables, "
        "then restart the app."
    )
    st.stop()

# `st.stop()` raises at runtime, but type checkers can't infer that, so narrow
# the optional values here.
assert PROJECT is not None and DATASET is not None


@st.cache_resource
def get_client_cached(project: str) -> bigquery.Client:
    return get_client(project)


@st.cache_data(ttl=3600)
def load_ai_chip_revenue_cached(project: str, dataset: str) -> pd.DataFrame:
    return load_ai_chip_revenue(get_client_cached(project), project, dataset)


@st.cache_data(ttl=3600)
def load_export_controls_cached(project: str, dataset: str) -> pd.DataFrame:
    return load_export_controls(get_client_cached(project), project, dataset)


st.title("Global Semiconductor Industry")
st.caption("AI chip revenue and export controls, sourced from the BigQuery marts.")

try:
    revenue = load_ai_chip_revenue_cached(PROJECT, DATASET)
    controls = load_export_controls_cached(PROJECT, DATASET)
except Exception as exc:
    st.error(f"Failed to load data from BigQuery: {exc}")
    st.stop()

min_year, max_year = year_range(revenue, controls)

with st.sidebar:
    st.header("Filters")
    year_range_value = st.slider("Year", min_year, max_year, (min_year, max_year))
    vendors = st.multiselect("Vendor", sorted(revenue["vendor"].unique()))

revenue = filter_by_year(revenue, *year_range_value)
controls = filter_by_year(controls, *year_range_value)
revenue = filter_by_vendors(revenue, vendors)

st.subheader("AI chip estimated revenue by vendor (USD m)")
st.area_chart(pivot_revenue(revenue))

st.subheader("Export-control actions by administration")
st.bar_chart(pivot_controls(controls))
