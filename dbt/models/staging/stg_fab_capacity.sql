select
    year,
    company,
    country_iso3,
    process_node_nm,
    fab_type,
    monthly_wafer_capacity,
    fab_started_year
from {{ source('raw', 'fab_capacity') }}
where year is not null
