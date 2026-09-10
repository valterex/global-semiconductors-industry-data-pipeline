select
    {{ dbt_utils.generate_surrogate_key(['company', 'process_node_nm', 'year']) }} as company_node_year_key,
    year,
    company,
    country_iso3,
    process_node_nm,
    fab_type,
    monthly_wafer_capacity,
    monthly_wafer_capacity * 12 as annual_wafer_capacity,
    fab_started_year
from {{ ref('stg_fab_capacity') }}
