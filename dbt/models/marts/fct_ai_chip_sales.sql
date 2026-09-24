select
    {{ dbt_utils.generate_surrogate_key(['vendor', 'chip_name', 'year']) }} as chip_year_key,
    {{ dbt_utils.generate_surrogate_key(['vendor', 'chip_name']) }} as chip_key,
    year,
    estimated_shipments_units,
    estimated_asp_usd,
    estimated_revenue_usd_m
from {{ ref('stg_ai_chip_market') }}
