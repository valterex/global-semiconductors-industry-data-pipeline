select
    year,
    company,
    country_iso3,
    process_node_nm,
    fab_type,
    monthly_wafer_capacity,
    monthly_wafer_capacity * 12 as annual_wafer_capacity,
    fab_started_year
from {{ ref('stg_fab_capacity') }}
